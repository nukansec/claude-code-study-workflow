# ADR-0001 — Regras de segurança como permissão, não só como instrução

- Status: aceito
- Data: 2026-11-10

## Contexto

O `CLAUDE.md` global proíbe o agente de ler `.env`, `*.tfvars`, chaves e credenciais. Mas o `CLAUDE.md` é **instrução**: entra no contexto do modelo e depende de o modelo obedecer. Uma injeção de prompt num arquivo lido, um contexto longo ou um erro do modelo podem fazer a regra ser ignorada.

## Decisão

Cada regra de segurança existe em duas camadas:

1. **Instrução** (`CLAUDE.md`): explica o porquê e orienta o comportamento.
2. **Permissão** (`.claude/settings.json`, `permissions.deny`): o harness do Claude Code bloqueia a chamada de ferramenta antes de ela executar, independentemente do que o modelo decidir.

As regras `deny` têm precedência sobre `allow`. O `allow` cobre só comandos de leitura e de build que não causam dano (`ls`, `find`, `pandoc`). O `find` vem acompanhado de `deny` para `-delete`, `-exec`, `-execdir` e `-ok`, porque com essas opções ele vira um executor genérico.

## Alternativas consideradas

- **Só `CLAUDE.md`:** simples, mas não garante nada (defesa baseada em obediência).
- **Hook `PreToolUse` com script próprio:** mais flexível (regex no comando inteiro), mas é código a manter e testar. Fica para quando as regras `deny` não bastarem.
- **Sandbox do Claude Code:** isola também os comandos de shell; é o próximo passo para cobrir `cat .env` via Bash.

## Consequências

- O deny de `Read(...)` bloqueia as ferramentas de arquivo do agente, **não** um `cat` pelo shell. Esse risco residual está documentado e será tratado com sandbox ou hook.
- Regras de permissão valem só para sessões abertas na pasta que contém o `.claude/settings.json`. Para valer em todas as pastas, as mesmas regras devem ir para `~/.claude/settings.json`.
- Princípio aplicado: defesa em profundidade e privilégio mínimo, o mesmo raciocínio de IAM em nuvem.
