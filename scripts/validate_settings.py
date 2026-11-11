"""Contrato 2: política de permissões do Claude Code (policy as code).

Verifica `settings/settings.example.json`:
- é JSON válido, com `permissions.deny` (e `allow`, se houver) como lista de strings;
- `deny` cobre `.env`, `*.tfvars`, `*.pem`, `*.key` e o `find` com `-exec`/`-delete`;
- `allow` não tem regra curinga que libere uma ferramenta inteira (ex.: `Bash(*)`),
  porque isso anularia o privilégio mínimo: tudo o que não estivesse no deny
  rodaria sem confirmação.

A cobertura é checada por semântica (regex sobre as regras), não por string
exata: dá para reescrever uma regra sem quebrar o contrato, desde que ela
continue cobrindo o alvo.

Uso: python scripts/validate_settings.py [arquivo]   (padrão: settings/settings.example.json)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from _common import REPO_ROOT, Violation, read_text, rel, report, utf8_output

DEFAULT = REPO_ROOT / "settings" / "settings.example.json"

# alvo -> regex que uma regra do deny precisa casar para cobri-lo.
REQUIRED_DENY: dict[str, re.Pattern[str]] = {
    ".env": re.compile(r"^Read\((?:[^)]*/)?\.env\)$"),
    "*.tfvars": re.compile(r"^Read\([^)]*\*\.tfvars\)$"),
    "*.pem": re.compile(r"^Read\([^)]*\*\.pem\)$"),
    "*.key": re.compile(r"^Read\([^)]*\*\.key\)$"),
    # \b depois de "exec" não casa "-execdir" (o "d" é caractere de palavra).
    "find -exec": re.compile(r"^Bash\(find\b.*\s-exec\b"),
    "find -delete": re.compile(r"^Bash\(find\b.*\s-delete\b"),
}

# Ferramentas que, liberadas por inteiro, dão execução ou acesso a arquivos sem pergunta.
BROAD_TOOLS = ("Bash", "Read", "Edit", "Write", "WebFetch")
WILDCARD_ALLOW = re.compile(
    r"^(\*|(?:" + "|".join(BROAD_TOOLS) + r")(?:\((?:\*|\*\*|\*\*/\*|/\*\*|\*\*/\*\*)?\))?)$"
)


def find_line(text: str, needle: str) -> int:
    for i, line in enumerate(text.splitlines(), start=1):
        if needle in line:
            return i
    return 1


def check_file(path: Path) -> list[Violation]:
    name = rel(path)
    text = read_text(path)
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return [Violation(name, exc.lineno, f"JSON inválido: {exc.msg}")]

    perms = data.get("permissions") if isinstance(data, dict) else None
    if not isinstance(perms, dict):
        return [Violation(name, 1, "falta o objeto 'permissions'")]

    found: list[Violation] = []
    rules: dict[str, list[str]] = {}
    for key, required in (("deny", True), ("allow", False)):
        value = perms.get(key, None if required else [])
        if not isinstance(value, list) or not all(isinstance(r, str) for r in value):
            found.append(
                Violation(
                    name,
                    find_line(text, f'"{key}"'),
                    f"'permissions.{key}' deve ser lista de strings",
                )
            )
            value = []
        rules[key] = value

    deny_line = find_line(text, '"deny"')
    for target, pattern in REQUIRED_DENY.items():
        if not any(pattern.search(r) for r in rules["deny"]):
            found.append(Violation(name, deny_line, f"'permissions.deny' não cobre {target}"))

    for rule in rules["allow"]:
        if WILDCARD_ALLOW.match(rule.replace(" ", "")):
            found.append(
                Violation(
                    name,
                    find_line(text, json.dumps(rule)),
                    f"regra curinga em 'allow' libera a ferramenta inteira: {rule}",
                )
            )
    return found


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", nargs="?", type=Path, default=DEFAULT)
    args = parser.parse_args(argv)
    utf8_output()
    if not args.path.is_file():
        print(f"arquivo inexistente: {args.path}", file=sys.stderr)
        return 2
    return report(check_file(args.path), f"contrato 2 ok: {rel(args.path)} válido.")


if __name__ == "__main__":
    sys.exit(main())
