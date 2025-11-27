import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / "key.env"
# Load environment variables from .env file
#load_dotenv("D:\Learning\5 day google Agent AI course\Capstone Project\Vision Workflow Optimizer Agent\app\key.env")
load_dotenv(ENV_FILE)
if os.getenv("GOOGLE_API_KEY"):
    print("✅ GOOGLE_API_KEY successfully loaded into environment.")
else:
    print("❌ GOOGLE_API_KEY is NOT set. Check key.env file content.")
          
# Set the root logger level to DEBUG to capture ADK's internal events
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

# We import the pre-configured Orchestrator instance from its module
# This ensures the agents and runner are initialized when the app starts.
from app.orchestrator import orchestrator_instance 

# 1. Define Request/Response Models
class UserRequest(BaseModel):
    """Pydantic model for the incoming API request."""
    # The query containing the computer vision task (e.g., "detect cracks in pavement")
    query: str
    # A session ID to maintain conversation state across multiple calls (useful for memory)
    session_id: str = "default_user"

class AnalysisResponse(BaseModel):
    """Pydantic model for the outgoing API response."""
    session_id: str
    # The final synthesized strategy returned by the SequentialAgent pipeline
    strategy_json: str 

# 2. Initialize FastAPI Application
# Note: The app object must be defined at the top level for Uvicorn to import it.
app = FastAPI(
    title="Vision Workflow Optimizer API",
    description="Orchestrates GenAI Agents to generate CV project strategies.",
    version="1.0.0"
)

# 3. Define API Endpoints

@app.get("/")
def read_root():
    """Simple health check endpoint."""
    return {"status": "active", "service": "Vision Workflow Optimizer"}

@app.post("/analyze", response_model=AnalysisResponse)
async def run_analysis(request: UserRequest):
    """
    Kicks off the Vision Workflow Agent pipeline (OrchestratorAgent -> Parallel Research -> StrategyAgent).
    """
    if not request.query or not os.environ.get("GOOGLE_API_KEY"):
        # Check for API key at runtime (since it's loaded in .env)
        raise HTTPException(
            status_code=500, 
            detail="GOOGLE_API_KEY not found or query is empty. Check your .env file."
        )
    
    try:
        # Pass the query and session_id to the Orchestrator instance
        result = await orchestrator_instance.process_query(
            user_query=request.query, 
            session_id=request.session_id
        )

        return {
            "session_id": request.session_id, 
            "strategy_json": result
        }
        
    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")
        # Return a generic error to the user, log the detailed error internally
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred during workflow execution: {e.__class__.__name__}"
        )


# 4. Programmatic Server Start
# This block allows you to run the file directly using 'python main.py' for development.
if __name__ == "__main__":
    # Ensure the code that creates the server process is protected by if __name__ == '__main__': 
    # This is crucial when using `reload=True` to prevent recursive spawning issues.
    uvicorn.run(
        "app.main:app", # Format: <module>:<app_instance_name>
        host="0.0.0.0", 
        port=8000, 
        reload=True,    # Use reload in development for file watching
        log_level="info"
    )