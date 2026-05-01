import httpx
import os


MCP_SERVER_URL = "http://localhost:8000"


def call_tool(tool_name: str , parameters: dict) -> str:

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.post(
                f'{MCP_SERVER_URL}/call-tool',
                json={
                    "tool_name":tool_name,
                    "parameters": parameters
                }
            )

            if response.status_code == 200:
                return response.json()["result"]
            else:
                return f"MCP Error: {response.json()['detail']}"
            

            
            
    except httpx.ConnectError:
        return "MCP Server is not running. Please start it first"
    
    except Exception as e:
        return f'MCP Client Error: {str(e)}'
    


def list_tools() -> list:
    try:  
        with httpx.Client() as client:
            response = client.get(f'{MCP_SERVER_URL}/health')
            return response.json()['available_tools']
    except:
        return[]
        
