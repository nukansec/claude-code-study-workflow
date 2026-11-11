"""Contrato 3: gate de privacidade.

Falha se algum arquivo do repositório (versionado ou prestes a ser) contiver:
- caminho absoluto de usuário: `C:\\Users\\<nome>`, `/home/<nome>`, `/Users/<nome>`;
- endereço de e-mail;
- um termo da lista local `.privacy-terms.txt` (gitignored, um termo por linha,
  `#` para comentário). A comparação ignora maiúsculas e acentos.

Placeholders como `C:\\Users\\<x>` ou `/home/<usuario>` são permitidos, para a
documentação poder citar o padrão. Sem a lista de termos, o gate só avisa
(quem clona o repo e o CI não a têm); com `--require-terms`, falha. O
pre-commit do autor usa `--require-terms`. Ver docs/adr/0002.

Uso: python scripts/check_privacy.py [--terms-file F] [--require-terms] [arquivo ...]
     (sem arquivos: todos os de `git ls-files --cached --others --exclude-standard`)
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
import unicodedata
from pathlib import Path

from _common import REPO_ROOT, Violation, rel, repo_files, report, utf8_output

TERMS_FILE = REPO_ROOT / ".privacy-terms.txt"
BINARY_SNIFF = 8192

# Nome do usuário: para no separador, espaço, aspas ou fim de placeholder.
_NAME = r"([^\\/\s<>\"'`*]+)"
# Depois do prefixo, recusa placeholder/variável: <x>, ~, %USERNAME%, $USER, {user}.
_NOT_PLACEHOLDER = r"(?![<~%$*{])"
PATH_PATTERNS = (
    # C:\Users\<nome>, C:\\Users\\<nome> (escapado em JSON/código) ou C:/Users/<nome>.
    re.compile(r"(?i)\b[a-z]:(?:\\{1,2}|/)users(?:\\{1,2}|/)" + _NOT_PLACEHOLDER + _NAME),
    # /home/<nome> e /Users/<nome>. O lookbehind evita casar dentro de URL
    # (site.com/home/x) e repetir o achado de C:/Users/<nome> (o ":" antes da barra).
    re.compile(r"(?<![\w.~/:-])/(?:home|Users)/" + _NOT_PLACEHOLDER + _NAME),
)
# Pastas do Windows que não identificam ninguém.
GENERIC_USERS = {"public", "default", "default user", "all users"}

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")


def normalize(text: str) -> str:
    """Minúsculas e sem acento: 'Conceição' e 'CONCEICAO' viram o mesmo texto."""
    decomposed = unicodedata.normalize("NFKD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c)).casefold()


def load_terms(path: Path) -> list[str]:
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        term = line.strip()
        if term and not term.startswith("#"):
            terms.append(normalize(term))
    return terms


def load_excludes(root: Path = REPO_ROOT) -> list[str]:
    pyproject = root / "pyproject.toml"
    if not pyproject.is_file():
        return []
    with pyproject.open("rb") as fh:
        config = tomllib.load(fh)
    return list(config.get("tool", {}).get("privacy_gate", {}).get("exclude", []))


def is_excluded(name: str, excludes: list[str]) -> bool:
    return any(name == e or (e.endswith("/") and name.startswith(e)) for e in excludes)


def is_binary(data: bytes) -> bool:
    return b"\0" in data[:BINARY_SNIFF]


def scan_text(name: str, text: str, terms: list[str]) -> list[Violation]:
    found: list[Violation] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for pattern in PATH_PATTERNS:
            for m in pattern.finditer(line):
                if m.group(1).casefold() not in GENERIC_USERS:
                    found.append(Violation(name, lineno, f"caminho pessoal: {m.group(0)}"))
        for m in EMAIL.finditer(line):
            found.append(Violation(name, lineno, f"e-mail: {m.group(0)}"))
        if terms:
            norm = normalize(line)
            for idx, term in enumerate(terms, start=1):
                if term in norm:
                    # Não imprime o termo: a saída pode parar num log ou num print.
                    found.append(Violation(name, lineno, f"termo nº {idx} de .privacy-terms.txt"))
    return found


def scan_file(path: Path, terms: list[str], root: Path = REPO_ROOT) -> list[Violation]:
    name = rel(path, root)
    found: list[Violation] = []
    # O nome do arquivo também vaza informação (ex.: ata_<nome>.md).
    norm_name = normalize(name)
    for idx, term in enumerate(terms, start=1):
        if term in norm_name:
            found.append(Violation(name, 1, f"nome do arquivo contém o termo nº {idx}"))

    data = path.read_bytes()
    if is_binary(data):
        # Binários (PDF, imagem) não são lidos aqui; ver pendência no ADR-0002.
        return found
    return found + scan_text(name, data.decode("utf-8", errors="replace"), terms)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--terms-file", type=Path, default=TERMS_FILE)
    parser.add_argument(
        "--require-terms",
        action="store_true",
        help="falha se a lista de termos não existir (uso no pre-commit do autor)",
    )
    parser.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    utf8_output()
    root: Path = args.root

    if args.terms_file.is_file():
        terms = load_terms(args.terms_file)
    elif args.require_terms:
        print(f"erro: lista de termos ausente: {args.terms_file}", file=sys.stderr)
        return 2
    else:
        print(
            f"aviso: {args.terms_file.name} ausente; checando só caminhos e e-mails.",
            file=sys.stderr,
        )
        terms = []

    files = args.files or repo_files(root)
    excludes = load_excludes(root)
    terms_path = args.terms_file.resolve()
    targets = [
        f
        for f in files
        if f.is_file() and f.resolve() != terms_path and not is_excluded(rel(f, root), excludes)
    ]

    violations = [v for f in targets for v in scan_file(f, terms, root)]
    return report(
        violations,
        f"contrato 3 ok: {len(targets)} arquivo(s) sem dados pessoais ({len(terms)} termo(s)).",
    )


if __name__ == "__main__":
    sys.exit(main())
