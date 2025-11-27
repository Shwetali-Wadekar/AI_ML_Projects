from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from app.tools.metrics_parser import MetricsParser

def create_eval_agent(model_name="gemini-2.0-flash-lite", retry_config=None):
    
    """
    Evaluation Agent: Summarizes key evaluation metrics for the task.
    """

    return Agent(
        name="EvaluationAgent",
        description="Identifies and summarizes key evaluation metrics relevant to the specified computer vision task.",
        model=Gemini(model=model_name, retry_options=retry_config),
        instruction="""
        Use the **google_search** tool to find the most important evaluation metrics specific to the task keywords.
        Produce a JSON list containing keys 'metric', 'description', and 'formula'.
        Output ONLY a JSON list: [{"metric": "...", "description": "...", "formula": "..."}]
        No conversational filler.
        """,
        tools=[google_search],
        output_key="evaluation_search"
    )
    return Agent(
        name="EvaluationAgent",
        model=genai.Gemini(
            model=model_name,
            retry_options=retry_config
        ),
        instruction="""
        You are the Evaluation Interpreting Agent. Use Google Search for 'most important evaluation metrics for the given CV task'.
        Produce a JSON object containing keys 'metric',description','task_applicability','formula','usage_notes'.
        
        [
          {
            "metric": "mIoU",
            "description": "...",
            "task_applicability": "semantic segmentation",
            "formula": "...",
            "usage_notes": "..."
          }
        ]
        Also You take normalized metrics and explain failure modes and provide experiment suggestions.
        ONLY output JSON. No extra text.
        """,
        tools=[google_search],
        output_key="evaluation_search"
    )


