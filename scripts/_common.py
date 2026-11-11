"""Utilidades compartilhadas pelos validadores de contrato.

Todos os scripts seguem o mesmo protocolo: imprimem uma violação por linha no
formato `arquivo:linha: mensagem` (clicável em editores e no log do CI) e saem
com código 1 se houver violação, 0 se não houver e 2 em erro de uso.
"""

from __future__ import annotations

import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True, order=True)
class Violation:
    path: str
    line: int
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.message}"


def rel(path: Path, root: Path = REPO_ROOT) -> str:
    """Caminho relativo à raiz, com `/`, para mensagens iguais no Windows e no Linux."""
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def read_text(path: Path) -> str:
    """Lê como UTF-8 explícito: no Windows o padrão é cp1252 e quebraria os acentos."""
    return path.read_text(encoding="utf-8")


def repo_files(root: Path = REPO_ROOT) -> list[Path]:
    """Arquivos versionados + não versionados que não estão no .gitignore.

    Só `git ls-files` não basta: antes do primeiro commit (ou num arquivo novo
    ainda não adicionado) a lista viria vazia e o gate passaria sem olhar nada.
    """
    result = subprocess.run(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
        cwd=root,
        capture_output=True,
        check=True,
    )
    names = result.stdout.decode("utf-8").split("\0")
    return [root / n for n in sorted(set(names)) if n and (root / n).is_file()]


def utf8_output() -> None:
    """Força UTF-8 no stdout/stderr: no Windows o padrão do console é cp1252."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8")


def report(violations: Iterable[Violation], ok_message: str) -> int:
    found = sorted(violations)
    for v in found:
        print(v)
    if found:
        print(f"\n{len(found)} violação(ões) encontrada(s).", file=sys.stderr)
        return 1
    print(ok_message)
    return 0
