# Modelo de contexto de projeto

> Base para todo `CLAUDE.md` de área ou projeto e para as instruções dos Projetos no claude.ai.

## Como as camadas se encaixam

| Camada | Claude Code | claude.ai | Muda quando |
|---|---|---|---|
| 1. Quem sou e como trabalho | `~/.claude/CLAUDE.md` | Preferências pessoais (configurações do perfil) | Raramente |
| 2. Estado atual | `_central/AGORA.md` | Arquivo do projeto "Central" | Toda semana |
| 3. Projeto | `<pasta>\CLAUDE.md` (+ `CLAUDE.local.md` em repo público) | Instruções do projeto + o mesmo `CLAUDE.md` como arquivo | A cada decisão ou entrega |

- **Uma fonte da verdade por camada.** O `CLAUDE.md` da pasta é a fonte; o claude.ai recebe uma cópia. Mudou o arquivo, suba de novo no projeto.
- O Claude Code carrega o global, depois o `CLAUDE.md` de cada pasta acima da pasta atual, e o das subpastas quando lê arquivos nelas. Por isso o específico fica perto do trabalho e o geral fica no global.
- Se você rodar o Claude Code dentro do WSL, o global fica em `~/.claude/CLAUDE.md` do Linux, não na pasta `.claude` do usuário no Windows.

---

## A. `CLAUDE.md` de área ou projeto

Limite: menos de 200 linhas. Detalhe que não é usado em toda sessão vai para arquivo à parte (`INDICE.md`, `docs/`, `GUIA_*.md`), citado aqui.

````markdown
# CLAUDE.md — <Nome do projeto>

> Fonte única de contexto deste projeto. Atualizado em AAAA-MM-DD.
> Mapa de arquivos: `INDICE.md` (se houver). Contexto global e regras gerais: `~/.claude/CLAUDE.md`.

## 1. O projeto
- O que é, para quem e por quê (2–3 linhas).
- Vínculo: bolsa | voluntário | disciplina | curso | pessoal. Período: início–fim.
- Entregas ou indicadores cobrados.

## 2. Meu papel
- O que eu faço aqui e com quem divido.

## 3. Pessoas
| Nome | Papel | Vínculo |
|---|---|---|

## 4. Estado atual
- O que anda, o que está atrasado, próximo marco com data.

## 5. Decisões e pendências
- AAAA-MM-DD — decisão ou pendência (quem, o quê).

## 6. Regras deste projeto
- Só o que não está no global: privacidade, identidade visual, autoria, normas do programa.

## 7. Rotina
- Reuniões, prazos recorrentes.

## 8. Onde está cada coisa
- Pastas, repositório, Drive.

## 9. Como o Claude trabalha aqui
- Onde salvar cada tipo de produto.
- O que atualizar neste arquivo ao concluir algo (normalmente as seções 4 e 5).
- Ao mudar o estado do projeto, atualizar também a linha dele em `_central/AGORA.md`.
````

---

## B. Repositório de código

Escolha um dos dois padrões que você já usa:

| Situação | Padrão | Exemplo |
|---|---|---|
| Repo público em que a IA pode aparecer como ferramenta de desenvolvimento | `CLAUDE.md` público (propósito, estrutura, convenções, regras de dados) + `CLAUDE.local.md` no `.gitignore` com o contexto pessoal | `<repo-publico>` |
| Repo em que o Claude não pode aparecer | `CLAUDE.md` e `.claude/` em `.git/info/exclude` (não no `.gitignore`) | `<repo-privado>` |

- Para não depender de configurar repo por repo, deixe a atribuição desligada no `~/.claude/settings.json` (se o arquivo já existir, junte com o que houver nele):

```json
{
  "attribution": { "commit": "", "pr": "" }
}
```

- Projeto novo: preencha o `Prompt-Mae_Projetos-Agenticos.md` e siga o checklist dele.

---

## C. Instruções de Projeto no claude.ai

Mesmo cabeçalho em todos os projetos; só o miolo muda. Anexe o `CLAUDE.md` da pasta como arquivo do projeto.

```text
Sou <nome>, <curso/área>, rumo a <objetivo>.
Responda em português, direto e técnico, e explique o porquê das decisões.

Projeto: <nome> — <uma linha sobre o que é>. Meu papel: <papel>.
O arquivo CLAUDE.md anexado é a fonte da verdade deste projeto. Se algo que eu
disser contradizer ele, aponte a diferença.
Pasta local: <caminho>. Quando gerar algo para eu salvar, sugira o nome no
padrão AAAA-MM-DD_Tipo_Descricao.ext e a subpasta de destino.

Regras específicas:
- <2 a 4 regras que só valem aqui>
```

---

## D. Preferências pessoais do claude.ai (valem para todas as conversas)

```text
Sou <nome>, <curso/área>, mirando <objetivo>. Português do Brasil, respostas diretas e técnicas, sem introdução.
Explique o porquê das decisões; prefiro entender a receber pronto.
Quando eu pedir código para repositório: Conventional Commits em português e
nenhuma atribuição ao Claude. Nunca peça nem use dados pessoais de terceiros.
Meus projetos do dia a dia têm um CLAUDE.md na pasta; quando ele estiver anexado,
ele é a referência.
```

---

## E. Nomes de arquivo e pasta (resumo)

| Tipo | Padrão | Exemplo |
|---|---|---|
| Pasta nova | minúsculas, sem acento, `_` | `grupo_de_estudos` |
| Documento datado | `AAAA-MM-DD_Tipo_Descricao.ext` | `2026-11-13_Ata_Reuniao-TI.md` |
| Anotação de aula | ver ``templates/CLAUDE.graduacao.md`` | `2026-11-04_aula_13_manuscrito.pdf` |
| Pasta de repositório | nome do repo no GitHub | `<repo-publico>` |
| Quarentena | `_revisar\` na raiz da área | — |
