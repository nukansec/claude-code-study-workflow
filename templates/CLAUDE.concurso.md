# CLAUDE.md — Concurso `<órgão>` (`<cargo>`)

> Modelo de `CLAUDE.md` para a pasta de um concurso. Preencha os `<campos>`.
> Contexto global: `~/.claude/CLAUDE.md`. Estado geral: `_central/AGORA.md`.

## 1. O projeto

- Banca: `<banca>`. Edital: `<nº/ano>`, retificações em `edital/`.
- Cargo: `<código – nome>`. **Prova: `<data>`**. Convocação (local e horário): `<data>`.
- Estrutura da prova: `<disciplinas, nº de questões, pesos, discursiva>`.

## 5. Decisões e pendências

- AAAA-MM-DD — `<pendência>`.

## 6. Regras deste projeto — método de estudo

Concurso se estuda por **questões da banca**: a teoria entra só para destravar a questão.

**Ciclo de cada tópico do edital:**

1. **Teoria curta:** resumo em `templates/MODELO_resumo-de-estudo.md`, com exercícios priorizando `[prova antiga]` da mesma banca (órgão, ano e número da questão). Sem prova antiga, `[proposto]` no estilo da banca.
2. **Bateria de questões:** 15–30 questões do tópico, cronometradas. Placar em `questoes/AAAA-MM-DD_<topico>.md` (acertos/total e tempo).
3. **Caderno de erros:** todo erro, chute certo ou dúvida vai para `caderno_de_erros.md` da matéria:

   | data | questão (fonte) | assunto | tipo do erro | regra para não errar | D+7 |
   |---|---|---|---|---|---|

   Tipos: conceito · leitura/pegadinha · lei seca · cálculo · chute.
4. **Revisão:** caderno de erros na D+7. Na semana da prova, revisar **só** os cadernos de erros e a lei seca.

**Simulados:** prova completa no horário real. Em `simulados/AAAA-MM-DD_simulado.md`, registrar o placar por disciplina, o tempo e as 5 disciplinas com mais erros.

**Discursiva:** 1 por semana na reta final, à mão e cronometrada. A correção usa esta rubrica:

- diagnóstico;
- solução;
- justificativa com norma ou boa prática;
- riscos;
- clareza e norma-padrão.

O Claude aponta o que faltou sem reescrever o texto.

**Legislação:** lei seca + questões; todo resumo cita artigo e lei.

**Fontes e direitos:** enunciados sempre resumidos, com a fonte. Não copiar apostilas ou cursos pagos.

## 8. Onde está cada coisa

- `edital/` — edital e retificações.
- `material_de_estudo/<materia>/` — `resumos_md/`, `resumos_pdf/`, `questoes/`, `caderno_de_erros.md` (criar quando a matéria começar).
- `material_de_estudo/simulados/`.
