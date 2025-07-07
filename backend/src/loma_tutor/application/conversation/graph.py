from functools import lru_cache

from langgraph import graph
from langgraph.graph import START, END, StateGraph

from loma_tutor.application.conversation.nodes import (
    greeting_node,
    conversation_node,
    question_advancing_node,
)

from loma_tutor.application.conversation.conditionals import (
    should_greet,
    should_advance_question_node
)

from loma_tutor.application.conversation.state import TutorState

@lru_cache(maxsize=1)
def create_tutor_conversation_graph():
    graph_builder = StateGraph(TutorState)

    # Add all nodes
    graph_builder.add_node("greeting_node", greeting_node)
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("question_advancing_node", question_advancing_node)
    graph_builder.add_node("should_advance_question_node", should_advance_question_node)

    # Define the flow
    graph_builder.add_conditional_edges(START, should_greet)
    graph_builder.add_edge("greeting_node", END)
    graph_builder.add_edge("conversation_node", "should_advance_question_node")
    graph_builder.add_edge("question_advancing_node", END)

    return graph_builder

graph = create_tutor_conversation_graph().compile()