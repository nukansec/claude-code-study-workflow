---
description: Gera o resumo padronizado de uma aula e converte para PDF
argument-hint: <arquivo(s) ou data/número da aula>
---

Gere o resumo da aula a partir de: $ARGUMENTS

1. Identifique a disciplina pela pasta em que o material está (ou pela pasta atual).
2. Reúna todas as fontes da mesma aula: slide em `01_aulas/` e, em `02_anotacoes_brutas/`, o `_digitado.md`, o `_manuscrito.pdf` e a `_manuscrito_transcricao.md`.
3. Se houver PDF manuscrito sem transcrição, transcreva primeiro seguindo "Anotações manuscritas" do `CLAUDE.md`. Se a transcrição tiver trechos `[ilegível]` em fórmulas, liste-os e pergunte antes de continuar.
4. Escreva o resumo seguindo exatamente "Geração de resumos" do `CLAUDE.md`, convertendo as marcas à caneta conforme a tabela.
5. Salve em `04_resumos_md/` da disciplina, sem sobrescrever arquivo existente. No frontmatter, preencha `revisao_d7` e `revisao_d30` (data da aula + 7 e + 30 dias), conforme "Revisão espaçada" do `CLAUDE.md`.
6. Converta para `05_resumos_pdf/` com o comando Pandoc do `CLAUDE.md`.
7. Ao final, informe só o caminho dos arquivos gerados e as pendências que ficaram no resumo.
