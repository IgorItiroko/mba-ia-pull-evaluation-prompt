"""
Testes automatizados para validação de prompts.
"""
import re
import pytest
import yaml
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

PROMPT_FILE = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
PROMPT_KEY = "bug_to_user_story_v2"

# Tags de domínio do projeto — não contam como técnicas de prompt engineering
DOMAIN_TAGS = {"bug-analysis", "user-story", "product-management"}


def load_prompt() -> dict:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert PROMPT_KEY in data, f"Chave '{PROMPT_KEY}' não encontrada em {PROMPT_FILE.name}"
    return data[PROMPT_KEY]


class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt = load_prompt()
        assert "system_prompt" in prompt, "Campo 'system_prompt' não encontrado no YAML"
        assert prompt["system_prompt"].strip(), "'system_prompt' está vazio"

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: 'Você é um Project Manager')."""
        prompt = load_prompt().get("system_prompt", "")
        assert "Você é" in prompt or "você é" in prompt, (
            "Prompt não define uma persona. Adicione algo como 'Você é um Product Manager...'"
        )

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato User Story padrão (BDD / Dado-Quando-Então)."""
        prompt = load_prompt().get("system_prompt", "")
        bdd_keywords = ["Dado que", "Quando", "Então"]
        missing = [kw for kw in bdd_keywords if kw not in prompt]
        assert not missing, (
            f"Prompt não menciona as palavras-chave de formato BDD: {missing}"
        )

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém pelo menos 2 exemplos few-shot com campo 'Bug:'."""
        prompt = load_prompt().get("system_prompt", "")
        example_count = prompt.count("Bug:")
        assert example_count >= 2, (
            f"Prompt deve conter ao menos 2 exemplos few-shot com 'Bug:', encontrados: {example_count}"
        )

    def test_prompt_no_todos(self):
        """Garante que nenhum 'TODO' foi deixado no system_prompt."""
        prompt = load_prompt().get("system_prompt", "")
        assert not re.search(r"\bTODO\b", prompt), (
            "system_prompt ainda contém TODO(s) — remova-os antes de publicar"
        )

    def test_minimum_techniques(self):
        """Verifica se pelo menos 2 técnicas de prompt engineering estão listadas nas tags."""
        prompt = load_prompt()
        all_tags = prompt.get("tags", [])
        technique_tags = [t for t in all_tags if t not in DOMAIN_TAGS]
        assert len(technique_tags) >= 2, (
            f"Mínimo de 2 técnicas requeridas nas tags, encontradas: {technique_tags}. "
            f"Adicione tags como 'Few-Shots', 'Role Prompting', 'CoT', 'SoT', etc."
        )


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
