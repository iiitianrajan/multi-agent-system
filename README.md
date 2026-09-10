# 🔬 ResearchMind

**A multi-agent AI research pipeline that searches, reads, writes, and critiques — turning a single topic into a polished, evaluated research report.**

Built with **Python · LangChain · Google Gemini · Tavily · Streamlit**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C)](https://www.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**[Live Demo](https://multi-agent-system-4zvbci6jsqi5y37dpswjnd.streamlit.app)** · 
---

## Overview

Most AI research tools make a single LLM call and hope for the best. **ResearchMind splits the job into four specialized agents**, each responsible for one stage of the research process — search, extraction, writing, and quality review — producing a more reliable and inspectable output than a single monolithic prompt.

```
Topic → Search Agent → Reader Agent → Writer Chain → Critic Chain → Report + Feedback
```

Enter a topic, and ResearchMind returns a structured Markdown report **plus a critical review of its own output**, with every intermediate step visible along the way.

---

## Why This Project Matters

This project demonstrates practical, end-to-end experience with the skills modern AI engineering roles look for:

| Area | Demonstrated Skill |
|---|---|
| **Multi-agent orchestration** | Decomposing a task into specialized, sequential agents rather than one large prompt |
| **Tool-augmented LLMs** | Integrating live web search (Tavily) into an agent's reasoning loop |
| **LLM application development** | Building with LangChain and Google Gemini in a production-style pipeline |
| **Prompt engineering** | Distinct prompts tuned per agent role (search, extraction, writing, critique) |
| **Full-stack delivery** | Shipping a working, deployed, interactive UI — not just a notebook |
| **Software design** | Modular, extensible architecture that separates concerns cleanly |

---

## How It Works

```
                    ┌─────────────────┐
                    │   Research Topic │
                    └────────┬─────────┘
                             ▼
                    ┌─────────────────┐
                    │  01 Search Agent │  → Tavily web search
                    └────────┬─────────┘
                             ▼
                    ┌─────────────────┐
                    │  02 Reader Agent │  → Selects & scrapes best source
                    └────────┬─────────┘
                             ▼
                    ┌─────────────────┐
                    │ 03 Writer Chain  │  → Google Gemini drafts the report
                    └────────┬─────────┘
                             ▼
                    ┌─────────────────┐
                    │ 04 Critic Chain  │  → Reviews & scores the report
                    └────────┬─────────┘
                             ▼
                    ┌─────────────────┐
                    │  Report + Review │
                    └─────────────────┘
```

| Stage | Responsibility | Tool / Model |
|---|---|---|
| **Search Agent** | Finds recent, relevant information about the topic | Tavily |
| **Reader Agent** | Picks the best source and extracts deeper content | Web scraping |
| **Writer Chain** | Synthesizes findings into a structured report | Google Gemini |
| **Critic Chain** | Reviews the report and flags weaknesses | Google Gemini |

---

## Features

- 🔎 Live web search grounded in current information (not just model memory)
- 📄 Automatic source selection and content extraction
- ✍️ Structured, Markdown-formatted research reports
- 🧐 Built-in self-critique of the generated report
- 📊 Real-time pipeline status for each agent stage
- 🔍 Inspectable intermediate outputs (raw search & scraped content)
- ⬇️ One-click Markdown report download
- 🔐 Secrets managed via environment variables, never hardcoded

---

## Tech Stack

- **Language:** Python 3.12
- **LLM:** Google Gemini
- **Orchestration:** LangChain
- **Web Search:** Tavily
- **UI:** Streamlit, custom CSS

---

## Getting Started

### 1. Clone & set up environment

```bash
git clone https://github.com/YOUR_USERNAME/ResearchMind.git
cd ResearchMind
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API keys

Create a `.env` file in the project root (use `.env.example` as a template):

```env
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

| Variable | Purpose |
|---|---|
| `GEMINI_API_KEY` | Access to Google Gemini |
| `TAVILY_API_KEY` | Web search via Tavily |

> **Never commit real API keys.** Keep `.env` in `.gitignore`; commit `.env.example` instead. If a key is ever pushed by mistake, revoke and rotate it immediately.

### 3. Run the app

```bash
streamlit run app.py
```

---

## Project Structure

```
ResearchMind/
├── app.py              # Streamlit UI & pipeline orchestration
├── agents.py           # Search, Reader, Writer, Critic agent definitions
├── requirements.txt
├── .env.example
├── README.md
└── tests/
    └── test_agents.py
```

---

## Example Topics to Try

```
LLM agents 2025
CRISPR gene editing
Fusion energy progress
Recent advances in quantum computing
```

---

## Roadmap

- [x] Core 4-agent pipeline (Search → Read → Write → Critique)
- [x] Interactive Streamlit UI with live pipeline status
- [x] Markdown report export
- [ ] Parallel multi-source research
- [ ] Automatic citation generation
- [ ] Structured (JSON) report output
- [ ] Agent retry & error-handling improvements
- [ ] Persistent research history + user auth
- [ ] Docker deployment & CI/CD

---

## Testing

```bash
pytest
```

Coverage targets each agent independently — valid/invalid inputs, empty results, and failure handling for search, extraction, writing, and critique stages.

---

## Author

**Rajan Kumar**

[GitHub](https://github.com/iiitianrajan/multi-agent-system) · [LinkedIn](www.linkedin.com/in/rajan-kumar-b787382b9)

---


If you find this project useful, consider giving it a ⭐ on GitHub.
