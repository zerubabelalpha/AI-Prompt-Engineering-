# AI Prompt Engineering - Learning & Testing 

A structured playground for exploring Large Language Models (LLMs), prompt engineering techniques, and future agentic implementations. This project currently focuses on basic API interactions via OpenRouter and terminal-based reasoning, we will update is while learning and testing.

##  Project Overview

This repository serves as a learning hub for mastering LLM integrations. It provides a clean, terminal-based interface to interact with various modelsthrough OpenRouter's unified API.

### Current Features
- **Terminal Chat Interface**: Interactive CLI for real-time model communication.
- **Rich Rendering**: Markdown support in the terminal for better readability of AI responses.
- **OpenRouter Integration**: Access to a wide range of free and paid models.
- **Structured Prompting**: Template-based request handling for consistent results.

## Tech Stack
- **Python**: Core logic.
- **OpenAI SDK**: API client for OpenRouter.
- **Rich**: Terminal formatting and markdown rendering.
- **Python-dotenv**: Secure environment variable management.

## Getting Started

### Prerequisites
- Python 3.11, above
- An [OpenRouter API Key](https://openrouter.ai/)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/zerubabelalpha/AI-Prompt-Engineering.git
   cd AI-Prompt-Engineering
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**:
   Create a `.env` file in the root directory and add your API key:
   ```env
   API_KEY=your_openrouter_api_key_here
   ```

### Usage

Run the basic API testing script:
```bash
python 01_basic_api.py
```

## Roadmap

The project is evolving from basic API testing to advanced agentic workflows:

- [done] **Phase 1: API Essentials** - Basic chat and parameter testing with prompt template.
- [ ] **Phase 2: Prompt Engineering** - Deep dive into few-shot, CoT, and system prompt optimization.
- [ ] **Phase 3: Agentic Concepts** - Implementing autonomous agents with reasoning capabilities.
- [ ] **Phase 4: Tool Calling & RAG** - Enabling models to use external tools and private data.
- [ ] **Phase 5: Multi-Agent Systems** - Orchestrating multiple specialized agents.


*Note: In this project i will test every thing and try different usecase to use llm*