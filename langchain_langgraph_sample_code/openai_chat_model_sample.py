# pip install -qU langchain-openai
from langchain_openai import ChatOpenAI
import getpass
import os


def get_llm(model="gpt-4o"):
    if not os.environ.get("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

    llm = ChatOpenAI(
        model=model,
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key= os.environ["OPENAI_API_KEY"]
        # base_url="...",
        # organization="...",
        # other params...
    )
    return llm

def invoke(llm, messages):
    ai_msg = llm.invoke(messages)
    return ai_msg.context

def main():
    model = "gpt-4o"
    llm = get_llm(model)
    messages = [
        (
            "system",
            "You are a helpful assistant that translates English to Japanese. Translate the user sentence.",
        ),
        ("human", "I love programming."),
    ]
    ai_msg = llm.invoke(messages)
    print(ai_msg.content)

if __name__ == "__main__":
    main()

