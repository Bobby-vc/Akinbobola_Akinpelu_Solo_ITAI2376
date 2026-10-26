# AI Investment Multi-Agent System

**Akinbobola Akinpelu**

ITAI 2376 — Professor McManus

---
Demo: https://drive.google.com/file/d/1VLG0AVz0deRrmIlhUtg4bDtiqcClM9aq/view?usp=drive_link

## Overview

A dual-agent AI system that combines natural language understanding with quantitative analysis to educate users about the stock market and execute paper trades on their behalf. The system bridges the gap between learning platforms and trading apps by doing both in a single pipeline.

- **Agent 1 — The Advisor**: Accepts a user's investment question, fetches live price data and recent news headlines, performs sentiment analysis, and generates a plain-language recommendation tuned to the user's experience level.
- **Agent 2 — The Trader**: Receives the Advisor's trade signal, checks the current portfolio, and executes a paper trade via the Alpaca Markets API if confidence is sufficient.

The two agents communicate through a shared task pipeline managed by CrewAI, mirroring how real financial firms separate research and execution desks.

---

## Architecture

```
User Input (question, ticker, experience level)
        |
        v
Agent 1: Advisor (GPT-4o)
  - Tools: Get Stock Price Data, Get Stock News (yfinance)
  - Outputs: Sentiment summary, recommendation, TRADE SIGNAL
        |
        v
Agent 2: Trader (GPT-4o)
  - Tools: Check Portfolio, Execute Paper Trade (Alpaca API)
  - Outputs: Order confirmation or HOLD justification
        |
        v
trade_report.md (saved to project root)
```

---

## Deep Learning Connections

This project directly applies several deep learning concepts from ITAI 2376:

**Transformers & Self-Attention**
Both agents are powered by GPT-4o, a large language model built on the Transformer architecture. The self-attention mechanism allows the model to weigh relationships across the entire context window, connecting a user's question, live price data, and news headlines simultaneously to generate a coherent, context-aware response. This is the core of why the Advisor can calibrate its recommendation to a beginner vs. an advanced investor using the same underlying data.

**LLM Reasoning Loop (Plan → Act → Observe → Respond)**
The agents follow the ReAct (Reasoning + Acting) pattern, which maps directly to the reasoning loop covered in the course. For each query, the Advisor plans what data it needs, acts by calling the yfinance tools, observes the returned prices and headlines, and then responds with a structured recommendation and trade signal. The Trader repeats the same loop; checking the portfolio, deciding whether confidence is high enough, and acting on or holding the signal. CrewAI's task pipeline enforces this loop explicitly.

**Prompt Engineering as Model Steering**
Agent behavior is defined through carefully structured system prompts in `agents.yaml`. This is applied prompt engineering, using natural language instructions to constrain the model's role, tone, and output format without any weight updates. The Advisor is steered to produce a sentiment summary, a plain-language recommendation, and a structured trade signal in a single response. This reflects how Transformer models are guided through instruction-following rather than fine-tuning for every use case.

**Embeddings & Semantic Understanding**
Internally, GPT-4o converts all inputs: user questions, news headlines, and price summaries, into high-dimensional embeddings before processing. This enables the model to recognize semantic similarity across different phrasings of the same intent, such as treating "Is NVDA worth buying?" and "Should I invest in Nvidia?" as equivalent queries. While embeddings are not explicitly exposed in this project (no ChromaDB or vector store), they are the mechanism behind the model's language understanding at every step.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| CrewAI | Multi-agent orchestration |
| OpenAI GPT-4o | Core LLM for both agents |
| yfinance | Live stock price data and news headlines |
| Alpaca Markets API | Paper trade execution (simulated, no real money) |
| Python-dotenv | Secure API key management |

---

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager
- OpenAI API key
- Alpaca Markets paper trading account (free at [alpaca.markets](https://alpaca.markets))

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

**2. Install dependencies**
```bash
uv sync
```

**3. Set up environment variables**

Create a `.env` file in the project root with the following keys:
```
OPENAI_API_KEY=your_openai_key_here
APCA_API_KEY_ID=your_alpaca_key_here
APCA_API_SECRET_KEY=your_alpaca_secret_here
APCA_API_BASE_URL=https://paper-api.alpaca.markets
```

Your Alpaca API keys can be found in your Alpaca dashboard under API Keys. Use the paper trading keys, not live trading.

---

## Running the System

```bash
crewai run
```

The system will prompt you for:
- Your investment question (e.g. "Is NVDA a good buy right now?")
- The stock ticker (e.g. NVDA)
- Your experience level (beginner / intermediate / advanced)

The Advisor will then fetch live data, analyze it, and pass a trade signal to the Trader. If the signal meets the confidence threshold, the Trader will execute a paper order on Alpaca. A full trade report is saved to `trade_report.md` after each run.

---

## Project Structure

```
first_ai_agents/
├── src/first_ai_agents/
│   ├── config/
│   │   ├── agents.yaml        # Agent roles, goals, and backstories
│   │   └── tasks.yaml         # Task descriptions and agent assignments
│   ├── tools/
│   │   └── custom_tool.py     # yfinance and Alpaca tool definitions
│   ├── crew.py                # Crew assembly and agent/task wiring
│   └── main.py                # Entry point with user input prompts
├── trade_report.md            # Auto-generated after each run
├── pyproject.toml
└── .env                       # API keys (not committed to repo)
```

---

## Disclaimer

This system is built for educational purposes only as part of a course project. All trading is simulated using Alpaca's paper trading sandbox. No real money is involved. This is not licensed financial advice.
