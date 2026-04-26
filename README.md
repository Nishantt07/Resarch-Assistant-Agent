🔬 Research Assistant Agent
A multi-agent AI research assistant that intelligently routes user queries across specialized agents for document retrieval, web search, and real-time data fetching — powered by LangGraph, Groq, Pinecone and MCP.

📌 What It Does
The Research Assistant Agent understands what type of question you are asking and automatically decides which tools and agents to use to find the best answer.
User QueryWhat Happens"What is machine learning?"RAG Agent searches Pinecone documents"Latest news on ChatGPT?"Web Search (Tavily) + NewsAPI"Weather in Delhi today?"OpenWeatherMap API"Explain transformers and today's AI news"RAG + News Agent both run together

🏗️ Architecture
User Query
    ↓
Orchestrator Agent (LangGraph)
    ↓           ↓            ↓
RAG Agent   Web Search   API Agent
(Pinecone)  (Tavily)     (News + Weather)
    ↓           ↓            ↓
        Synthesizer Agent
        (combines all results)
              ↓
        Final Answer ✅
All tools are managed through a Model Context Protocol (MCP) server, and agents communicate through Agent-to-Agent (A2A) shared state via LangGraph.

🧩 Tech Stack
TechnologyPurposePythonCore languageLangChainAgent and chain frameworkLangGraphMulti-agent workflow orchestrationGroq (LLaMA3-8B)Fast LLM inferencePineconeVector database for RAGSentence TransformersText embedding (all-MiniLM-L6-v2)FastAPIMCP serverTavily APIReal-time web searchNewsAPILatest news headlinesOpenWeatherMap APILive weather datahttpxAsync HTTP client for MCPpython-dotenvEnvironment variable management

📁 Project Structure
research-assistant-agent/
├── main.py                      # Entry point + conversation loop
├── graph.py                     # LangGraph workflow
├── .env                         # API keys
├── requirements.txt             # Dependencies
│
├── agents/
│   ├── orchestrator.py          # Routes queries to right agents
│   ├── rag_agent.py             # Searches Pinecone documents
│   ├── web_search_agent.py      # Searches internet via Tavily
│   ├── api_agent.py             # Fetches news and weather
│   └── synthesizer.py           # Combines all results (A2A)
│
├── mcp/
│   ├── mcp_server.py            # Central tool registry (FastAPI)
│   └── mcp_client.py            # Agents call tools through here
│
├── tools/
│   ├── tavily_tool.py           # Web search tool
│   ├── news_tool.py             # NewsAPI tool
│   ├── weather_tool.py          # OpenWeatherMap tool
│   └── rag_tool.py              # Pinecone RAG tool
│
└── utils/
    ├── state.py                 # Shared AgentState between agents
    └── prompts.py               # All LLM prompts

⚙️ How It Works
1. Shared State
All agents share a common AgentState dictionary managed by LangGraph. Each agent reads from and writes to this state, enabling seamless Agent-to-Agent (A2A) communication.
2. MCP Server
All tools (Tavily, NewsAPI, Weather, RAG) are registered in a central FastAPI-based MCP server. Agents never import tools directly — they call tools through the MCP client using standardized HTTP requests.
3. Query Routing
The Orchestrator agent sends the user query to Groq LLM which classifies it and returns a list of tools needed (e.g. rag,news). LangGraph then activates only the relevant agents.
4. Agent Flow
User types query
      ↓
main.py → graph.invoke(initial_state)
      ↓
orchestrator_agent → fills task_type in state
      ↓
rag_agent → searches Pinecone → fills rag_result
      ↓
web_search_agent → searches web → fills web_search_result
      ↓
api_agent → fetches news/weather → fills news/weather_result
      ↓
synthesizer_agent → reads all results → fills final_answer
      ↓
User sees final_answer ✅

🔑 API Keys Required
APIGet It AtGROQ_API_KEYgroq.comTAVILY_API_KEYtavily.comNEWSAPI_KEYnewsapi.orgOPENWEATHER_API_KEYopenweathermap.orgPINECONE_API_KEYpinecone.io

🚀 Getting Started
1. Clone the repository
bashgit clone https://github.com/yourusername/research-assistant-agent.git
cd research-assistant-agent
2. Install dependencies
bashpip install -r requirements.txt
3. Set up environment variables
Create a .env file in the root directory:
envGROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
NEWSAPI_KEY=your_newsapi_key
OPENWEATHER_API_KEY=your_openweather_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=research-agent
4. Set up Pinecone Index
Go to pinecone.io and create an index with:
Index Name:  research-agent
Dimensions:  384
Metric:      cosine
5. Run the project
bashpython main.py
When prompted, type yes to load sample documents into Pinecone on first run.

💬 Example Conversation
You: What is RAG?
🤖 Agent: RAG stands for Retrieval Augmented Generation...
          [answer from your Pinecone documents]

You: Latest news on artificial intelligence
🤖 Agent: Here are the latest AI developments...
          [summarized from NewsAPI + Tavily]

You: What is the weather in Mumbai?
🤖 Agent: Current weather in Mumbai:
          Temperature: 32°C, Humidity: 78%...

🔄 Agent Responsibilities
AgentFileJobOrchestratoragents/orchestrator.pyReads query, decides which agents runRAG Agentagents/rag_agent.pySearches Pinecone for relevant document chunksWeb Search Agentagents/web_search_agent.pySearches internet using TavilyAPI Agentagents/api_agent.pyFetches live news and weatherSynthesizeragents/synthesizer.pyCombines all results into one final answer

📦 Key Concepts Used
RAG (Retrieval Augmented Generation) — Documents are converted to vectors using Sentence Transformers and stored in Pinecone. When a user asks a question, the most relevant document chunks are retrieved and passed to the LLM for accurate, grounded answers.
MCP (Model Context Protocol) — A centralized FastAPI server acts as a tool registry. All agents call tools through a standardized HTTP interface instead of importing them directly, keeping the system modular and maintainable.
A2A (Agent-to-Agent Communication) — Agents communicate through shared LangGraph state. Each agent writes its result to the state, and the Synthesizer reads all results to produce the final combined answer.
LangGraph — Manages the entire agent workflow as a directed graph. Defines nodes (agents) and edges (connections), handles state passing and controls execution order.

📋 Requirements
Python 3.10+
langchain
langchain-groq
langchain-community
langchain-pinecone
langgraph
tavily-python
pinecone-client
sentence-transformers
newsapi-python
requests
python-dotenv
fastapi
uvicorn
httpx

🙋 Author
Built as a learning project to understand multi-agent AI systems, RAG pipelines, MCP architecture and LangGraph orchestration.

📄 License
MIT License — feel free to use and modify for your own projects.
