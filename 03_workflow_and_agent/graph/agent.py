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
    
    
#Define tools
@tool
def get_product_price(product_name: str) -> str:
    """Get the product price"""
    return f"The price of {product_name} is $10."

@tool
def get_weather_info(city: str) -> str:
    """Get the weather info"""
    return f"The weather in {city} is sunny."

@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a * b

@tool
def divide(a: int, b: int) -> int:
    """Divide a by b.

    Args:
        a: first int
        b: second int
    """
    return a / b


@tool
def add(a: int, b: int) -> int:
    """Add a and b.

    Args:
        a: first int
        b: second int
    """
    return a + b
    
    
tools = [get_product_price, get_weather_info, multiply, divide, add]

tools_by_name = {tool.name: tool for tool in tools}

llm_with_tools = llm.bind_tools(tools, parallel_tool_calls=False)


def llm_call(state: AgentState):
    """LLM call"""
    
    messages = state['messages']
    
    system_instruction = """You are a helpful assistant tasked with performing arithmetic on a set of inputs."""
    
    messages = [
        {"role": "system", "content": system_instruction}
    ] + messages
    
    response = llm_with_tools.invoke(messages)
    
    return {"messages": [response]}


def tool_node(state: AgentState):
    """Tool node"""
    
    result = []
    
    for tool_call in state['messages'][-1].tool_calls:
        tool = tools_by_name[tool_call['name']]
        
        observation = tool.invoke(tool_call['args'])
        
        result.append(ToolMessage(content=observation, tool_call_id=tool_call['id']))
        
    return {"messages": result}


def should_continue(state: AgentState)->Literal["tool_node", END]:
    """Should continue"""
    
    messages = state['messages']
    
    last_message = messages[-1]
    
    if last_message.tool_calls:
        return "tool_node"
    
    return END
        
        
agent_builder = StateGraph(AgentState)

agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue, {"tool_node": "tool_node", END: END})
agent_builder.add_edge("tool_node", "llm_call")

graph = agent_builder.compile()


        
    


