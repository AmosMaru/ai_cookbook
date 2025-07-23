from typing import Annotated
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from langgraph.graph.message import add_messages
from typing import TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import AnyMessage

open_ai_llm = init_chat_model("openai:gpt-4o-mini")

google_genai_llm = init_chat_model("google_genai:gemini-2.0-flash")


class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    user_intent: str
    
class UserIntent(BaseModel):
    intent: str = Field(description="Classify the user query into one of the following categories: weather, news")
    
def user_intent(state: State)-> State:
    #Get the current messages
    messages = state["messages"]
    
    user_query = messages[-1]
    
    PROMPT = """
    You are a helpful assistant that can classify user queries into one of the following categories: weather, news.
    {user_query}
    """
    
    system_instruction = PROMPT.format(user_query=user_query)
    
    
    
    messages = [
        {"role": "system", "content": system_instruction}
    ]
    
    response = open_ai_llm.with_structured_output(UserIntent).invoke(messages)
    
    return {"user_intent": response.intent}



graph_builder = StateGraph(State)
graph_builder.add_node("user_intent", user_intent)
graph_builder.add_edge(START, "user_intent")
graph_builder.add_edge("user_intent", END)

graph = graph_builder.compile()


