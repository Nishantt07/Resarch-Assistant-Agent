from langchain_groq import ChatGroq
from utils.state import AgentState
from dotenv import load_dotenv
import os
load_dotenv()


llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)


def synthesizer(state: AgentState) -> AgentState:

    query = state['user_query']

    collected_information = ""

    if state.get("rag_result"):
        collected_information+= f" --- from knowledge base ---\n{state['rag_result']}\n\n"

    if state.get("news_result"):
        collected_information+= f" --- from latest news ---\n{state['news_result']}\n\n"

    if state.get("weather_result"):
        collected_information+= f" ---from weather result ---\n{state['weather_result']}\n\n"

    if state.get("web_search_result"):
        collected_information+= f" ---from web search result ---\n {state['web_search_result']}\n\n"


    if not collected_information:
        state['final_answer'] = "I am not able to find any relevant information. Please try again"



    prompt = f"""
    You are a helpful research assistant. You have received information from 
    multiple sources. Combine them into ONE clear, well-structured answer 
    for the user. Do not mention the sources separately, just give a unified answer.
    
    User Question: {query}
    
    Information collected:
    {collected_information}
    
    Final unified answer:
    """


    response = llm.invoke(prompt)

    print("[Synthesizer] Final Answer Ready")

    state['final_answer'] = response.content
    return state
