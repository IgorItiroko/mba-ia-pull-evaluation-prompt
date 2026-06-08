"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.loading import load_prompt
from utils import load_yaml, check_env_vars, print_section_header
from langsmith import Client


load_dotenv()

PROJECT_NAME = 'MBA_DESAFIO_2'


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """

    data = prompt_data 

    template = ChatPromptTemplate.from_messages([
        ("system", data["system_prompt"]),
        ("human", data["user_prompt"]),
    ])

    client = Client()
    url = client.push_prompt(
        "bug_to_user_story_v2",
        object=template,
        tags=[
            f"{prompt_data["version"]}",
            f"model: {prompt_data["model"]}",
            *prompt_data["tags"],
        ],
        description=prompt_data["description"],
    )
    return True if url else False



def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    is_valid = True
    errors = []
    validations = ["system_prompt", "user_prompt", "version", "description"]

    for validation in validations:
        if validation not in prompt_data:
            is_valid = False
            errors.append(f"O prompt não possuí {validation}")
    return (is_valid, errors)



def main():
    """Função principal"""
    print_section_header("Iniciando Push de Prompts do LangSmith Prompt Hub")
    
    required_env_vars = ["LANGSMITH_API_KEY"]
    check_env_vars(required_env_vars)
    prompt = load_yaml("prompts/bug_to_user_story_v2.yml")
    
    (is_valid, errors) = validate_prompt(prompt["bug_to_user_story_v2"])
    if not is_valid:
        print("Prompt invalido:\n" + "\n".join(f"- {error}" for error in errors))
        return 1

    try:
        push_prompt_to_langsmith(PROJECT_NAME, prompt["bug_to_user_story_v2"])
        print("Push realizado.")
    except Exception as e:
        print(f"Erro no push: {e}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
