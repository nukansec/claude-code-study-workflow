"""Testes do contrato 1 (frontmatter dos comandos)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import validate_commands as vc

FIX = Path(__file__).parent / "fixtures" / "commands"
REPO = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("path", sorted((FIX / "ok").glob("*.md")), ids=lambda p: p.name)
def test_comando_valido_passa(path: Path) -> None:
    assert vc.check_file(path) == []


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("sem_frontmatter.md", "sem frontmatter"),
        ("sem_description.md", "'description' ausente"),
        ("description_vazia.md", "'description' ausente ou vazio"),
        ("sem_argument_hint.md", "'argument-hint'"),
        ("yaml_invalido.md", "YAML inválido"),
        ("frontmatter_lista.md", "mapeamento"),
        # safe_load recusa a tag em vez de executar os.system.
        ("tag_python.md", "YAML inválido"),
    ],
)
def test_comando_invalido_falha(name: str, expected: str) -> None:
    violations = vc.check_file(FIX / "bad" / name)
    assert violations, f"{name} deveria violar o contrato"
    assert any(expected in v.message for v in violations)


def test_todos_os_fixtures_bad_sao_testados() -> None:
    # Fixture nova em bad/ sem caso de teste vira teste esquecido.
    testados = {p[0] for p in test_comando_invalido_falha.pytestmark[0].args[1]}
    assert testados == {p.name for p in (FIX / "bad").glob("*.md")}


def test_comandos_do_repositorio_passam() -> None:
    assert vc.main([str(REPO / "commands")]) == 0


def test_codigos_de_saida() -> None:
    assert vc.main([str(FIX / "ok")]) == 0
    assert vc.main([str(FIX / "bad")]) == 1
    assert vc.main([str(FIX / "nao_existe")]) == 2


def test_cli_imprime_arquivo_e_linha() -> None:
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "validate_commands.py"), str(FIX / "bad")],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode == 1
    assert "sem_argument_hint.md:2:" in result.stdout
