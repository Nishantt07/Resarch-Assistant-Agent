from langchain_groq import ChatGroq
from mcp.mcp_client import call_tool
from utils.state import AgentState
from dotenv import load_dotenv
from utils.prompts import SYSTEM_POLICY
from langchain_core.messages import SystemMessage,HumanMessage


import os

load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)


def rag_agent(state:AgentState) -> AgentState:
    
    if "database" not in state["task_type"]:
        return state
    
    query = state['user_query']


    print(f"[DATABASE] Searching Pinecone for: {query}")

    retrieved_chunks =  call_tool("rag_search", {"query": query})

    prompt = f"""
    You are a helpful research assistant.
    Answer the user question based ONLY on the context provided below.
    If the context doesn't have enough information, say so clearly.
    
    Context from documents:
    {retrieved_chunks}
    
    User Question: {query}
    


    Answer:
    """

    response = llm.invoke([
        SystemMessage(content=SYSTEM_POLICY),
        HumanMessage(content=prompt)
    ])

    print(f"[DATABASE] Generated the Answer")

    state['rag_result'] = response.content
    return state