# Ultra-Advanced Autonomous Digital Paralegal

An enterprise-grade, Multi-Agent AI system designed to autonomously ingest, process, and analyze legal contracts using advanced OpenClaw-style Agent orchestration and Server-Sent Events (SSE) streaming.

## 🚀 Architecture Highlights

- **Planner Agent (Brain)**: Evaluates state and coordinates the Swarm.
- **Legal Agent**: Executes high-precision prompt templates against specific clauses using Async Generative flows.
- **Memory Agent**: Embeds long-term semantic contract context via `ChromaDB`.
- **Report Agent**: Synthesizes agent traces and LLM outputs into a unified JSON structure.
- **Full-Stack Streaming**: Streams real-time `LangChain` tokens and Planner trace events to a `Framer Motion` React Dashboard.

## 🛠 Tech Stack

- **Backend**: FastAPI, Python 3.10+, OpenAI (`gpt-4o-mini`), LangChain, ChromaDB
- **Frontend**: React 18, Framer Motion, Axios
- **Protocols**: SSE (Server-Sent Events) for real-time agent output

## ⚡ Quick Start & Deployment

### 1. Configure the AI API Key

```bash
cp .env.example .env
# Edit .env to add your OPENAI_API_KEY
```

### 2. Start the Agent Backend Swarm

```bash
pip install -r requirements.txt
uvicorn api.main:app --reload --port 8000
```

_(Runs on http://127.0.0.1:8000)_

### 3. Start the Advanced Dashboard

```bash
cd frontend/react-dashboard
npm install
npm start
```

_(Runs on http://localhost:3000)_

## 🧪 Testing the Website

1. A **sample risky legal contract** named `sample_risky_contract.pdf` has been generated for you in the root folder.
2. Open your browser to [http://localhost:3000](http://localhost:3000).
3. Click **Upload Legal Contract** and select `sample_risky_contract.pdf`.
4. Click **Launch Core Agents** and watch the real-time reasoning and SSE stream tracing in the UI!

> **Troubleshooting**: If you see a `Connection failed` or `System Error` in the UI trace log after uploading, verify that your `.env` contains a valid OpenAI API key and that the Python backend terminal shows no `401 Unauthorized` errors.
