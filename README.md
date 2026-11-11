# claude-code-study-workflow

[![ci](https://github.com/nukansec/claude-code-study-workflow/actions/workflows/ci.yml/badge.svg)](https://github.com/nukansec/claude-code-study-workflow/actions/workflows/ci.yml)

> **EN —** A Claude Code setup that turns handwritten lecture notes (tablet PDFs) into structured study summaries with exercises and answer keys, schedules spaced reviews, and runs a weekly review that lists overdue work and plans the next week. Security rules are enforced as **permissions** (deny rules), not only as prompt instructions. Docs are in Brazilian Portuguese.

Configuração do Claude Code que uso para estudar na graduação (Ciência da Computação, UFG), em cursos livres e em concurso. Ela:

- **transcreve** anotações manuscritas (PDF do Samsung Notes) para Markdown, marcando o que ficou ilegível em vez de inventar;
- **gera resumos padronizados** (definições, aplicações, 6–10 exercícios com origem marcada e gabarito em página separada) e o PDF para resolver no tablet;
- **agenda revisões espaçadas** (D+7/D+30 na graduação; D+1/D+7/D+30 nos cursos) e recuperação ativa;
- **faz o fechamento semanal** (`/fechamento`): atrasos, pendências de todas as frentes, revisões vencidas, prazos de 14 dias e o plano da semana seguinte;
- **bloqueia** a leitura de segredos e credenciais pela camada de permissão do harness.

## Arquitetura

```text
~/.claude/CLAUDE.md            camada 1: quem sou, como trabalhar, regras de segurança
_central/AGORA.md              camada 2: estado atual (prazos, frentes, pendências)
<area>/CLAUDE.md               camada 3: regras da área (pastas, nomes, fontes)
<area>/.claude/commands/*.md   fluxos repetíveis da área (/resumo, /modulo, ...)
<raiz>/.claude/settings.json   permissões: allow mínimo + deny de segredos
templates/                     modelos compartilhados (resumo, contexto, cabeçalho LaTeX)
```

- **Uma fonte da verdade por camada.** O específico fica perto do trabalho; o geral, no global. O Claude Code carrega o `CLAUDE.md` global e o de cada pasta acima da pasta atual.
- **Instrução × permissão:** o `CLAUDE.md` explica; o `settings.json` impõe. Ver [ADR-0001](docs/adr/0001-instrucao-vs-permissao.md).
- **Humano no laço:** os comandos que alteram estado (`/fechamento`, renomeações) propõem e só escrevem com OK, e nunca sobrescrevem arquivos (`mv -n`).

## Estrutura deste repositório

| Pasta | Conteúdo |
|---|---|
| `commands/graduacao/` | `/transcrever`, `/resumo` → copiar para `<disciplinas>/.claude/commands/` |
| `commands/cursos/` | `/novo-curso`, `/bloco`, `/modulo`, `/revisar` → `<cursos>/.claude/commands/` |
| `commands/raiz/` | `/fechamento` → `.claude/commands/` da pasta raiz de documentos |
| `templates/` | modelo de resumo, cabeçalho LaTeX (`\linhas{N}`), modelo de contexto, `CLAUDE.md` de graduação, cursos e concurso |
| `settings/` | `settings.example.json` com as regras allow/deny |
| `docs/` | [arquitetura](docs/arquitetura.md), fluxo de estudo (tablet → notebook → resumo) e ADRs |
| `scripts/` | validadores dos contratos (frontmatter, permissões, privacidade) |
| `tests/` | testes dos validadores, com fixtures fictícias que passam e que falham |

## Como usar

1. Copie os comandos e templates para as suas pastas, conforme a tabela acima, e adapte os `CLAUDE.md`.
2. Instale Pandoc e uma distribuição LaTeX com `xelatex` para gerar os PDFs.
3. Abra o `claude` na pasta da área e use os comandos; na pasta raiz, rode `/fechamento` toda sexta.

## Segurança e privacidade

- `permissions.deny` cobre `.env`, `*.tfvars`, chaves, certificados, `.ssh`, `.aws` e arquivos de credenciais; o `find` só é liberado sem `-delete`/`-exec`.
- Pastas com dados de terceiros (ex.: saúde) são marcadas no `CLAUDE.md` da área, e os comandos não leem conteúdo delas.
- Este repositório é uma **cópia sanitizada**: sem nomes de terceiros, caminhos pessoais ou dados de projetos. Ver as limitações no ADR-0001.

## Desenvolvimento

A configuração é tratada como código: cada regra tem um contrato validado em `scripts/` e testado em `tests/`.

| Contrato | Garante |
|---|---|
| Comandos | todo `commands/**/*.md` tem `description` e, se usa `$ARGUMENTS`, `argument-hint` |
| Permissões | o `deny` cobre `.env`, `*.tfvars`, `*.pem`, `*.key` e `find -exec`/`-delete`; o `allow` não tem curinga |
| Privacidade | nenhum arquivo tem caminho de usuário, e-mail ou termo da lista local `.privacy-terms.txt` ([ADR-0002](docs/adr/0002-gate-de-privacidade-local.md)) |

Requisitos: Python 3.12, GNU Make, Node (para o `npx markdownlint-cli2`).

```bash
make setup   # cria a .venv com as versões fixadas
make check   # ruff + markdownlint + pytest + os três contratos
make hooks   # pre-commit: gitleaks + contratos a cada commit
```

O CI (GitHub Actions) roda o mesmo `make check` e o gitleaks no histórico completo.

## Limitações conhecidas

- O deny de leitura não cobre um `cat` executado pelo shell; o próximo passo é sandbox ou hook `PreToolUse`.
- No CI, o gate de privacidade checa só os padrões genéricos (caminhos e e-mails); os termos pessoais são checados no pre-commit do autor (ver ADR-0002).
- Os comandos assumem o fluxo Samsung Notes → PDF; outro app de notas exige ajustar o `/transcrever`.
