# Ciência da Computação (UFG) — regras para o Claude Code

## Estrutura de cada disciplina (`<ano>_<semestre>/<disciplina>/`)

- `00_plano_de_ensino/` — plano de ensino, ementa, bibliografia
- `01_aulas/` — slides e materiais do professor
- `02_anotacoes_brutas/` — anotações pessoais, scans manuscritos
- `03_listas_e_provas/` — listas de exercícios e provas
- `04_resumos_md/` — resumos gerados (saída em Markdown)
- `05_resumos_pdf/` — resumos convertidos via Pandoc
- `06_livros_referencia/` — livros da bibliografia (básica e complementar) baixados

PDFs soltos na raiz da disciplina devem ser classificados nessas pastas. Use `mv -n` (nunca sobrescreva) e relate qualquer arquivo estranho.

Se uma disciplina nova não tiver essa estrutura, crie as sete pastas antes de mover qualquer arquivo.

## Livros de referência

- Antes de mover um livro para `06_livros_referencia/`, confira se ele consta na bibliografia básica, complementar ou nos livros-texto do plano de ensino em `00_plano_de_ensino/`.
- Livro que não está no plano de ensino: não mova; deixe na raiz e avise (pode ter sido salvo na disciplina errada).
- Exceção: livro recomendado diretamente pelo professor fica em `06_livros_referencia/` mesmo fora do plano. Ex.: um livro indicado em aula que não está na bibliografia.
- Edição diferente da listada no plano: mova normalmente, mas mencione a diferença.
- Os livros servem de fonte complementar para os resumos: quando o material da aula for raso ou ambíguo, consulte o capítulo correspondente e cite livro e capítulo no resumo.

## Anotações pessoais (`02_anotacoes_brutas/`)

Padrão de nomes (uma aula = um arquivo de cada tipo):

- `YYYY-MM-DD_aula_NN_digitado.md` — notas digitadas no notebook durante a aula
- `YYYY-MM-DD_aula_NN_manuscrito.pdf` — nota do Samsung Notes (tablet) exportada em PDF, geralmente escrita por cima dos slides
- `YYYY-MM-DD_aula_NN_manuscrito_transcricao.md` — transcrição gerada pelo Claude
- Disciplina sem aulas numeradas: omita o `_NN` e use só a data (ex.: `YYYY-MM-DD_aula_digitado.md`, `YYYY-MM-DD_aula_manuscrito.pdf`). Não invente número.
- Estudo fora da aula: `YYYY-MM-DD_estudo_assunto_manuscrito.pdf`
- Resolução de lista à mão: vai em `03_listas_e_provas/` como `lista_NN_resolucao_manuscrito.pdf`

Arquivos exportados com nome fora do padrão (ex.: `Notas_241104_1032.pdf`): proponha o nome correto com base na data e no conteúdo e renomeie com `mv -n`.

### Anotações manuscritas

- PDFs do Samsung Notes guardam a escrita como traço, não como texto: `pdftotext` volta vazio. Leia as páginas como imagem (no máximo 20 páginas por leitura).
- Em PDF de slide anotado, separe o que é conteúdo do slide do que é anotação à mão; a anotação à mão é o que mais importa.
- Sempre **transcreva antes de resumir**: gere `<nome>_transcricao.md` ao lado do PDF, com fórmulas em LaTeX, e use `[ilegível]` (ou `[?: leitura provável]`) quando não tiver certeza. Nunca invente o que não conseguiu ler.
- Se a transcrição já existir, use-a em vez de reler o PDF (ela pode ter sido corrigida à mão).
- Marcas que eu uso à caneta:

| Marca | Significado | Destino no resumo |
|---|---|---|
| `?` na margem | dúvida | item em *Pendências/Próximos Passos* |
| `!` ou retângulo em volta | conceito-chave / cai na prova | destaque em *Definições-Chave* |
| linha horizontal | troca de assunto | nova subseção |
| `→` | relação / consequência | manter a relação no texto |
| `*` | revisar no livro | consultar `06_livros_referencia/` e citar capítulo |

## Geração de resumos

- Junte as fontes da mesma aula (slide de `01_aulas/`, `_digitado.md` e `_manuscrito_transcricao.md` de `02_anotacoes_brutas/`) e grave o resumo em `04_resumos_md/`. Se houver só o PDF manuscrito, transcreva primeiro.
- Nome: `YYYY-MM-DD_resumo_assunto_da_aula.md` — minúsculas, sem acentos, `_` entre palavras. A data é a da aula, se identificável; senão, a de hoje.
- Estrutura, exercícios, gabarito e layout para o tablet: seguir `templates/MODELO_resumo-de-estudo.md`. Aqui, no frontmatter, `area` se chama `disciplina`.
- Fontes dos exercícios, nesta ordem:
  1. `03_listas_e_provas/` (listas e provas antigas da disciplina);
  2. livros de `06_livros_referencia/` (citar livro, edição, número e página);
  3. exercícios propostos.
- Tabelas para comparações; código sempre em blocos com linguagem (`` ```python ``, `` ```c ``, `` ```bash ``).
- Matemática em LaTeX (`$...$`, `$$...$$`), compatível com Pandoc.
- Tom técnico e direto, sem introduções.

## Revisão espaçada (D+7 e D+30)

- Todo resumo novo leva no frontmatter, a partir da data da aula:

  ```yaml
  revisao_d7: "☐ AAAA-MM-DD"
  revisao_d30: "☐ AAAA-MM-DD"
  ```

- **D+7:**
  1. Recuperação ativa: 5 min de página em branco no tablet, escrevendo de memória os tópicos da aula, sem consultar nada. Se quiser correção, exporte como `02_anotacoes_brutas/YYYY-MM-DD_aula_NN_recuperacao_d7.pdf` (a data é a da aula) e peça para comparar com o resumo, no formato Acertou / Faltou / Corrigir.
  2. Depois, refaça de memória 2–3 exercícios do resumo, sem olhar o gabarito.
- **D+30:** 2–3 exercícios diferentes dos da D+7 e conferência dos `?` daquela aula.
- Feito: trocar `☐` por `☑`.
- Não há D+1: o `/resumo` no mesmo dia já cumpre esse papel.
- As revisões entram no bloco Coringa do cronograma; o `/fechamento` (rodado em `Documents`) lista as vencidas.
- Resumos antigos sem esses campos: só recebem as datas se eu pedir.

## Correção de listas, quiz e flashcards

- Tudo no Claude Code aberto na pasta da disciplina (não há projeto da graduação no claude.ai).
- Correção de resolução manuscrita (`03_listas_e_provas/lista_NN_resolucao_manuscrito.pdf`): aponte onde está o erro e por quê, **sem dar a resposta pronta**; dê a resposta só se eu pedir.
- Quiz e flashcards antes da prova: a partir dos resumos das aulas cobradas; perguntas primeiro, respostas depois que eu responder.

## Conversão para PDF

```bash
pandoc 04_resumos_md/<arquivo>.md -f markdown+lists_without_preceding_blankline -H "templates/resumo_cabecalho.tex" -o 05_resumos_pdf/<arquivo>.pdf --pdf-engine=xelatex -V monofont=Consolas -V geometry:margin=2cm
```

- Motivo das opções e local de instalação: ver o modelo de resumo. Se as ferramentas não estiverem no PATH da sessão, use o caminho completo.
- Se o Pandoc ou o xelatex não estiverem instalados, avise e mantenha apenas o `.md`.

## Ao terminar

Liste os arquivos criados ou movidos, em uma linha cada.
