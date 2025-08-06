from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from pydantic import BaseModel, Field
from typing import TypedDict
from langchain.chat_models import init_chat_model

llm = init_chat_model("openai:gpt-4o-mini")

# Define the state
class AgentState(MessagesState):
    """State for the agent"""
    joke: str
    poem: str
    story: str
    combined_output: str
    
    
    
def generate_joke(state: AgentState) -> AgentState:
    """Generate a joke"""
    
    user_query = state['messages'][-1].content
    
    system_instruction = """You are a helpful assistant that can generate a joke."""
    
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_query}
    ]
    
    response = llm.invoke(messages)
    
    return {"joke": response.content}


def generate_poem(state: AgentState) -> AgentState:
    """Generate a poem"""
    
    user_query = state['messages'][-1].content
    
    system_instruction = """You are a helpful assistant that can generate a poem."""
    
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_query}
    ]
    
    response = llm.invoke(messages)
    
    return {"poem": response.content}


def generate_story(state: AgentState) -> AgentState:
    """Generate a story"""
    
    user_query = state['messages'][-1].content
    
    system_instruction = """You are a helpful assistant that can generate a story."""
    
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": user_query}
    ]
    
    response = llm.invoke(messages)
    
    return {"story": response.content}


def combine_output(state: AgentState) -> AgentState:
    """Combine the output"""
    
    user_query = state['messages'][-1].content
    
    combine_output = f"Here is a story, joke, and open about {user_query}\n\n"
    
    combine_output += f"STORY: {state['story']}\n\n"
    
    combine_output += f"JOKE: {state['joke']}\n\n"
    
    combine_output += f"POEM: {state['poem']}\n\n"
    
    return {"combined_output": combine_output}
    
    
    
# Define the graph
graph_builder = StateGraph(AgentState)

# Add nodes
graph_builder.add_node("generate_joke", generate_joke)
graph_builder.add_node("generate_poem", generate_poem)
graph_builder.add_node("generate_story", generate_story)
graph_builder.add_node("combine_output", combine_output)


# Add edges
graph_builder.add_edge(START, "generate_joke")
graph_builder.add_edge(START, "generate_poem")
graph_builder.add_edge(START, "generate_story")
graph_builder.add_edge("generate_joke", "combine_output")
graph_builder.add_edge("generate_poem", "combine_output")
graph_builder.add_edge("generate_story", "combine_output")
graph_builder.add_edge("combine_output", END)

# Compile the graph
graph = graph_builder.compile()

