from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from pydantic import BaseModel, Field
from typing import TypedDict, Literal
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage

llm = init_chat_model("openai:gpt-4o-mini")

# Define the state
class AgentState(MessagesState):
    """State for the agent"""
    
    
class SearchQuery(BaseModel):
    query: str = Field(description="The search query")
    justification: str = Field(description="Why is this the best search query?")

# Augment the llm with the schema for structured output
structured_llm = llm.with_structured_output(SearchQuery)

# Define the nodes
def llm_call(state: AgentState):
    """LLM call"""
    
    messages = state['messages']
    
    system_instruction = """You are a helpful assistant tasked with coming up with a search query for a user."""
    
    messages = [
        {"role": "system", "content": system_instruction}
    ] + messages
    
    response = structured_llm.invoke(messages)
    
    return {"messages": [response]}



graph_builder = StateGraph(AgentState)

graph_builder.add_node("llm_call", llm_call)

graph_builder.add_edge(START, "llm_call")
graph_builder.add_edge("llm_call", END)

graph = graph_builder.compile()

