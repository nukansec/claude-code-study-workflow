# Cursos Online — regras para o Claude Code

Pasta de cursos livres (fora da graduação). O objetivo não é "terminar vídeos", é **fixar e aplicar** o conteúdo.

## Estrutura de cada curso (`<nome_do_curso>/`)

```text
<nome_do_curso>/
├── CLAUDE.md          ← particularidades do curso (opcional)
├── PROGRESSO.md       ← status dos módulos, revisões e pendências
├── 00_material/       ← ebook, slides, links, certificado
└── modulos/
    └── NN_<nome_do_modulo>/
        ├── anotacoes/ ← notas do tablet e página em branco (recuperação)
        └── pratica/   ← exercícios, labs, código
```

- Nomes de pastas e arquivos: minúsculas, sem acentos, `_` entre palavras; módulos numerados com dois dígitos (`01_`, `02_`).
- Cursos divididos em níveis/trilhas: `modulos/<nivel>/NN_<modulo>/`. Respeite a organização própria do curso quando ela existir; registre a escolha no `CLAUDE.md` do curso.
- Arquivos soltos: classifique nessas pastas com `mv -n` (nunca sobrescreva) e relate qualquer arquivo estranho.

## Método de estudo (ciclo de cada módulo)

1. **Assistir:** vídeo no notebook; notas curtas no tablet (Samsung Notes), com minhas palavras.
2. **Recuperar:** página em branco escrita de memória, sem consulta → exportada como `anotacoes/YYYY-MM-DD_recuperacao.pdf`.
3. **Conferir:** comparar a recuperação com o ebook/notas e apontar o que faltou ou está errado.
4. **Aplicar:** exercício ou lab em `pratica/` antes de avançar.
5. **Revisar espaçado:** D+1, D+7 e D+30 após concluir o módulo, por perguntas (não reassistindo).

## Resumo (opcional)

- O fluxo padrão **não** gera resumo: recuperação + conferência + perguntas já fazem o papel de fixação.
- Se eu pedir um resumo de um módulo, siga `templates/MODELO_resumo-de-estudo.md` (com PDF para o tablet) e salve em `modulos/NN_<modulo>/resumo/`.
- As `perguntas_revisao.md` do módulo podem entrar como fonte da seção Exercícios (origem `[proposto]`).

## Anotações manuscritas

- PDFs do Samsung Notes guardam a escrita como traço: leia as páginas como imagem (até 20 páginas por leitura).
- Use `[ilegível]` quando não tiver certeza; nunca invente.
- Marcas à caneta: `?` dúvida · `!` conceito-chave · linha horizontal = troca de assunto · `→` relação · `*` revisar no material.

## PROGRESSO.md (um por curso)

Formato fixo:

```markdown
# <Nome do curso>
- Plataforma:
- Início:
- Meta: <ex.: 2 módulos por semana / terminar até DD/MM>

| Módulo | Concluído | D+1 | D+7 | D+30 | Prática |
|---|---|---|---|---|---|
| 01_nome | 2026-11-04 | ☐ 2026-11-05 | ☐ 2026-11-11 | ☐ 2026-12-04 | ☐ |

## Pendências
- [ ] (dúvidas `?` ainda não resolvidas, com o módulo)
```

- Ao concluir um módulo, preencha as datas de revisão automaticamente.
- Ao fazer uma revisão, troque `☐` por `☑`.

## Perguntas de revisão

- Prefira perguntas que exijam explicar, comparar ou aplicar ("por que", "o que acontece se", "quando usar X em vez de Y"), não definições decoradas.
- Em cursos técnicos, inclua pelo menos uma tarefa prática curta (comando, trecho de código, cenário).
- Mostre as perguntas primeiro; dê as respostas só quando eu pedir ou depois que eu responder.

## Tom

Direto e técnico. Ao terminar uma tarefa, liste os arquivos criados ou alterados, um por linha.
