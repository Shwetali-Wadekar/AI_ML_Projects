from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from app.tools.dataset_inspector import DatasetInspector

def create_dataset_agent(model_name="gemini-2.0-flash-lite", retry_config=None):
    return Agent(
        name="DatasetAgent",
        description="Searches for datasets relevant to the specified computer vision task.",
        model=Gemini(model=model_name, retry_options=retry_config),
        instruction="""
        You are a Dataset Analyst. Use the **google_search** tool to find datasets that could be used for the given task keywords.
        Output ONLY a JSON object: {"recommended_datasets": [...], "dataset_summary": "..."}
        The 'recommended_datasets' list should contain objects with 'name', 'url', 'class names', and 'class wise size'.
        No conversational filler (e.g., "Okay, I will help...").
        """,
        tools=[google_search],
        output_key="dataset_search"
    )


