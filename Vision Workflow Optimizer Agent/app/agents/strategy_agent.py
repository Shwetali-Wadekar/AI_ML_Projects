from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.tools import load_memory



def create_strategy_agent(model_name="gemini-2.0-flash-lite", retry_config=None):
    """
    Strategy Agent: Synthesizes SOTA + dataset + metrics into a project plan.
    """

    return  Agent(
        name="StrategyAgent",
        description="Creates a comprehensive project strategy based on SOTA models, datasets, and evaluation metrics.",
        model=Gemini(
            model= model_name,
            retry_options=retry_config
        ),
        instruction="""
        You are a Machine Learning Strategist. Your goal is to synthesize the search results 
        from {sota_search}, {dataset_search}, and {evaluation_search} into a concrete, 
        task-specific workflow plan.

        ***CRITICAL RULE:*** Every section of the plan MUST be directly supported by, and cite, 
        the data provided in the input search results. DO NOT HALLUCINATE MODELS, DATASETS, or METRICS.

        Output ONLY the final JSON object defined below. The 'details' field in each section 
        MUST contain direct citations and specific links found in the search results.

        Output JSON structure:
        {
          "task_summary": "Synthesized summary of the project goal and key challenges.",
          "model_strategy": {
            "recommended_approach": "Appproached to be used based on SOTA search",
            "recommended_model": "Specific model name",
            "reasoning": "Explain why this model is suited for the task and the specific challenge based on the SOTA search.",
            "sota_paper_reference": "Name of the key paper from SOTA search.",
            "sota_paper_link": "URL from the SOTA search."
          },
          "dataset_plan": {
            "recommended_dataset": "Specific dataset name for thew given task.",
            "dataset_link": "URL from the dataset search.",
            "data_preparation_notes": "How to prepare this specific dataset (e.g., resize, annotation format) based on its summary."
          },
          "evaluation_strategy": {
            "primary_metric": "The most relevant metric for this task.",
            "metric_description": "Description and formula/context from the evaluation search.",
            "secondary_metric": "A second key metric or loss function.",
            "metric_link": "Link to documentation or paper explaining the metric."
          },
          "deployment_notes": "Synthesis of hardware/speed requirements from the model and dataset choices."
        }
        """,
         tools=[load_memory],
        output_key="final_strategy"
    )


