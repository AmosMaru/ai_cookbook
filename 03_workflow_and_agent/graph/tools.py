#Define a tool
from langchain_core.tools import tool
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState

# Define the state
class AgentState(MessagesState):
    """State for the agent"""
    
    
llm = init_chat_model("openai:gpt-4o-mini")

@tool
def get_current_price(product: str, location: str) -> str:
    """
    Returns the current price of a product in a specific location.
    """
    return f"The current price of {product} in {location} is $100."

@tool
def get_current_weather(location: str) -> str:
    """
    Returns the current weather in a specific location.
    """
    return f"The current weather in {location} is sunny."

#Bind the tools to the llm
llm_with_tools = llm.bind_tools(tools=[get_current_price, get_current_weather])

def llm_call(state: AgentState):
    """LLM call"""
    
    messages = state['messages']
    
    system_instruction = """You are a helpful assistant that can get the current price of a product in a specific location."""
    
    messages = [
        {"role": "system", "content": system_instruction}
    ] + messages
    
    response = llm_with_tools.invoke(messages)
    
    return {"messages": [response]}


graph_builder = StateGraph(AgentState)

graph_builder.add_node("llm_call", llm_call)

graph_builder.add_edge(START, "llm_call")
graph_builder.add_edge("llm_call", END)

graph = graph_builder.compile()
