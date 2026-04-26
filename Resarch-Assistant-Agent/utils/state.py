from typing import TypedDict,List,Optional

class AgentState(TypedDict):
    user_query: str
    task_type: List[str]


    rag_result: Optional[str]
    web_search_result: Optional[str]
    news_result: Optional[str]
    weather_result: Optional[str]


    final_answer: Optional[str]
    error: Optional[str]

    