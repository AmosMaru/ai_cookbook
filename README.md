## AI Cookbook (LangGraph Masterclass)

A collection of small, focused examples showing how to build with LangGraph/LangChain in Python and how to wire up an AI voice/chat frontend with Next.js and Hume.

### Repository layout
- `01_building_basic_chatbot_using_langgraph/`: Minimal LangGraph chatbot
- `02_building_apps_with_ai-models/hume-quickstart/`: Next.js voice/chat starter using Hume EVI
- `03_workflow_and_agent/`: Multiple LangGraph patterns (prompt chaining, tools, orchestrator, evaluator/optimizer, parallelization)

### Prerequisites
- **Python**: 3.13 (as specified in each module)
- **Node.js**: 18+ (for the Next.js app)
- Package manager options:
  - Python: `uv` recommended, or `pip + venv`
  - JS: `npm` (lockfile present) or `pnpm`

### Credentials and environment variables
- **OpenAI (Python modules)**
  - `OPENAI_API_KEY`: required by LangChain when using `init_chat_model("openai:gpt-4o-mini")`
  - Create a `.env` file in each Python module directory (01 and 03) as shown below.
- **Hume (Next.js app)**
  - `HUME_API_KEY`, `HUME_SECRET_KEY`: required on the server to fetch an access token
  - Create `.env.local` in the Next.js project directory as shown below.

Example `.env` (for Python modules 01 and 03):
```bash
OPENAI_API_KEY=sk-...your_key...
```

Example `.env.local` (for the Hume Next.js app):
```bash
HUME_API_KEY=...your_hume_api_key...
HUME_SECRET_KEY=...your_hume_secret_key...
```

## 01 — Basic Chatbot (LangGraph, Python)
Location: `01_building_basic_chatbot_using_langgraph/`

- Graph registry: `langgraph.json` exposes `basic_chatbot` → `graph/graph.py:graph`
- Dependencies: see `pyproject.toml`

Setup (uv):
```bash
cd /Users/jameskanyiri/LANGGRAPH_MASTERCLASS/ai_cookbook/01_building_basic_chatbot_using_langgraph
uv sync
# add your OpenAI key
printf "OPENAI_API_KEY=sk-..." > .env
```

Run (LangGraph Dev UI):
```bash
uv run langgraph dev
# A local inspector will open; select the graph and chat interactively
```

Alternative (pip + venv):
```bash
cd /Users/jameskanyiri/LANGGRAPH_MASTERCLASS/ai_cookbook/01_building_basic_chatbot_using_langgraph
python3.13 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .
# add your OpenAI key
printf "OPENAI_API_KEY=sk-..." > .env
langgraph dev
```

## 02 — Hume Voice/Chat (Next.js)
Location: `02_building_apps_with_ai-models/hume-quickstart/`

- Pages Router (Next 14)
- Requires server-side token fetch using your Hume credentials (see `pages/index.tsx`)

Setup and run:
```bash
cd /Users/jameskanyiri/LANGGRAPH_MASTERCLASS/ai_cookbook/02_building_apps_with_ai-models/hume-quickstart
# create env
printf "HUME_API_KEY=...\nHUME_SECRET_KEY=...\n" > .env.local
npm install
npm run dev
# open http://localhost:3000
```

Build and start:
```bash
npm run build
npm start
```

## 03 — Workflows and Agents (LangGraph, Python)
Location: `03_workflow_and_agent/`

Available graphs (from `langgraph.json`):
- `prompt_chaining` → `graph/prompt_chaining.py:graph`
- `parallelization` → `graph/parallelization.py:graph`
- `orchestrator` → `graph/orchestrator.py:graph`
- `evaluator_optimizer` → `graph/evaluator_optimizer.py:graph`
- `agent` → `graph/agent.py:graph`
- `example` → `graph/example.py:graph`
- `tools` → `graph/tools.py:graph`

Setup (uv):
```bash
cd /Users/jameskanyiri/LANGGRAPH_MASTERCLASS/ai_cookbook/03_workflow_and_agent
uv sync
printf "OPENAI_API_KEY=sk-..." > .env
```

Run (LangGraph Dev UI):
```bash
uv run langgraph dev
# Choose a graph from the inspector and test
```

Alternative (pip + venv):
```bash
cd /Users/jameskanyiri/LANGGRAPH_MASTERCLASS/ai_cookbook/03_workflow_and_agent
python3.13 -m venv .venv && source .venv/bin/activate
pip install -U pip
pip install -e .
printf "OPENAI_API_KEY=sk-..." > .env
langgraph dev
```

### Notebooks
- `01_building_basic_chatbot_using_langgraph/notebooks/basic_chatbot.ipynb`
- `03_workflow_and_agent/notebook/workflows_and_agent.ipynb`

Open in VS Code or Jupyter. If you use uv, the kernel is available via `ipykernel`; if needed, install a kernel name:
```bash
uv run python -m ipykernel install --user --name ai-cookbook
```

### Troubleshooting
- "Missing API key" (Python): ensure `.env` exists with `OPENAI_API_KEY` in the corresponding module folder.
- "Missing HUME_API_KEY/HUME_SECRET_KEY" (Next.js): ensure `.env.local` is present in the Next.js app folder.
- Python version mismatch: both modules target Python 3.13; confirm `python3.13 --version`.
- Port conflicts: change port via `PORT=xxxx npm run dev` (Next.js) or stop existing processes.

### License
Educational examples only. Review licenses for LangChain, LangGraph, and Hume SDKs before production use.

