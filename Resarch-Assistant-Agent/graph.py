from langgraph.graph import StateGraph, END
from utils.state import AgentState
from agents.api_agent import api_agent
from agents.orchestrator import  orchestrator
from agents.rag_agent import rag_agent
from agents.synthesizer import synthesizer
from agents.web_search_agent import web_search_agent


def build_graph():

    graph = StateGraph(AgentState)

    graph.add_node("orchestrator",orchestrator) 
    graph.add_node("rag_agent",rag_agent)
    graph.add_node("web_search_agent",web_search_agent)
    graph.add_node("api_agent",api_agent)
    graph.add_node("synthesizer",synthesizer)

    graph.set_entry_point("orchestrator")

    graph.add_edge("orchestrator","rag_agent")
    graph.add_edge("rag_agent","web_search_agent")
    graph.add_edge("web_search_agent","api_agent")
    graph.add_edge("api_agent","synthesizer")
    graph.add_edge("synthesizer", END)

    app = graph.compile()
    return app  #RETURNING THE COMPILED GRAPH