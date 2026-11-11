"""Testes do contrato 3 (gate de privacidade).

Os dados pessoais das fixtures são fictícios (fulano, Zéfiro Quintanilha).
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import check_privacy as cp

FIX = Path(__file__).parent / "fixtures" / "privacy"
REPO = Path(__file__).resolve().parents[1]
FAKE_TERM = "zefiro quintanilha"  # sem acento de propósito: testa a normalização


@pytest.fixture
def terms_file(tmp_path: Path) -> Path:
    path = tmp_path / "termos.txt"
    path.write_text(f"# comentário ignorado\n\n{FAKE_TERM}\n", encoding="utf-8")
    return path


def git_repo(root: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    return root


# --- unidade -----------------------------------------------------------------


def test_placeholders_e_falsos_positivos_passam() -> None:
    path = FIX / "ok" / "placeholders.md"
    assert cp.scan_file(path, [cp.normalize(FAKE_TERM)], FIX) == []


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("caminho_windows.md", "caminho pessoal"),
        ("caminho_json.json", "caminho pessoal"),
        ("caminho_linux.sh", "caminho pessoal"),
        ("caminho_macos.txt", "caminho pessoal"),
        ("email.md", "e-mail"),
        ("termo.md", "termo nº 1"),
    ],
)
def test_dado_pessoal_falha(name: str, expected: str) -> None:
    violations = cp.scan_file(FIX / "bad" / name, [cp.normalize(FAKE_TERM)], FIX)
    assert any(expected in v.message for v in violations), violations


def test_todos_os_fixtures_bad_sao_testados() -> None:
    testados = {p[0] for p in test_dado_pessoal_falha.pytestmark[0].args[1]}
    assert testados == {p.name for p in (FIX / "bad").iterdir()}


def test_normalizacao_ignora_acento_e_caixa() -> None:
    assert cp.normalize("ZÉFIRO Quintanilha") == FAKE_TERM


def test_carrega_termos_ignorando_comentarios(terms_file: Path) -> None:
    assert cp.load_terms(terms_file) == [FAKE_TERM]


def test_nome_de_arquivo_com_termo_falha(tmp_path: Path) -> None:
    path = tmp_path / "ata_zefiro_quintanilha.md"
    path.write_text("conteúdo neutro\n", encoding="utf-8")
    violations = cp.scan_file(path, ["zefiro_quintanilha"], tmp_path)
    assert any("nome do arquivo" in v.message for v in violations)


def test_binario_e_ignorado(tmp_path: Path) -> None:
    path = tmp_path / "imagem.bin"
    # Conteúdo vem da fixture para este arquivo de teste não conter um e-mail literal.
    path.write_bytes(b"\0\1\2 " + (FIX / "bad" / "email.md").read_bytes())
    assert cp.scan_file(path, [], tmp_path) == []


def test_exclusao_restrita_as_fixtures_bad() -> None:
    """A lista de exclusão do pyproject não pode virar brecha (ver ADR-0002)."""
    excludes = cp.load_excludes(REPO)
    assert excludes == ["tests/fixtures/privacy/bad/"]


# --- CLI / ponta a ponta -------------------------------------------------------


def test_repositorio_passa_no_gate() -> None:
    # Usa a .privacy-terms.txt local se existir; no CI, só caminhos e e-mails.
    assert cp.main([]) == 0


def test_gate_falha_com_arquivo_de_teste_com_caminho_pessoal(tmp_path: Path) -> None:
    """Critério de sucesso do E0: um arquivo novo com caminho pessoal derruba o gate."""
    root = git_repo(tmp_path / "repo")
    shutil.copy(FIX / "bad" / "caminho_windows.md", root / "nota.md")
    assert cp.main(["--root", str(root), "--terms-file", str(tmp_path / "nada.txt")]) == 1


def test_gate_falha_com_arquivo_de_teste_com_email(tmp_path: Path) -> None:
    root = git_repo(tmp_path / "repo")
    shutil.copy(FIX / "bad" / "email.md", root / "contato.md")
    assert cp.main(["--root", str(root), "--terms-file", str(tmp_path / "nada.txt")]) == 1


def test_gate_respeita_gitignore(tmp_path: Path) -> None:
    root = git_repo(tmp_path / "repo")
    (root / ".gitignore").write_text("segredo.md\n", encoding="utf-8")
    shutil.copy(FIX / "bad" / "email.md", root / "segredo.md")
    assert cp.main(["--root", str(root), "--terms-file", str(tmp_path / "nada.txt")]) == 0


def test_termo_nao_aparece_na_saida(
    tmp_path: Path, terms_file: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "ata.md"
    path.write_text("Presente: Zéfiro Quintanilha\n", encoding="utf-8")
    assert cp.main(["--root", str(tmp_path), "--terms-file", str(terms_file), str(path)]) == 1
    out = capsys.readouterr()
    assert "termo nº 1" in out.out
    assert "quintanilha" not in (out.out + out.err).casefold()


def test_sem_lista_de_termos_so_avisa(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "neutro.md"
    path.write_text("texto neutro\n", encoding="utf-8")
    args = ["--root", str(tmp_path), "--terms-file", str(tmp_path / "nada.txt"), str(path)]
    assert cp.main(args) == 0
    assert "aviso" in capsys.readouterr().err


def test_require_terms_falha_sem_lista(tmp_path: Path) -> None:
    path = tmp_path / "neutro.md"
    path.write_text("texto neutro\n", encoding="utf-8")
    args = ["--root", str(tmp_path), "--terms-file", str(tmp_path / "nada.txt"), "--require-terms"]
    assert cp.main([*args, str(path)]) == 2


def test_cli_como_subprocesso(tmp_path: Path) -> None:
    path = tmp_path / "contato.md"
    shutil.copy(FIX / "bad" / "email.md", path)
    result = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "check_privacy.py"), str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    assert result.returncode == 1
    assert "contato.md:1: e-mail" in result.stdout


def test_caminho_com_barra_normal_e_reportado_uma_vez(tmp_path: Path) -> None:
    # C:/Users/<nome> casa o padrão do Windows; o POSIX não pode repetir o achado.
    source = (FIX / "bad" / "caminho_windows.md").read_text(encoding="utf-8")
    path = tmp_path / "nota.md"
    path.write_text(source.replace("\\", "/"), encoding="utf-8")
    assert len(cp.scan_file(path, [], tmp_path)) == 1
