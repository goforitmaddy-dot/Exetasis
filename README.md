# Exetasis

> **AI-Powered Workplace Intelligence Platform (Hackathon MVP Foundation)**

Exetasis combines a multi-agent LangGraph backend analyzing workplace dynamics with an interactive React + Three.js 3D Digital Twin visualization.

---

## 🏛 Architecture Overview

- **Backend (`backend/app`)**:
  - **FastAPI**: Asynchronous web framework exposing REST APIs and WebSocket streams.
  - **Database Layer**: SQLite + `aiosqlite` with SQLAlchemy 2.0 ORM and Repository pattern (`routes -> services -> repositories/agents`).
  - **Agents & Orchestration**: 8 specialized workplace intelligence agents wired into a LangGraph `StateGraph`:
    1. `workplace_architect`
    2. `workplace_configuration`
    3. `contribution`
    4. `fairness`
    5. `culture`
    6. `environment`
    7. `reward`
    8. `accountability`
  - **Local LLM Engine**: Open-weight models served locally via Ollama or local/AMD-hosted vLLM (OpenAI/Anthropic SDKs are strictly disallowed). Optional Gemini fallback disabled by default.
  - **Event Ingestion Adapters**: Modular adapters for Slack, GitHub, and Google Calendar (STUBs).
  - **Digital Twin WebSocket**: Real-time push of spatial state and event telemetry to the 3D twin canvas.

- **Frontend (`frontend/src`)**:
  - **React 18 + Vite + TypeScript**: Modern single-page app structure.
  - **Three.js & React Three Fiber (@react-three/fiber, @react-three/drei)**: Interactive 3D workplace twin showing department clusters, desk nodes, and avatar status indicators.
  - **Zustand**: Reactive state management handling twin node positioning and real-time event logs.
  - **Tailwind CSS**: Sleek dark-mode dashboard styling with Lucide icons.

---

## 🚀 Quickstart

### Prerequisites
- Python 3.12+
- Node.js 18+ and npm
- (Optional) [Ollama](https://ollama.ai/) running locally: `ollama run llama3.2`

### Backend Setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest

# Start backend server
uvicorn app.main:app --reload --port 8000
```
FastAPI interactive docs will be available at [http://localhost:8000/docs](http://localhost:8000/docs).

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Frontend web dashboard will be available at [http://localhost:5173](http://localhost:5173).

---

## 📁 Repository Layout
```
Exetasis/
├── backend/
│   ├── app/
│   │   ├── api/routes/          # REST API endpoints
│   │   ├── core/                # Configuration and logging
│   │   ├── db/
│   │   │   ├── models/          # SQLAlchemy ORM models
│   │   │   └── repositories/    # Database repository access layer
│   │   ├── schemas/             # Pydantic schemas for IO validation
│   │   ├── services/
│   │   │   └── llm/             # Ollama / vLLM client factory
│   │   ├── agents/              # 8 workplace agents with external prompts/
│   │   ├── orchestration/       # LangGraph multi-agent StateGraph
│   │   ├── events/adapters/     # Workplace event ingestion adapters (STUB)
│   │   ├── websocket/           # Digital Twin live streaming server
│   │   └── main.py              # Application entry point
│   ├── tests/                   # Pytest test suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable UI widgets
│   │   ├── pages/               # Top-level view routes
│   │   ├── features/            # Feature domains (dashboard, agents, twin)
│   │   ├── digital-twin/        # Three.js 3D canvas and meshes
│   │   ├── services/            # REST and WebSocket client
│   │   ├── store/               # Zustand stores
│   │   ├── hooks/               # Custom lifecycle hooks
│   │   ├── types/               # TypeScript interfaces
│   │   └── lib/                 # Shared utilities
│   ├── package.json
│   └── vite.config.ts
├── .env.example
├── .gitignore
└── README.md
```

---

## 🔒 Constraints & Rules
- All stubbed methods and mocks are marked with `STUB`.
- Prompts are strictly separated in `prompts/*.md` markdown files.
- Layering boundary is strictly enforced: `routes` never perform DB operations or agent reasoning directly.
