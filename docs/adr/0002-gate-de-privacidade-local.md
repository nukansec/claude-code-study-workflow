# ADR-0002 — Gate de privacidade com lista local de termos

- Status: aceito
- Data: 2026-11-10

## Contexto

Este repositório é a cópia pública e sanitizada de uma configuração pessoal. O risco principal não é um segredo clássico (token, chave), que o gitleaks já cobre, e sim **dado pessoal** que escapa na hora de copiar um arquivo da pasta real: um caminho `C:\Users\<nome>`, um e-mail, o nome de uma pessoa ou de um projeto privado.

Duas restrições:

1. A lista do que é pessoal **é ela própria um dado pessoal**. Versionar "estes são os nomes que não podem aparecer" publica exatamente esses nomes.
2. O gate precisa rodar em qualquer clone (CI, colaborador) sem depender de arquivo que só o autor tem.

## Decisão

O gate (`scripts/check_privacy.py`) tem duas partes:

- **Padrões genéricos, versionados:** caminho absoluto de usuário no Windows (inclusive escapado em JSON), Linux e macOS, e e-mail. Valem para qualquer pessoa e rodam em todo lugar, inclusive no CI.
- **Termos pessoais, locais:** `.privacy-terms.txt`, um termo por linha, no `.gitignore`. A comparação ignora maiúsculas e acentos (normalização Unicode NFKD), porque "Conceição" escrito sem acento continua identificando a pessoa. O gate também confere o **nome** dos arquivos.

Comportamento sem a lista:

| Onde | Sem `.privacy-terms.txt` | Por quê |
|---|---|---|
| `make check`, CI | aviso e segue só com os padrões | quem clona não tem a lista; o CI não pode recebê-la |
| pre-commit do autor | **falha** (`--require-terms`) | na máquina de quem tem dados a proteger, o gate não pode ser pulado em silêncio |

Outros detalhes:

- **Escopo:** `git ls-files --cached --others --exclude-standard`, isto é, versionados + novos ainda não adicionados, respeitando o `.gitignore`. Só `git ls-files` deixaria de fora tudo o que ainda não foi commitado, que é justamente o que está para vazar.
- **Placeholders permitidos:** `C:\Users\<usuario>`, `/home/<usuario>`, `%USERNAME%`, `$USER` e `~` não disparam o gate, para a documentação poder citar o padrão.
- **Saída sem o termo:** a violação diz "termo nº 3 de .privacy-terms.txt", nunca o termo. A saída do gate pode parar num log, num print ou numa issue.
- **Exceção única:** `tests/fixtures/privacy/bad/` contém violações fictícias de propósito, para os testes provarem que o gate falha. A exclusão fica em `[tool.privacy_gate]` no `pyproject.toml`, e um teste falha se ela passar a cobrir qualquer outra coisa.

## Alternativas consideradas

- **Lista de termos cifrada no repositório** (ex.: `git-crypt`, `sops`): permitiria rodar os termos no CI, mas exige gerenciar chave no GitHub Secrets e expõe o tamanho e a quantidade de termos. Complexidade alta para um repositório de documentação.
- **Hashes dos termos versionados:** sem a lista em claro, o gate teria que testar hash de toda substring de cada linha, e termos curtos (nome próprio) são fáceis de recuperar por força bruta. Dá falsa sensação de segurança.
- **Só gitleaks com regras customizadas:** o gitleaks é feito para segredos com alta entropia ou formato conhecido; nome de pessoa não tem nenhum dos dois. As regras customizadas também iriam para o `.gitleaks.toml` versionado, com o mesmo problema da restrição 1.
- **Só revisão manual:** é o que falha quando se copia rápido.

## Consequências

- O CI garante os padrões genéricos; a garantia dos termos pessoais depende do pre-commit na máquina do autor (`make hooks`). Um commit feito com `--no-verify` ou em outra máquina só passa pelos padrões genéricos. Esse risco residual é aceito.
- Falso positivo é preferível a falso negativo: um termo curto pode casar dentro de outra palavra. Se isso acontecer, o termo deve ficar mais específico (ex.: nome + sobrenome).
- Os metadados do git (autor e e-mail do commit) estão fora do alcance do gate. Neste repositório o e-mail do commit é o noreply do GitHub.
- **Pendência (E1):** o gate não lê arquivos binários. PDFs gerados pelo Pandoc podem levar autor ou caminho nos metadados; antes de versionar o primeiro PDF de exemplo, o gate precisa checar os metadados de PDF (ou o PDF precisa ser gerado sem eles).
