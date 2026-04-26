from langchain_groq import ChatGroq
from mcp.mcp_client import call_tool
from utils.state import AgentState
from dotenv import load_dotenv
import os
from langchain_core.messages import HumanMessage, SystemMessage
from utils.prompts import SYSTEM_POLICY
import re


load_dotenv()

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)


def api_agent(state: AgentState) -> AgentState:
    query = state['user_query']
    task_type = state["task_type"]

    if "news" in task_type:
        news_results = call_tool("get_news",{"query" : query})
        print(f"[DEBUG] News Results: {news_results}") 
        prompt = f"""
        Summarize these news articles to answer the user's question.
        Present the key headlines and important information clearly.
        
        News Articles:
        {news_results}
        
        User Question: {query}
        
        Summary:
        """

        response = llm.invoke([
            SystemMessage(content=SYSTEM_POLICY),
            HumanMessage(content=prompt)
        ])
        state["news_result"] = response.content
        print(f"[API AGENT] News Summary generated ")

    if "weather" in task_type:

        city_prompt = f"""
        Extract ONLY the city name from this query. Reply with just the city name, nothing else.
        Query: {query}
        City:
        """

        city_response = llm.invoke(city_prompt)
        weather_result = call_tool("get_weather" , {"city": city_response.content.strip()})

        state['weather_result'] = weather_result
        print(f"[API Agent] Weather data fetched.")
        
    return state
    










