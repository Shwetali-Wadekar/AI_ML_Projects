import os
import json
from google.adk.agents import Agent, SequentialAgent, ParallelAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.runners import Runner
from google.adk.tools import load_memory

# Import Agent Creators
from app.agents.dataset_agent import create_dataset_agent
from app.agents.eval_agent import create_eval_agent
from app.agents.strategy_agent import create_strategy_agent
from app.agents.sota_agent import create_sota_agent
# Import services 
from app.db.memory import session_service, memory_service 

MODEL_NAME = "gemini-2.0-flash-lite"
from pathlib import Path

LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"

async def auto_save_orchestrator_turn_to_memory(callback_context):
    """
    Callback function that automatically saves the current session 
    (user prompt and orchestrator's plan) to long-term memory 
    after the agent completes its turn.
    """
    print("🔑 Auto-saving Orchestrator turn to MemoryService...")
    # The callback_context contains the runner's internal invocation context, 
    # which holds the session and memory services.
    try:
        # Access the memory service and current session via the callback_context
        await callback_context._invocation_context.memory_service.add_session_to_memory(
            callback_context._invocation_context.session
        )
    except AttributeError:
        # Handle case where internal structure might change or context is missing
        print("⚠️ Warning: Could not access memory service via callback context.")
        # In a stable version of the ADK, the access path should be consistent.
    except Exception as e:
        print(f"⚠️ Error saving memory: {e}")

# --- Define Global Retry Configuration ---
RETRY_CONFIG = types.HttpRetryOptions(
    attempts=4,               # Total attempts (1 initial + 3 retries)
    initial_delay=1,          # Initial delay before the first retry (seconds)
    exp_base=2.0,             # Delay multiplier
    http_status_codes=[429, 500, 503, 504] # Retry on these errors
)
# ---------------------------------------

class VisionOrchestrator:
    def __init__(self):
        # 1. Initialize Individual Agents
        self.orchestrator_agent = Agent(
            name="OrchestratorAgent",
            description="Converts user requests into structured task plans for computer vision projects.",
            model=Gemini(model=MODEL_NAME, retry_options=RETRY_CONFIG),
            instruction="""
            Convert the user's request into a compact JSON plan for downstream agents. 
            Identify the core task and necessary keywords. Output ONLY JSON: 
            {"task": "...", "keywords": [...], "negative_keywords": [...], "additional_notes": "..."}
            """,
            output_key="task_request",
            after_agent_callback=auto_save_orchestrator_turn_to_memory
        )
        self.sota = create_sota_agent(MODEL_NAME, retry_config=RETRY_CONFIG)
        self.data = create_dataset_agent(MODEL_NAME, retry_config=RETRY_CONFIG)
        self.eval = create_eval_agent(MODEL_NAME, retry_config=RETRY_CONFIG)
        self.strategy = create_strategy_agent(MODEL_NAME, retry_config=RETRY_CONFIG)

        # 2. Parallel Step
        self.parallel_research = ParallelAgent(
            name="ParallelVisionResearch",
            sub_agents=[self.sota, self.data, self.eval]
        )

        # 3. Sequential Pipeline
        self.pipeline = SequentialAgent(
            name="VisionWorkflowPipeline",
            sub_agents=[
                self.orchestrator_agent,
                self.parallel_research,
                self.strategy
            ]
        )

        # 4. Runner
        self.runner = Runner(
            agent=self.pipeline,
            app_name="VisionWorkflowApp",
            session_service=session_service,
            memory_service=memory_service
        )

    async def process_query(self, user_query: str, session_id: str):
        print(f"--- Processing: {user_query} (Session: {session_id}) ---")
        
        # Ensure session exists (using the session_id pattern fix)
        try:
            session = await session_service.create_session(
                app_name="VisionWorkflowApp", user_id="api_user", session_id=session_id
            )
        except:
            session = await session_service.get_session(
                app_name="VisionWorkflowApp", user_id="api_user", session_id=session_id
            )

        query_content = types.Content(role="user", parts=[types.Part(text=user_query)])

        # Dictionary to store all steps, including the final strategy
        full_workflow_log = {
            "session_id": session_id,
            "user_query": user_query,
            "intermediate_results": {}
        }
        final_output = ""
        
        # Execute Runner
        async for event in self.runner.run_async(
            user_id="api_user", 
            session_id=session.id, # Using .id as previously fixed
            new_message=query_content
        ):
            # 1. Capture intermediate outputs from Parallel Agents
            if event.step_end:
                state = event.step_end.get("state", {})
                
                # Check for outputs from our research agents
                if state.get("sota_search"):
                    full_workflow_log["intermediate_results"]["sota_search"] = state["sota_search"]
                if state.get("dataset_search"):
                    full_workflow_log["intermediate_results"]["dataset_search"] = state["dataset_search"]
                if state.get("evaluation_search"):
                    full_workflow_log["intermediate_results"]["evaluation_search"] = state["evaluation_search"]
                    
            # 2. Capture final output from Strategy Agent
            if event.is_final_response and event.content:
                final_output = event.content.parts[0].text
                full_workflow_log["final_strategy"] = final_output
        
        # Save the full workflow log to a file
        log_file_path = LOGS_DIR / f"{session_id}_workflow_log.json"
        with open(log_file_path, "w") as log_file:
            json.dump(full_workflow_log, log_file, indent=4)
        # 3. Write the entire log to a JSON file
        try:
            # Ensure the logs directory exists
            LOGS_DIR.mkdir(exist_ok=True) 
            
            # Use the session_id to name the file
            log_file_path = LOGS_DIR / f"workflow_log_{session_id}.json"
            
            with open(log_file_path, 'w') as f:
                json.dump(full_workflow_log, f, indent=2)
            
            print(f"✅ Workflow log saved to: {log_file_path}")
            
        except Exception as e:
            print(f"❌ Failed to save workflow log: {e}")

        # Return the final strategy to the FastAPI endpoint
        return final_output
        

# Global Instance
orchestrator_instance = VisionOrchestrator()