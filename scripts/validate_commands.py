"""Contrato 1: frontmatter dos comandos do Claude Code.

Todo `commands/**/*.md` precisa:
- começar com frontmatter YAML (`---` ... `---`);
- ter `description` como string não vazia (é o texto que aparece no menu `/`);
- ter `argument-hint` (string não vazia) se o corpo usar `$ARGUMENTS`, para o
  usuário saber o que passar ao comando.

Uso: python scripts/validate_commands.py [arquivo_ou_pasta ...]   (padrão: commands/)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from _common import REPO_ROOT, Violation, read_text, rel, report, utf8_output

FENCE = "---"


def split_frontmatter(text: str) -> tuple[str, str, int] | None:
    """Devolve (yaml, corpo, linha onde o corpo começa) ou None se não houver frontmatter."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != FENCE:
        return None
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == FENCE:
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1 :]), i + 2
    return None


def non_empty_str(value: object) -> bool:
    return isinstance(value, str) and value.strip() != ""


def check_file(path: Path) -> list[Violation]:
    name = rel(path)
    try:
        text = read_text(path)
    except UnicodeDecodeError:
        return [Violation(name, 1, "arquivo não está em UTF-8")]

    parts = split_frontmatter(text)
    if parts is None:
        return [Violation(name, 1, "sem frontmatter YAML (o arquivo deve começar com '---')")]
    raw, body, _ = parts

    try:
        # safe_load, nunca load: o load interpreta tags YAML (!!python/object...)
        # e pode instanciar objetos arbitrários, o que é execução de código.
        meta = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line = mark.line + 2 if mark else 1
        return [Violation(name, line, f"frontmatter YAML inválido: {exc}")]

    if not isinstance(meta, dict):
        return [Violation(name, 2, "frontmatter deve ser um mapeamento chave: valor")]

    found: list[Violation] = []
    if not non_empty_str(meta.get("description")):
        found.append(Violation(name, 2, "'description' ausente ou vazio"))
    if "$ARGUMENTS" in body and not non_empty_str(meta.get("argument-hint")):
        found.append(Violation(name, 2, "usa $ARGUMENTS mas 'argument-hint' está ausente ou vazio"))
    return found


def collect(targets: list[Path]) -> list[Path]:
    files: list[Path] = []
    for t in targets:
        if t.is_dir():
            files.extend(sorted(t.rglob("*.md")))
        elif t.suffix == ".md":
            files.append(t)
    return files


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", type=Path, default=[REPO_ROOT / "commands"])
    args = parser.parse_args(argv)
    utf8_output()

    missing = [p for p in args.paths if not p.exists()]
    if missing:
        print(f"caminho inexistente: {', '.join(map(str, missing))}", file=sys.stderr)
        return 2

    files = collect(args.paths)
    if not files:
        print("nenhum comando .md encontrado", file=sys.stderr)
        return 2

    violations = [v for f in files for v in check_file(f)]
    return report(violations, f"contrato 1 ok: {len(files)} comando(s) válido(s).")


if __name__ == "__main__":
    sys.exit(main())
