from langchain.chat_models import init_chat_model
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

llm =  init_chat_model("openai:gpt-4o-mini")

llm = llm.bind_tools([])

#Define the state
class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    

#Define the nodes
def chatbot(state: AgentState)-> AgentState:
    
    #get messages from state
    messages = state["messages"]
    
    #get last message
    last_message = messages[-1]
    
    #Define a prompt
    PROMPT= """ you are helpful assistant please response to this user query {user_query} """
    
    system_instruction = PROMPT.format(user_query=last_message.content)
    
    messages = [
        {"role": "system", "content": system_instruction}
    ]
    
    response = llm.invoke(messages)
    
    return {"messages": [response]}
    
    


#Compile the graph

graph_builder = StateGraph(AgentState)

#add nodes
graph_builder.add_node("chatbot", chatbot)

#add edges
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

#compile the graph
graph = graph_builder.compile()