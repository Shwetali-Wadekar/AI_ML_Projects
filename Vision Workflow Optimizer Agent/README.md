# 🤖 Vision Workflow Optimizer Agent

## 🌟 Project Overview

The **Vision Workflow Optimizer Agent** is a sophisticated **multi-agent system** designed to automatically generate a complete, technical project plan for any given computer vision task.

Built upon the Google Agent Development Kit (ADK) and FastAPI, this service orchestrates specialized research agents to provide an evidence-based strategy in seconds, drastically cutting down the manual research time for new Machine Learning projects.


### The Problem Solved

Traditional ML project initiation requires extensive manual research into:
1.  **State-of-the-Art (SOTA):** Which model architecture is best for the task (e.g., speed vs. accuracy)?
2.  **Data Sourcing (Datasets):** What publicly available datasets exist for training?
3.  **Evaluation Metrics:** What are the most appropriate technical and business metrics?

Our agent pipeline automates this entire discovery phase, delivering a definitive, **task-specific workflow plan** with citations and links.

## 🏗️ Architecture and Agent Pipeline

The system utilizes a **Sequential/Parallel** hybrid architecture.

| Agent Name | Type | Key Role |
| :--- | :--- | :--- |
| **OrchestratorAgent** | Agent | Converts the user's natural language query into a structured JSON `plan` (task, keywords). |
| **ParallelVisionResearch** | ParallelAgent | Simultaneously executes the SOTA Loop, Dataset, and Evaluation agents to gather information efficiently. |
| **StrategyAgent** | Agent | Synthesizes all parallel research outputs into a single, comprehensive, citation-heavy JSON strategy, ensuring **factual grounding**. |

### Key Technologies

* **Agent Framework:** Google Agent Development Kit (ADK)
* **LLM Core:** Gemini (`gemini-2.0-flash-lite` configured with retry logic)
* **Web API:** FastAPI (served via Uvicorn)
* **Observability:** Basic logging enabled for debugging agent execution steps.
* **Tools:** ADK built-in `Google Search` for web grounding.

---

## 🛠️ Setup and Installation

**Repo Layout**
```bash
vision_workflow_optimizer/
├─ README.md
├─ requirements.txt
├─ LICENSE
├─ app/
│ ├─ main.py # FastAPI orchestrator + endpoints
│ ├─ orchestrator.py # Orchestration logic calling agents
│ ├─ agents/
│ │ ├─ __init__.py
│ │ ├─ dataset_agent.py # Dataset Analyst Agent
│ │ ├─ strategy_agent.py # Model Strategy Agent
│ │ └─ eval_agent.py # Evaluation Interpreting Agent
│ ├─ tools/
│ │ ├─ __init__.py
│ └─ db/
│ ├─ __init__.py
│ └─ memory.py 
├─ logs/  # Runtime logs, including detailed agent audit trails.
└─ docs/
```
### Prerequisites

1.  Python 3.10+
2.  A [Gemini API Key](https://ai.google.dev/gemini-api/docs/api-key)
3.  Git installed

### Step 1: Clone the Repository

```bash
git clone [GITHUB_REPO_URL]
cd Vision-Workflow-Optimizer-Agent
```

### Step 2: Set up the Environment

```bash
# Create and activate the environment (Windows Example)
python -m venv Vision_Agent.venv
.\Vision_Agent.venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Create and activate the environment (Windows Example)
pip install -r requirements.txt
```

### Step 4: Configure API Key

1. Create a file named key.env inside the app/ directory.
2. Add your Gemini API Key to this file:

```bash
# File: app/key.env
GOOGLE_API_KEY="YOUR_ACTUAL_GEMINI_API_KEY_HERE"
```

## ▶️ Usage

1. **Start the Server**
    Run the application from the project root directory using the Python module flag (-m).
    ```bash
    python -m app.main
    ```
    The server will start with auto-reload enabled (for development) and run on port 8000: ```INFO: Uvicorn running on http://0.0.0.0:8000```

2. **Submit a Query and Test**
    1. Open your browser to the interactive documentation: ```http://127.0.0.1:8000/docs```

    2. Click on the ```/analyze``` POST endpoint.

    3. Click "Try it out".

    Enter a query and a session ID:

    ```JSON

    {
        "query": "Outline a project strategy for a system to perform robust prediction of pedestrian trajectories at complex intersections using onboard camera data.",
        "session_id": "pedestrian-project-alpha"
    }
    ```

    The server's console will show DEBUG logs from the agents (due to logging configuration), and the API response will contain the highly structured, evidence-based ML Strategy JSON.

3. **Auditing and Debugging**
    For every request, a detailed audit log of the user query and all intermediate agent outputs (SOTA, Dataset, Eval) is saved:

    Log Location: ``` ./logs/workflow_log_[session_id].json```

    This is invaluable for debugging the agent's decision-making process.

## 🚀 Future Work
This project can be extended with the following features:

1. **Human-in-the-Loop (HITL):** Integrate the ADK's long-running operations feature to allow an expert to pause the workflow and manually approve or modify the strategy before final execution.

2. **External Tool Integration:** Use OpenAPI tools to connect the agent to a live CV Model Zoo or a cloud service API for deployment estimates.

3. **Advanced Observability:** Integrate OpenTelemetry tracing to visualize the full pipeline execution in platforms like Google Cloud Trace.

## License  

This project is licensed under the MIT License.  
See the `LICENSE` file for details.  