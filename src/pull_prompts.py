"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header
from langsmith import Client

load_dotenv()


def pull_prompts_from_langsmith():
    client = Client()
    return client.pull_prompt("leonanluppi/bug_to_user_story_v1")


def main():
    """Função principal"""
    print_section_header("Iniciando Pull de Prompts do LangSmith Prompt Hub")

    required_env_vars = ["LANGSMITH_API_KEY"]
    check_env_vars(required_env_vars)

    try:
        prompts = pull_prompts_from_langsmith()
        print("Pull Realizado.")
    except Exception as e:
        print(f"Erro no pull: {e}")
        return 1

    output_path = Path("prompts/bug_to_user_story_v1.yml")
    save_yaml(prompts, output_path)
    print(f"Prompts salvos em: {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
