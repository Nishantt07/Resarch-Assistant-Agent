from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.news_tool import get_news
from tools.rag_tool import rag_search
from tools.tavily_tool import web_search
from tools.weather_tool import get_weather


app = FastAPI(title="MCP Tool Server")

class ToolRequest(BaseModel):
    tool_name: str
    parameters: dict
    

TOOL_REGISTRY = {
    "get_news" : get_news,
    "rag_search" : rag_search,
    "web_search" : web_search,
    "get_weather" : get_weather
}


@app.get("/health")
def health_check():
    return{
        "status": "running",
        "available_tools": list(TOOL_REGISTRY.keys())
    }


@app.post("/call-tool")
def call_tool(request: ToolRequest):
    if request.tool_name not in TOOL_REGISTRY:
        raise HTTPException(
            status_code = 404,
            detail = f'Tool {request.tool_name} not found. Available tools are {list(TOOL_REGISTRY.keys())}'
        )
    
    try:

        tool_function = TOOL_REGISTRY[request.tool_name]
        result = tool_function(**request.parameters)

        return{
            "tools": request.tool_name,
            "result": result,
            "status": "success"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail= f'Tool execution failed: {str(e)} '
        )

    




