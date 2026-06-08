import sys
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, get_llm

load_dotenv()

YAML_PATH = "prompts/bug_to_user_story_v2.yml"


def main():
    bug_report = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else input("Bug report: ")

    data = load_yaml(YAML_PATH)["bug_to_user_story_v2"]

    prompt = ChatPromptTemplate.from_messages([
        ("system", data["system_prompt"]),
        ("human", data["user_prompt"]),
    ])

    llm = get_llm()
    chain = prompt | llm

    response = chain.invoke({"bug_report": bug_report})
    print("\n" + response.content)


if __name__ == "__main__":
    main()
