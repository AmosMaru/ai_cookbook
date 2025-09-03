from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from typing import TypedDict


llm = init_chat_model(model="gpt-4o-mini", temperature=0)

class AgentState(TypedDict):
    question: str
    answer: str

AGENT_PROMPT = """
You are a helpful assistant that can answer questions and help with tasks.
"""


def agent_node(state: AgentState):
    
    user_input = state["question"]

    
    messages_list = [
        {
            "role": "system",
            "content": AGENT_PROMPT
        },
        {
            "role": "user",
            "content": user_input
        }
    ] 
    
    response = llm.invoke(messages_list)
    
 
    return {"answer": response.content}



graph_builder = StateGraph(AgentState)

graph_builder.add_node("agent", agent_node)

graph_builder.add_edge(START, "agent")
graph_builder.add_edge("agent", END)

graph = graph_builder.compile()