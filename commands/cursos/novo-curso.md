---
description: Cria a estrutura de pastas e o PROGRESSO.md de um novo curso
argument-hint: <nome do curso> [plataforma] [lista de módulos ou caminho do ebook]
---

Crie um novo curso a partir de: $ARGUMENTS

1. Gere o nome da pasta no padrão do `CLAUDE.md` (minúsculas, sem acentos, `_`).
2. Crie `00_material/` e `modulos/`.
3. Se eu passar a lista de módulos, ou se houver um ebook/sumário em `00_material/`, crie as pastas `modulos/NN_<nome>/anotacoes/` e `modulos/NN_<nome>/pratica/`, respeitando níveis/trilhas se existirem.
4. Crie o `PROGRESSO.md` no formato fixo, com todos os módulos na tabela e as colunas de data vazias.
5. Pergunte a plataforma e a meta se eu não informar, e crie um `CLAUDE.md` do curso só se ele tiver alguma particularidade.
6. Ao final, mostre a árvore de pastas criada.
