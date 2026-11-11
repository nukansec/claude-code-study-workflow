"""Testes do contrato 2 (política de permissões)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import validate_settings as vs

FIX = Path(__file__).parent / "fixtures" / "settings"


def test_settings_do_repositorio_passa() -> None:
    assert vs.check_file(vs.DEFAULT) == []
    assert vs.main([]) == 0


def test_settings_minimo_passa() -> None:
    assert vs.check_file(FIX / "ok" / "minimo.json") == []


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("json_invalido.json", "JSON inválido"),
        ("sem_permissions.json", "falta o objeto 'permissions'"),
        ("deny_nao_lista.json", "deve ser lista de strings"),
        ("sem_env.json", "não cobre .env"),
        # -execdir não substitui -exec: o contrato exige os dois cobertos.
        ("so_execdir.json", "não cobre find -exec"),
        ("allow_curinga.json", "regra curinga em 'allow'"),
    ],
)
def test_settings_invalido_falha(name: str, expected: str) -> None:
    violations = vs.check_file(FIX / "bad" / name)
    assert any(expected in v.message for v in violations), violations


def test_todos_os_fixtures_bad_sao_testados() -> None:
    testados = {p[0] for p in test_settings_invalido_falha.pytestmark[0].args[1]}
    assert testados == {p.name for p in (FIX / "bad").glob("*.json")}


@pytest.mark.parametrize("target", list(vs.REQUIRED_DENY))
def test_remover_qualquer_alvo_quebra_o_contrato(target: str, tmp_path: Path) -> None:
    """Tira do settings real a(s) regra(s) que cobrem um alvo e confere a falha."""
    data = json.loads(vs.DEFAULT.read_text(encoding="utf-8"))
    pattern = vs.REQUIRED_DENY[target]
    data["permissions"]["deny"] = [r for r in data["permissions"]["deny"] if not pattern.search(r)]
    path = tmp_path / "settings.json"
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    messages = [v.message for v in vs.check_file(path)]
    assert f"'permissions.deny' não cobre {target}" in messages


@pytest.mark.parametrize("rule", ["Bash", "Bash(*)", "Read(**)", "Edit(**/*)", "WebFetch", "*"])
def test_curingas_no_allow_sao_recusados(rule: str) -> None:
    assert vs.WILDCARD_ALLOW.match(rule)


@pytest.mark.parametrize("rule", ["Bash(ls *)", "Bash(pandoc *)", "Read(docs/**)", "WebSearch"])
def test_regras_especificas_no_allow_sao_aceitas(rule: str) -> None:
    assert not vs.WILDCARD_ALLOW.match(rule)


def test_codigos_de_saida() -> None:
    assert vs.main([str(FIX / "bad" / "sem_env.json")]) == 1
    assert vs.main([str(FIX / "nao_existe.json")]) == 2
