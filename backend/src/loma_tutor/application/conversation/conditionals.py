from typing import Literal

from loma_tutor.application.conversation.state import TutorState
from loma_tutor.config import settings
from langgraph.types import Command


def should_summarize_conversation(
    state: TutorState
) -> Literal["summarize_conversation_node", "__end__"]:
    messages = state["messages"]

    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "summarize_conversation_node"
    else:
        return "__end__"

def should_greet(
    state: TutorState
) -> Literal["greeting_node", "conversation_node"]:
    if len(state["messages"]) > 0:
        return "conversation_node"
    else:
        return "greeting_node"

def should_advance_question_node(
    state: TutorState
) -> Command[Literal["question_advancing_node", "__end__"]]:
    question_index = state["current_question_index"]
    requirements_for_current_question = state["updated_answer_requirements"][question_index]
    
    if not requirements_for_current_question:
        num_questions = len(state["question_answer_pairs"])

        if question_index ==  num_questions:
            raise ValueError("question_index is now incremented over num_questions")

        return Command(
            update={"current_question_index": question_index + 1}, 
            goto="question_advancing_node"
        )
    else:
        return Command(
            update={},
            goto="__end__"
        )
