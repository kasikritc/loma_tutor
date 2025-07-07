from functools import lru_cache
from typing import Annotated, Literal, TypedDict

class QAPair(TypedDict):
    question: str
    answer_requirements: str

class QAList(TypedDict):
    qa_pairs: list[QAPair]

class EvaluationMetric(TypedDict):
    question: str
    answer_requirements: str
    user_answer: str
    metric: str
    score: int
    explanation: str

class TutorResponse(TypedDict):
    response_to_student: Annotated[str, "The Socratic response that will visible to the student as a reply to the student's most recent response"]
    updated_answer_requirements: Annotated[str, "This private checklist that is only visible to AI and not student, for the tutor dynamically tracks the student's remaining learning requirements by adapting to their most recent answer, removing concepts they have mastered, and adding any new misconceptions that are revealed."]