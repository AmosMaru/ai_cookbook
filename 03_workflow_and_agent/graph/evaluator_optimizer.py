from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import MessagesState
from pydantic import BaseModel, Field
from typing import TypedDict, Literal
from langchain.chat_models import init_chat_model


llm = init_chat_model("openai:gpt-4o-mini")


# Define the state
class AgentState(TypedDict):
    """State for the agent"""
    customer_email: str
    draft_reply: str
    final_reply: str
    quality: Literal["pass", "fail"]
    feedback: str


# Define the AnalyzedInput class
class EmailReplyFeedback(BaseModel):
    quality: Literal["pass", "fail"] = Field(
        description="Mark as 'pass' if the reply is helpful, complete, professional, and appropriately toned. Otherwise, mark as 'fail'."
    )
    feedback: str = Field(
        description=(
            "If marked 'fail', provide detailed, actionable feedback. "
            "Mention missing information, tone issues, or anything unclear or unhelpful. "
            "Ensure feedback focuses on tone, completeness, and clarity."
        )
    )

    
evaluator_llm = llm.with_structured_output(EmailReplyFeedback)

#Generate email node
def generate_reply_email(state: AgentState):
    """Generate an email reply"""
    
    customer_email = state['customer_email']
    
    feedback = state.get("feedback", "")
    
    if feedback:
        feedback = f"Here is some feedback {feedback}."
    else:
        feedback = ""
    
    system_instruction = """You are a helpful assistant that can a very simple email reply."""
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": f"Here is the customer email {customer_email}. {feedback}"}
    ]
    response = llm.invoke(messages)
    
    return {"draft_reply": response.content}


def evaluate_reply(state: AgentState):
    """Evaluate the email reply"""
    
    customer_email = state['customer_email']
    
    draft_reply = state['draft_reply']
    
    system_instruction = """You are a helpful assistant that can evaluate an email reply."""
    
    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": f"Here is the draft reply {draft_reply} and the actual email {customer_email}. Please evaluate the email reply."}
    ]
    response = evaluator_llm.invoke(messages)
    
    return {"quality": response.quality, "feedback": response.feedback}


def router_by_quality(state: AgentState):
    """Router by quality"""
    
    if state['quality'] == "pass":
        return "Accepted"
    
    return "Rejected"


graph_builder = StateGraph(AgentState)
graph_builder.add_node("generate_reply_email", generate_reply_email)
graph_builder.add_node("evaluate_reply", evaluate_reply)


graph_builder.add_edge(START, "generate_reply_email")
graph_builder.add_edge("generate_reply_email", "evaluate_reply")
graph_builder.add_conditional_edges("evaluate_reply", router_by_quality, {"Accepted": END, "Rejected": "generate_reply_email"})

graph = graph_builder.compile()
