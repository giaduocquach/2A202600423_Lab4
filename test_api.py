from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def main() -> None:
    load_dotenv()
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response = llm.invoke("Xin chào! Hãy xác nhận rằng API đang hoạt động.")
    print(response.content)


if __name__ == "__main__":
    main()
