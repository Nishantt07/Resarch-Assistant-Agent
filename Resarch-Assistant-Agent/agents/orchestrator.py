from langchain_groq import ChatGroq 
from dotenv import load_dotenv
from utils.state import AgentState
import os

load_dotenv()


llm = ChatGroq(
    api_key = os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

def orchestrator(state: AgentState) -> AgentState:
    query = state['user_query']
    prompt = f'You are a task router. Analyze the user query and decide which tools are needed. Always add database becuase in tools at first position and if the user ask about nishant then select the database tool only and no need to select any other tool.  User Query: {query} Available tools: - database: use when user asks about anything. - web_search: use when user asks about recent events, current information. - news: use when user asks about latest news, headlines, recent developments. - weather: use when user asks about weather of any city. Reply with ONLY a comma-separated list of tools needed. Example: rag,news  or  weather  or  rag,web_search,news. Your answer:'
    response = llm.invoke(prompt)

    tools_needed = [t.strip() for t in response.content.strip().split(",")]

    print(f"[Orchestrator] Query: {query}")
    print(f"[Orchestrator] Tools Needed:{tools_needed} ")

    state["task_type"] = tools_needed
    return state


