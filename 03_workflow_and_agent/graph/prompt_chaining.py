from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from pydantic import BaseModel, Field
from typing import TypedDict
from langchain.chat_models import init_chat_model

llm = init_chat_model("openai:gpt-4o-mini")

#Define the state
class AgentState(MessagesState):
    """State for the agent"""
    classification: str 
    
#Define the AnalyzedInput class
class AnalyzedInput(BaseModel):
    """Analyzed input"""
    classification: str = Field(description="Classification of the input. Can be get_product_price or get_weather_info")
    reason: str = Field(description="Reason for the classification")
    
# Define the analyze_user_input function
def analyze_user_input(state: AgentState) -> AgentState:
    """Analyze the user input"""
    user_query = state['messages'][-1].content
    
    structured_llm = llm.with_structured_output(AnalyzedInput)
    
    system_instruction = """You are a helpful assistant that can analyze user input and classify it into one of two categories: get_product_price or get_weather_info."""
    
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_query}
    ]
    
    response = structured_llm.invoke(messages)
    
    return {"classification": response.classification}

# Define the get_product_price function
def get_product_price(state: AgentState) -> AgentState:
    """Get the product price"""
    
    system_instruction = """You are a helpful assistant that can get the product price."""
    
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": state['messages'][-1].content}
    ]
    
    response = llm.invoke(messages)
    
    return {"messages": [response]}

# Define the get_weather_info function
def get_weather_info(state: AgentState) -> AgentState:
    """Get the weather info"""
    
    system_instruction = """You are a helpful assistant that can get the weather info."""
    
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": state['messages'][-1].content}
    ]
    
    response = llm.invoke(messages)
    
    return {"messages": [response]}

#def translate to swahili function
def translate_to_swahili(state: AgentState) -> AgentState:
    """Translate the user input to swahili"""
    
    system_instruction = """You are a helpful assistant that can translate user input to swahili."""
    
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": state['messages'][-1].content}
    ]
    
    response = llm.invoke(messages)
    
    return {"messages": [response]}

# Define the route_user_query function
def route_user_query(state: AgentState) -> AgentState:
    """Route the user query to the appropriate node"""
    
    if state['classification'] == "get_product_price":
        return "get_product_price"
    
    return "get_weather_info"
   

# Define the graph
graph_builder = StateGraph(AgentState)

# Add nodes
graph_builder.add_node("analyze_user_input", analyze_user_input)
graph_builder.add_node("get_product_price", get_product_price)
graph_builder.add_node("get_weather_info", get_weather_info)
graph_builder.add_node("translate_to_swahili", translate_to_swahili)

# Add edges
graph_builder.add_edge(START, "analyze_user_input")
graph_builder.add_conditional_edges("analyze_user_input", route_user_query, {"get_product_price": "get_product_price", "get_weather_info": "get_weather_info"})
graph_builder.add_edge("get_product_price", END)
graph_builder.add_edge("get_weather_info", "translate_to_swahili")
graph_builder.add_edge("translate_to_swahili", END)

# Compile the graph
graph = graph_builder.compile()

    
    
    
    