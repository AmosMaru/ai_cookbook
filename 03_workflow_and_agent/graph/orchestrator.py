from pydantic import BaseModel, Field
from typing import List
from langchain.chat_models import init_chat_model

llm = init_chat_model("openai:gpt-4o-mini")

#Schema for structured output to use in planning
class Section(BaseModel):
    name: str = Field(description="The name of the section of the report")
    description: str = Field(description="Brief overview of the main topics and concepts to be covered in this section.")
    
class Sections(BaseModel):
    sections: List[Section] = Field(description="List of sections to be covered in the report")
    
planner_llm = llm.with_structured_output(Sections)
    
    
    
import operator
from typing_extensions import Annotated
from langgraph.types import Send
from langgraph.graph.message import MessagesState
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# Graph state
class SharedState(MessagesState):
    sections: list[Section]
    completed_sections: Annotated[list, operator.add]
    final_report: str
    
#Worker state
class WorkerState(TypedDict):
    section: Section
    completed_sections: Annotated[list, operator.add]
    
    
#Orchestrator
def orchestrator(state: SharedState):
    """Orchestrator to generate a plan for the report"""
    
    user_query = state['messages'][-1].content
    
    system_instruction = """You are a helpful assistant that can generate a plan for the report."""
    
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": f"Here is the report topic {user_query}. Please generate a plan for the report."}
    ]
    
    response = planner_llm.invoke(messages)
    
    return {"sections": response.sections}
    
    
#Worker
def worker(state: WorkerState):
    """Worker to write a section of the report"""
    
    section_name = state['section'].name
    section_description = state['section'].description
    
    system_instruction = """Write a report section following the provided name and description. Include no preamble for each section. Use markdown formatting."""
    
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": f"Here is the section name {section_name} and description {section_description}. Please write a report section following the provided name and description."}
    ]
    
    response = llm.invoke(messages)
    
    return {"completed_sections": [response.content]}

def synthesizer(state: SharedState):
    """Synthesize the completed sections into a final report"""
    
    final_report = "\n\n".join(state["completed_sections"])
    
    return {"final_report": final_report}

def assign_workers(state: SharedState):
    """Assign a worker to write a section of the report"""
    
    return [Send("worker", {"section": section}) for section in state["sections"]]
    
    
graph_builder = StateGraph(SharedState)
graph_builder.add_node("orchestrator", orchestrator)
graph_builder.add_node("worker", worker)
graph_builder.add_node("synthesizer", synthesizer)

graph_builder.add_edge(START, "orchestrator")
graph_builder.add_conditional_edges("orchestrator", assign_workers, ["worker"])

graph_builder.add_edge("worker", "synthesizer")
graph_builder.add_edge("synthesizer", END)
graph = graph_builder.compile()
        
    