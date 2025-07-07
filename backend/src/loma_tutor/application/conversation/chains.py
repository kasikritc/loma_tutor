from typing import Optional, Literal
from langchain_core.runnables import Runnable
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from functools import lru_cache
from pydantic import SecretStr

from loma_tutor.config import settings
from loma_tutor.domain.prompts import (
    QA_GENERATION_SYSTEM_PROMPT,
    QA_GENERATION_USER_PROMPT,
    TUTOR_GREETING_SYSTEM_PROMPT,
    TUTOR_GREETING_USER_PROMPT,
    TUTOR_RESPONSE_SYSTEM_PROMPT,
    TUTOR_RESPONSE_USER_PROMPT,
)
from loma_tutor.application.conversation.schemas import (
    QAList, 
    TutorResponse
)

@lru_cache
def get_chat_model(
    provider: Literal["OpenAI", "Groq"],
    model: Optional[str] = None,
    temperature: Optional[float] = None,
    api_key: Optional[str] = None
) -> BaseChatModel:
    """
    Returns a chat model instance for the given provider, allowing overrides for model, temperature, and api_key.
    Falls back to settings if not provided. Custom provider is not implemented yet.
    """
    if provider == "OpenAI":
        model_name = model if model is not None else settings.OPENAI_LLM_MODEL
        temp = temperature if temperature is not None else settings.OPENAI_LLM_TEMPERATURE
        key = api_key if api_key is not None else settings.OPENAI_API_KEY
        return ChatOpenAI(
            model=model_name,
            temperature=temp,
            api_key=SecretStr(key),
        )
    elif provider == "Groq":
        model_name = model if model is not None else settings.GROQ_LLM_MODEL
        temp = temperature if temperature is not None else settings.GROQ_LLM_TEMPERATURE
        key = api_key if api_key is not None else settings.GROQ_API_KEY
        return ChatGroq(
            model=model_name,
            temperature=temp,
            api_key=SecretStr(key),
        )
    else:
        raise ValueError(f"Unknown provider: {provider}")

def get_qa_generation_chain() -> Runnable:
    """
    When invoking, need to specify "topic" and "num_questions".
    """
    model = get_chat_model(provider=settings.QA_GENERATOR_LLM_PROVIDER)
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", QA_GENERATION_SYSTEM_PROMPT),
            ("user", QA_GENERATION_USER_PROMPT)
        ],
        template_format="jinja2",
    )

    model_with_structured_output = model.with_structured_output(schema=QAList)

    return prompt | model_with_structured_output

def get_tutor_greeting_chain() -> Runnable:
    """
    When invoking, need to specify "topic" and "first_question".
    """
    model = get_chat_model(provider=settings.TUTOR_LLM_PROVIDER)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", TUTOR_GREETING_SYSTEM_PROMPT),
            ("user", TUTOR_GREETING_USER_PROMPT)
        ],
        template_format="jinja2",
    )

    return prompt | model

def get_tutor_response_chain() -> Runnable:
    """
    When invoking, need to specify "topic", "messages", "original_question", and "updated_answer_requirements".
    """
    model = get_chat_model(provider=settings.TUTOR_LLM_PROVIDER)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", TUTOR_RESPONSE_SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="messages"),
            ("user", TUTOR_RESPONSE_USER_PROMPT)
        ],
        template_format="jinja2",
    )

    model_with_structured_output = model.with_structured_output(schema=TutorResponse)

    return prompt | model_with_structured_output