from src.loma_tutor.application.conversation.chains import get_qa_generation_chain
import pprint

def main():
    qa_generation_chain = get_qa_generation_chain()
    response = qa_generation_chain.invoke(input={
        "topic": "LinkedLists",
        "num_questions": 2
    })
    print(response)


if __name__ == "__main__":
    main()
