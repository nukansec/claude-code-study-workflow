---
description: Fechamento semanal — atrasos, pendências abertas, revisões vencidas, prazos e plano da próxima semana
argument-hint: "[data de referência; vazio = hoje]"
---

Faça o fechamento semanal com referência em: $ARGUMENTS (vazio = hoje). Até o passo 7, só leitura.

**Período:**

- Pode rodar na sexta, no sábado ou no domingo.
- "Esta semana" = da segunda-feira anterior até hoje.
- O plano vale para a próxima segunda a domingo. Se rodar no sábado ou no domingo, inclua no plano o que ainda dá para fazer no fim de semana atual.

1. **Contexto.** Leia `_central/AGORA.md` e o cronograma vigente apontado em `_central/indice_estudos.md`. Diga em que fase do cronograma estamos.
2. **UFG** (`<graduacao>/<semestre atual>/*/`):
   - aulas da semana sem `_manuscrito.pdf`, transcrição ou resumo (compare os nomes em `02_anotacoes_brutas/` e `04_resumos_md/`);
   - pendências `- [ ]` abertas nos resumos, por disciplina, destacando as com mais de 7 dias (regra: `?` resolvida até a semana seguinte);
   - revisões `revisao_d7` / `revisao_d30` com `☐` e data até hoje + 7.
3. **Cursos Online** (`<cursos>/*/PROGRESSO.md`): revisões D+1/D+7/D+30 vencidas ou da próxima semana, pendências abertas e módulo em andamento parado há mais de 7 dias.
   **Concurso** (`<concurso>/material_de_estudo/`): linhas dos `caderno_de_erros.md` com D+7 vazio e data de 7 ou mais dias atrás; placar das baterias e dos simulados da semana (tópicos com menos de 70% de acerto).
4. **Pendências abertas (obrigatório; liste todas, sem resumir nem filtrar).** Varra estas fontes e mostre cada item com a fonte (`arquivo:linha`):
   - `_central/AGORA.md`: a seção "Pendências gerais", todo `[preencher]` e todo `[a confirmar]`;
   - o cronograma vigente: a seção "Pendências deste cronograma" (itens `- [ ]`) e todo `[a confirmar]` / `(prov.)` cuja data já tenha passado ou caia nos próximos 14 dias;
   - todo `CLAUDE.md` de `<projetos>/*`, `<carreira>/**`, `<graduacao>/**` e `<pessoal>/**` (ignore `.venv/`): linhas com "Pendência" na seção 5 e todo `[preencher]`;
   - `<plano de estudo>/*.md` e `<concurso>/**/*.md`: itens `- [ ]`.

   Agrupe por frente. Marque com ⚠ o que tem data nos próximos 7 dias ou já venceu. Não omita item por parecer pequeno: a lista completa é o objetivo deste passo.
5. **Prazos dos próximos 14 dias:** `AGORA.md`, cronograma (inclusive a tabela de eventos) e as seções 4–5 dos `CLAUDE.md` das frentes. Lembre os prazos recorrentes listados no `AGORA.md` (ex.: frequência mensal de bolsa).
6. **Entregue no chat:**
   - **Atrasado:** o que fazer primeiro, em ordem.
   - **Pendências abertas:** a lista completa do passo 4.
   - **Revisões da semana:** data e item.
   - **Prazos (14 dias).**
   - **Plano da próxima semana:** a semana-tipo da fase atual, com os blocos Coringa já preenchidos com os atrasos e as pendências ⚠. Se houver prova da UFG, troque os blocos do concurso de seg–qui pela disciplina da prova.
   - **Atualizações propostas:** diff curto no `AGORA.md` e itens resolvidos que podem ser marcados `[x]` ou removidos.
7. **Pergunte antes de escrever:** (a) salvar o relatório em `_central/revisoes/AAAA-MM-DD_Fechamento_Semanal.md`; (b) aplicar as atualizações propostas.

Regras:

- Não abra `.env`, `*.tfvars`, chaves ou credenciais.
- Em pastas marcadas como sensíveis no `CLAUDE.md` da área (ex.: projeto com dados de saúde), leia só `CLAUDE.md`, `INDICE.md` e atas.
- Não invente. Se um arquivo não existir ou não puder ser lido, diga qual.
