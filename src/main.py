
import os
import getpass
import embeding
import templates
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA


def main():
    repo_path = input("Enter the path to the repository: ")
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass(
            "Enter API key for OpenAI: ")
    user_query = input(
        "Please enter an explanation of the test you would like to write: ")

    retriver = embeding.embed_from_path(repo_path)

    llm = ChatOpenAI(model_name="gpt-4", temperature=0)

    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=retriver,
        chain_type_kwargs={"prompt": templates.prompt_template},
    )

    result = qa_chain.invoke({"query": user_query})
    print(result["result"])


if __name__ == "__main__":
    main()
