from loma_tutor.application.conversation.state import TutorState
from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig

from loma_tutor.application.conversation.chains import (
    get_tutor_greeting_chain,
    get_tutor_response_chain
)

# TODO: update this nodes.py file

async def greeting_node(state: TutorState, config: RunnableConfig):
    greeting_chain = get_tutor_greeting_chain()

    response = await greeting_chain.ainvoke(
        {
            "topic": state["topic"],
            "first_question": state["question_answer_pairs"][0]["question"]
        },
        config
    )

    return {"messages": response.content}

async def conversation_node(state: TutorState, config: RunnableConfig):
    conversation_chain = get_tutor_response_chain()
    current_question_index = state["current_question_index"]

    response = await conversation_chain.ainvoke(
        {
            "topic": state["topic"],
            "messages": state["messages"],
            "original_question": state["question_answer_pairs"][current_question_index]["question"],
            "updated_answer_requirements": state["updated_answer_requirements"][current_question_index]
        },
        config
    )
    
    state["updated_answer_requirements"][current_question_index] = response["updated_answer_requirements"]
    
    return {
        "messages": response["response_to_student"],
        "updated_answer_requirements": state["updated_answer_requirements"]
    }

async def question_advancing_node(state: TutorState, config: RunnableConfig):
    pass

# async def summarize_conversation_node(state: TutorState):
#     summary = state.get("summary", "")
#     summary_chain = get_conversation_summary_chain(summary)

#     response = await summary_chain.ainvoke(
#         {
#             "messages": state["messages"],
#             "philosopher_name": state["philosopher_name"],
#             "summary": summary,
#         }
#     )

#     delete_messages = [
#         RemoveMessage(id=m.id)
#         for m in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]
#     ]
#     return {"summary": response.content, "messages": delete_messages}