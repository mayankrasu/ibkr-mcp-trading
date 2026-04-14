# IBKR MCP 🚀

A Model Context Protocol (MCP) based trading interface for Interactive Brokers (IBKR) TWS API, enabling natural language driven trading workflows.

---

## 🎯 Overview

This project demonstrates how to build an end-to-end trading system that translates **natural language instructions into executable IBKR API calls** using an MCP architecture.

It is designed as a **learning-focused repository** for building real-world trading infrastructure step by step.

---

## ✨ Features

- 🧠 Natural Language → Trading Execution (via LLM)
- 🔌 MCP-based tool orchestration layer
- 📊 Market scanners (volume, gainers, losers)
- 📈 Historical data retrieval
- 📡 Real-time market data (console-based)
- 🧾 Fundamentals extraction (parsed from XML)
- 💼 Account summary & PnL
- 💰 Order placement (market & limit)
- ⚙️ Strategy execution framework
- 🖥️ Streamlit chatbot UI

---

## 🏗️ Architecture
User Input (NL)
↓
LLM Parser (DeepSeek)
↓
MCP Server (Tool Routing)
↓
IBKR Service Layer
↓
TWS / IB Gateway API
---

## 📦 Installation

```bash
git clone <your-repo-url>
cd ibkr_mcp
pip install -e .
```

## 🔑 Environment Setup
`pip install -r requirements.txt`
Create a `.env` file in the project root and add your deepseek API key as a variable
`DEEPSEEK_API_KEY=your_api_key`


## Running the Applications
1. Console Interface (Recommended for Full Functionality)
`python examples/nl_testing.py`

Use this for:

- Streaming market data
- Debugging
- Full control

2. Streamlit Chat UI
`streamlit run app.py`

Use this for:

- ChatGPT-style interface
- Table rendering for results
- Easy interaction for non-technical users


