from langchain_groq import ChatGroq
from utils.state import AgentState
from mcp.mcp_client import call_tool
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from utils.prompts import SYSTEM_POLICY

import os

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def web_search_agent(state:AgentState) -> AgentState:

    if "web_search" not in state['task_type']:
        return state
    
    query = state['user_query']

    print(f"\n[Web Search Agent] Searching web for: {query}")

    search_results = call_tool("web_search",{"query": query})
    


    prompt = f"""
    You are a research assistant. Summarize the following web search results
    to directly answer the user's question. Be concise and accurate.
    
    Web Search Results:
    {search_results}
    
    User Question: {query}
    
    Summary:
    """

    response = llm.invoke([
        SystemMessage(content=SYSTEM_POLICY),
        HumanMessage(content=prompt)
    ])

    print(f"[WEB SEARCH AGENT] Summary Generated")

    state["web_search_result"] = response.content
    return state








