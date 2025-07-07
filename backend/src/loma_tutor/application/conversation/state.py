from langgraph.graph import MessagesState
from loma_tutor.application.conversation.schemas import QAPair

class TutorState(MessagesState):
    topic: str
    question_answer_pairs: list[QAPair]
    updated_answer_requirements: list[str]
    current_question_index: int