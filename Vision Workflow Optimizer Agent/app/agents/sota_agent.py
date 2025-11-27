from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search



def create_sota_agent(model_name="gemini-2.0-flash-lite", retry_config=None):
    """
    SOTA Search Agent: Finds recent CV models for the user's task.
    """
    return Agent(
        name="SOTASearchAgent",
        description="Searches for state-of-the-art computer vision models and approachs relevant to the specified task.",
        model=Gemini(model=model_name, retry_options=retry_config),
        instruction="""
        Use the **google_search** tool to find 10-15 recent academic papers (SOTA models and approaches) related to the task keywords.
        Output ONLY a JSON list of objects: [{"model_name": "...", "description": "...", "year": "...", "url": "..."}]
        No conversational filler.
        """,
        tools=[google_search],
        output_key="sota_search"
    )