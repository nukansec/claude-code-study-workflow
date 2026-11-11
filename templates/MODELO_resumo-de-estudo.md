# Modelo de resumo de estudo

> Padrão para resumos de **qualquer** área: disciplina da faculdade, curso online, concurso ou estudo próprio.
> Quando gerar: na UFG, um por aula (`/resumo`); no concurso, um por tópico do edital; nos cursos online, **só quando eu pedir** (o fluxo padrão dos cursos é recuperação + perguntas; ver ``templates/CLAUDE.cursos-online.md``).
> Uso: ler no tablet (PDF no Samsung Notes), resolver os exercícios escrevendo por cima e conferir no gabarito.
> Criado em 2026-11-10. Regras específicas de uma área (pastas, nomes, fontes) ficam no `CLAUDE.md` dela.

## Estrutura

````markdown
---
data: AAAA-MM-DD            # data da aula/módulo; senão, a de hoje
area: <disciplina | curso | tema>
topico: <tópico>
tags: [tag1, tag2]
fontes: <slide, anotação, livro e capítulo, vídeo/módulo do curso>
---

# <Tópico>

## Definições-Chave
- Bullets diretos. Tabelas para comparações.

## Aplicações/Lógica
- Algoritmos, arquiteturas, código, exemplos resolvidos (enunciado e resolução juntos).

\newpage

## Exercícios

### Fixação
**1.** `[proposto]` Enunciado de resposta escrita.

\linhas{6}

### Aplicação
**4.** `[livro]` Walpole, 8ª ed., ex. 6.7 (p. 120): enunciado resumido.

\vspace{5cm}

### Desafio
**8.** `[proposto]` Enunciado.

\vspace{5cm}

## Pendências/Próximos Passos
- [ ] Dúvidas, leituras, o que confirmar com o professor.

\newpage

## Gabarito
**1.** Resposta final. Resolução curta (os passos que importam).
**4.** Resposta. `Conferido com a resposta do livro.` / `Resolução própria.`
````

## Regras

### Exercícios

- **Quantidade:** 6–10 por resumo, em três blocos:

  | Bloco | Quantidade | O que cobra |
  |---|---|---|
  | Fixação | 2–4 | Conceito e definição |
  | Aplicação | 3–5 | Problema e cálculo |
  | Desafio | 1 | Junta tópicos ou vai além da aula |

  Tema curto pede menos exercícios; não encher por encher.
- **Outros artefatos têm quantidade própria, menor de propósito** (são checagens rápidas, não material de estudo):

  | Artefato | Quantidade | Onde está a regra |
  |---|---|---|
  | Resumo (este modelo) | 6–10 exercícios + gabarito | aqui |
  | `/modulo` (fim de módulo de curso) | 5 perguntas de revisão | `commands/cursos/modulo.md` |
  | `/bloco` (fim de aula da plataforma) | 3 perguntas | `commands/cursos/bloco.md` |
  | Pré-quiz de curso com prova objetiva | 5 de múltipla escolha | `<CLAUDE.md do curso>` |
  | Bateria de questões de concurso | por tópico, sem limite | ``templates/CLAUDE.concurso.md`` |

- **Origem obrigatória**, entre crases, no início do enunciado:
  - `[livro]`: livro, edição, número do exercício e página;
  - `[lista]`: lista da disciplina e número;
  - `[prova antiga]`: ano e questão;
  - `[proposto]`: criado pelo Claude.
- **Prioridade de fonte:** primeiro lista e prova antiga, porque são o estilo do professor; depois o livro da bibliografia; por fim exercícios propostos para cobrir o que faltar.
- **Exercício de livro:** enunciado **resumido** em poucas linhas, com os dados necessários. Não transcrever páginas do livro.
- **Estilo da avaliação:** se a prova for discursiva, incluir perguntas do tipo "explique" e "compare"; se for de cálculo, priorizar cálculo.
- **Sem pistas:** nenhuma resposta nem dica ao lado do enunciado. Tudo vai no gabarito.

### Gabarito

- Sempre a **última seção**, depois de `\newpage`.
- Cada item traz a resposta final e a resolução curta. Em perguntas discursivas, os pontos que a resposta precisa ter.
- **Números conferidos com script** (Python) antes de entrar no gabarito. Se o livro tiver resposta, comparar e registrar ("Conferido com a resposta do livro"). Em divergência, registrar as duas e explicar a diferença (ex.: arredondamento da tabela).
- Quando a resposta depender de leitura de tabela (ex.: $\Phi(z)$), dar o valor de tabela, que é o que se usa na prova, e o exato, se for diferente.
- Se não der para verificar uma resposta, marcar `[não verificado]`. Nunca inventar.

### Layout para o tablet

- `\newpage` antes de **Exercícios** e antes de **Gabarito**, para não ver a resposta sem querer.
- O espaço de resposta depois de cada exercício depende do tipo:

  | Tipo de resposta | Comando | Tamanho |
  |---|---|---|
  | **Escrita** (explique, defina, compare, justifique) | `\linhas{N}`: linhas pautadas cinza-claro, 0,94 cm entre elas | 4–5 (curta), 8–10 (média), 12–14 (com vários itens) |
  | **Conta ou desenho** (cálculo, tabela, diagrama, topologia) | `\vspace{Xcm}`: espaço em branco | 3 cm (curta), 5–6 cm (média), 7–8 cm (longa) |
  | **Misto** | Usar o que predomina | — |

- `\linhas` está definido em `templates/resumo_cabecalho.tex`, que o comando de conversão carrega com `-H`. Sem esse arquivo, o PDF não compila.
- Esses comandos são LaTeX puro, em linha própria e com linha em branco antes e depois. Só funcionam no PDF; na pré-visualização do Markdown aparecem como texto.

### Conversão para PDF

```bash
pandoc <resumo>.md -f markdown+lists_without_preceding_blankline -H "templates/resumo_cabecalho.tex" -o <resumo>.pdf --pdf-engine=xelatex -V monofont=Consolas -V geometry:margin=2cm
```

- `-H resumo_cabecalho.tex`: carrega o comando `\linhas` (pauta para resposta escrita).
- `lists_without_preceding_blankline`: sem essa extensão, uma lista logo abaixo de uma linha de texto (sem linha em branco) é colada no parágrafo anterior.
- `monofont=Consolas`: a fonte padrão de código não tem símbolos como `≈`.
- `geometry:margin=2cm`: margens menores para a tela do tablet.
- Ferramentas instaladas em 2026-11-10:
  - Pandoc em `<pasta de instalação do Pandoc>`;
  - MiKTeX em `<pasta de instalação do MiKTeX>`, com instalação automática de pacotes.
- Se faltar alguma das duas, avisar e entregar só o `.md`.

## Onde salvar

- Área com estrutura própria (ex.: disciplina da UFG): seguir o `CLAUDE.md` da área (`04_resumos_md/` e `05_resumos_pdf/`).
- Curso online: `modulos/NN_<modulo>/resumo/` (o `.md` e o `.pdf` juntos), só quando eu pedir.
- Concurso: `material_de_estudo/<materia>/resumos_md/` e `resumos_pdf/` (ver o `CLAUDE.md` do concurso).
- Outra área sem estrutura: criar `resumos_md/` e `resumos_pdf/` na pasta do tema. Nome do arquivo: `AAAA-MM-DD_resumo_assunto.md`, minúsculas, sem acentos, `_` entre palavras.
