import subprocess
import time
import sys
import os
from dotenv import load_dotenv

load_dotenv()

from graph import build_graph
from tools.rag_tool import store_documents
from utils.state import AgentState


def start_mcp_server():
    print('Starting MCP Server...')

    process = subprocess.Popen(
        ["uvicorn", "mcp.mcp_server:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.DEVNULL,  
        stderr=subprocess.DEVNULL
    )
    time.sleep(5)  
    print("[System] MCP Server running on http://localhost:8000 ")
    return process

def load_sample_documents():
    print("[System] Loading document into Pinecone")


    sample_docs = [
        "Nishant is a developer focused on building practical AI-powered and full-stack applications. He works with technologies like LangChain, FastAPI, React, and modern LLM APIs to create scalable and modular systems.",
        "Nishant has experience developing conversational AI systems, RAG-based applications, and API-driven services. He emphasizes clean architecture, structured outputs, and proper validation before deployment.",
        "He understands core AI engineering concepts such as vector embeddings, state management, multi-agent workflows, and retrieval systems, ensuring that his solutions are technically strong and production-ready.",
        "In addition to AI development, Nishant builds responsive web applications using HTML, CSS, JavaScript, and React. He focuses on modular code structure and efficient state handling.",
        "Nishant is particularly interested in cloud computing, DevOps practices, and scalable AI infrastructure. He experiments with multi-LLM systems and cost-efficient inference strategies using providers like Groq and OpenAI.",
        "He approaches development with a problem-solving mindset, continuously improving his understanding of system design, API architecture, and real-world AI deployment."
    ]


    result  = store_documents(sample_docs)

    print(f'[System] {result}')


def run_agent(query: str , graph) -> str:

    initial_state: AgentState = {   ## Creating initial state dictionary following AgentState structure
        "user_query": query,
        "task_type": [],
        "rag_result": None,
        "web_search_result": None,
        "news_result": None,
        "weather_result": None,
        "final_answer": None,
        "error": None

    }

    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}")


    final_state = graph.invoke(initial_state) #CALLING COMPILED GRAPH WITH THE INITIAL STATE BECAUSE GRAPH TAKES STATE AND RETURN A STATE

    return final_state['final_answer'] #FETCHING THE STATE OUT OF STATE


if __name__ == "__main__":

    mcp_process = start_mcp_server()

    print("\n[System] Do you want to load sample documents into Pinecone?")
    print("(Type 'yes' if first time running, 'no' if already loaded)")
    load_docs = input("Your choice: ").strip().lower()

    if load_docs == "yes":
        load_sample_documents()



    print("\n Building Agent graph")
    graph = build_graph()   #GRAPH VARIABLE STORES THE COMPILED GRAPH
    print("[SYSTEM] Agent Graph Ready")

    print("\n" + "="*60)
    print("🔬 Research Assistant Agent is Ready!")
    print("="*60)
    print("You can ask about:")
    print("  → Concepts & definitions (uses your Pinecone documents)")
    print("  → Latest news on any topic")
    print("  → Weather in any city")
    print("  → Current events (web search)")
    print("\nType 'quit' to exit\n")


    while True:
            try:
                user_input = input("You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() == "quit":
                    print("[System] Shutting Down")
                    mcp_process.terminate()
                    sys.exit(0)
                    

                answer = run_agent(user_input , graph)  #SENDING THAT COMPILED GRAPH AND THE USER INPUT , TAKING ANSWER IN RETURN
                print(f'\n Agent: {answer}') #PRINTING THE FINAL ANSWER IN RETURN

            except KeyboardInterrupt:
                print("\n[System] Shutting down...")
                mcp_process.terminate()
                sys.exit(0)

            except Exception as e:
                print(f"[Error] Something went wrong: {str(e)}")


        










