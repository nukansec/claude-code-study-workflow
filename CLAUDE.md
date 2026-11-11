# CLAUDE.md — claude-code-study-workflow

> Contexto do Claude Code para quem trabalha **neste repositório**. Contexto pessoal do autor, se houver, fica em `CLAUDE.local.md` (gitignored).

## O projeto

Configuração do Claude Code para estudo (comandos, templates, permissões) e os validadores que mantêm essa configuração correta e sem dados pessoais. Peça de portfólio pública: o texto precisa ser legível para quem não conhece o projeto. Arquitetura em `docs/arquitetura.md`; decisões em `docs/adr/`.

## Estrutura

- `commands/`, `templates/`, `settings/`: o conteúdo distribuído. Mudanças de conteúdo são decididas pelo autor; aqui só correções de lint ou de contrato.
- `scripts/`: um validador por contrato (`validate_commands.py`, `validate_settings.py`, `check_privacy.py`) e `_common.py`.
- `tests/`: espelha `scripts/`; fixtures fictícias em `tests/fixtures/{commands,settings,privacy}/{ok,bad}/`.
- `docs/`: arquitetura, fluxo de estudo e ADRs.

## Comandos

```bash
make setup   # .venv + dependências fixadas (pip --group dev)
make check   # ruff + markdownlint + pytest + contratos 1, 2, 3
make hooks   # instala o pre-commit (gitleaks + contratos)
make secrets # gitleaks no histórico (precisa do binário no PATH)
```

`make check` precisa passar antes de qualquer commit.

## Regras

- **Dados:** só exemplos fictícios (`fulano`, `exemplo.org`, temas públicos como busca binária). Nunca caminho de usuário, e-mail, nome de terceiro ou dado de projeto privado. O gate de privacidade bloqueia; não contorne com exclusão nova no `pyproject.toml` (ver ADR-0002).
- **Segredos:** não ler `.env`, `*.tfvars`, chaves ou credenciais; o `settings.example.json` deste repo também se aplica aqui.
- **Contratos:** toda regra nova num validador entra com um caso que passa e um que falha. Fixture nova em `bad/` precisa de caso de teste (há um teste que confere isso).
- **Dependências:** versões fixadas com `==` no `pyproject.toml`; actions do GitHub fixadas por SHA de commit, com a tag no comentário.
- **Python:** 3.12, só PyYAML no runtime; ler e escrever arquivos sempre em UTF-8 explícito.
- **Git:** GitHub Flow (`feat/`, `fix/`, `docs/`), Conventional Commits em português, sem commit direto na `main`.
- **Decisão não trivial:** novo ADR em `docs/adr/NNNN-titulo.md`, no formato dos existentes.
