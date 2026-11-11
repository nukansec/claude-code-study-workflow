---
description: Transcreve anotações manuscritas (PDF do Samsung Notes) para Markdown
argument-hint: <pdf manuscrito ou pasta>
---

Transcreva as anotações manuscritas de: $ARGUMENTS
(sem argumento: todos os `*_manuscrito.pdf` de `02_anotacoes_brutas/` e `03_listas_e_provas/` da disciplina atual que ainda não têm `_transcricao.md`)

1. Se o nome do arquivo estiver fora do padrão do `CLAUDE.md`, proponha o nome correto e renomeie com `mv -n`.
2. Leia as páginas como imagem e transcreva fielmente, na ordem em que foram escritas.
3. Fórmulas em LaTeX; diagramas descritos em uma linha entre colchetes; mantenha as marcas (`?`, `!`, `→`, `*`) no texto.
4. Use `[ilegível]` ou `[?: leitura provável]` sempre que não tiver certeza. Não complete com conteúdo inventado.
5. Salve como `<nome>_transcricao.md` ao lado do PDF, sem sobrescrever.
6. Ao final, liste os arquivos gerados e cada trecho marcado como incerto, com a página, para eu conferir.
