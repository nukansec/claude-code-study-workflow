# Fluxo de Estudo — Galaxy Book6 Pro + Tab S10 FE+

> **Tablet escreve. Notebook organiza. Samsung Notes é a ponte. A pasta do computador é o arquivo final.**

## Regras de ouro

1. **1 aula = 1 nota = 1 PDF.**
2. **Exporte no mesmo dia.** Nota que fica só no Samsung Notes não existe para o Claude.
3. **Transcreva antes de resumir** e confira as fórmulas.
4. **`?` vira pendência.** Toda dúvida marcada precisa sair resolvida até a semana seguinte.
5. **Conta e diagrama à caneta; código e definição no teclado.**

## Marcas à caneta

| Marca | Significa |
|---|---|
| `?` na margem | dúvida → Pendências |
| `!` ou retângulo | conceito-chave / cai na prova |
| linha horizontal | troca de assunto |
| `→` | relação / consequência |
| `*` | revisar no livro |

---

## 0. Preparação (uma vez)

- Mesma conta Samsung nos dois aparelhos, sincronização do Samsung Notes ligada.
- No Samsung Notes, uma **pasta por disciplina**: `PE`, `CN`, `Redes`, `SB`.
- Título de toda nota: `2026-11-04 aula 13` (data + número da aula). Disciplina sem aulas numeradas: só `2026-11-04 aula`.
- Nos nomes de arquivo abaixo, `_NN` é o número da aula; sem número, omita o `_NN` (ex.: `2026-11-05_aula_digitado.md`).
- Ative **Quick Share**, **Multi Control** (mouse e teclado do notebook no tablet) e **Second Screen** (tablet como segunda tela).

## 1. Antes da aula (2 min)

- Baixe o slide da aula para `01_aulas/`.
- Mande para o tablet (Quick Share) e, no Samsung Notes, **importe o PDF** dentro da pasta da disciplina, já com o título padrão.
- Sem slide? Crie uma nota em branco com o título padrão.

## 2. Durante a aula

| Tablet | Notebook |
|---|---|
| Escrever **por cima do slide**: contas, exemplos, setas, diagramas | `02_anotacoes_brutas/YYYY-MM-DD_aula_NN_digitado.md` |
| Usar as marcas (`?`, `!`, `*`) | Definições ditadas, avisos de prova, datas, código, links |

- Matéria de conta (PE, Cálculo Numérico): **tablet principal**, notebook só para avisos.
- Matéria de código ou conceito (SB, Redes): **notebook principal**, tablet para diagramas.

## 3. Mesmo dia, depois da aula (10 min)

1. No notebook, abra a nota no **Samsung Notes** (já sincronizada) → **Salvar como arquivo → PDF** → salve em
   `02_anotacoes_brutas/YYYY-MM-DD_aula_NN_manuscrito.pdf`.
   *(Se o app do notebook não exportar, exporte no tablet e mande por Quick Share; depois mova o arquivo de Downloads.)*
2. Abra o terminal na pasta da disciplina e rode `claude`.
3. `/transcrever` → confira os trechos marcados como incertos e corrija o `_transcricao.md`.
4. `/resumo aula NN` (ou `/resumo YYYY-MM-DD` se a aula não tiver número) → gera o `.md` em `04_resumos_md/` e o PDF em `05_resumos_pdf/`.

## 4. Estudo sozinho (ciclo de cada sessão)

1. **Revisar (tablet):** importe o resumo de `05_resumos_pdf/` no Samsung Notes e marque o que não ficou claro com `?`.
2. **Praticar (tablet):** resolva a lista à mão, uma nota por lista. Exporte para `03_listas_e_provas/lista_NN_resolucao_manuscrito.pdf`.
3. **Corrigir (notebook):** no Claude Code aberto na pasta da disciplina, peça para corrigir `lista_NN_resolucao_manuscrito.pdf`; ele aponta os erros sem dar a resposta pronta.
4. **Aprofundar:** use o **Second Screen** com o livro de `06_livros_referencia/` aberto no tablet enquanto digita ou programa no notebook (ou o contrário).
5. **Sessão sem aula:** nota `YYYY-MM-DD_estudo_assunto`, exportada para `02_anotacoes_brutas/`.
6. **Revisão D+7 e D+30 (bloco Coringa):** na D+7, 5 min de página em branco com os tópicos da aula e depois 2–3 exercícios do resumo; na D+30, só exercícios. Marque `☑` no frontmatter (regra no `CLAUDE.md`).

## 5. Fechamento semanal (sexta, 16h)

- Rode `/fechamento` no Claude Code aberto em `Documents`. Ele confere se cada aula da semana tem `_manuscrito.pdf`, transcrição e resumo, lista as pendências abertas e as revisões D+7/D+30 vencidas, e monta o plano da semana seguinte.
- Resolva ou leve as pendências para o professor ou monitor.

## 6. Antes da prova

- No Claude Code, na pasta da disciplina: **quiz e flashcards** a partir dos resumos das aulas cobradas.
- Refaça à mão as questões das listas que você errou.
- Monte uma folha de consulta: `/resumo` com o tema *"folha de consulta, aulas X a Y"*.

---

## Comandos no terminal

| Comando | Faz |
|---|---|
| `claude` (dentro da pasta da disciplina) | abre o Claude com as regras do `CLAUDE.md` |
| `/transcrever` | transcreve todos os manuscritos sem transcrição |
| `/resumo aula 13` | junta slide + digitado + manuscrito e gera o resumo e o PDF |
| *"organize os PDFs soltos"* | classifica arquivos nas pastas 00–06 |
