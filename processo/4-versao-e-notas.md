# 4. Notas da versão e registro de liberação

Notas da versão e registro de liberação são, com a Orientação de commits (`artefatos/gco4-orientacao-de-commits.md`) e a nota de incidente (`processo/6-nota-de-incidente.md`), os registros do resultado GCO 4. Este arquivo diz como eles são gerados na simulação.

## Número da versão: `vX.Y.Z`

Toda baseline tem etiqueta `vX.Y.Z` no git e Release com o mesmo nome no GitHub. Quem cria: Responsável por configuração, com `gco.mjs baseline`. O número segue a seção 3 de `artefatos/gco2-procedimento-de-repositorios-branches-versoes-e-releases.md`. Na simulação, X fica em 0, e o item fora do repositório cuja correção libera de novo a mesma versão é `infra/producao.env`.

## Criar a baseline

O que compõe a baseline, quando ela é criada e como é controlada: `artefatos/gco3-definicao-de-baseline.md`. Na simulação:

1. `node scripts/gco.mjs homologar` conferido.
2. Escreva as notas em `registros/notas-vX.Y.Z.md`, pelo modelo abaixo; o commit delas na `main` pode vir antes ou depois da baseline.
3. `node scripts/gco.mjs baseline vX.Y.Z --notas registros/notas-vX.Y.Z.md`

A baseline etiqueta o commit do último `homologar` ok e recusa se `app/`, `infra/`, `scripts/` ou `.github/` mudaram entre ele e o `HEAD`.

## Modelo das notas da versão

O que vai em cada seção:

- **O que mudou:** uma linha por demanda (`#N`) e por PR; inclua a configuração nova que a versão exige.
- **Para quem:** quem percebe a mudança (quem usa o mural, quem opera o ambiente).
- **Como voltar:** `node scripts/gco.mjs reverter` e o que mais for preciso (configuração, dados).

```markdown
## O que mudou
[PREENCHER - autores]

## Para quem
[PREENCHER - autores]

## Como voltar
[PREENCHER - autores]
```

## Registro de liberação

Depois de `verificar`, o Responsável por configuração roda `node scripts/gco.mjs registrar vX.Y.Z --demanda <n>`. O comando reescreve, a partir de `registros/execucoes.csv`, o bloco abaixo como última seção da Release, embaixo das notas. A Demanda vem de `--demanda`; o Resultado da verificação vem da última linha `verificar` daquela versão no log.

```markdown
## Registro de liberação
- Versão: vX.Y.Z
- Demanda: #N
- Commit: <hash completo>
- Imagem: sha256:...
- Liberado por: <login>
- Liberado em: AAAA-MM-DDTHH:MM:SS-03:00
- Slot: azul ou verde
- Cópia do banco: copias/antes-vX.Y.Z.db (<impressão digital>)
- Resultado da verificação: sem falha ou com falha
```

Na primeira liberação (`v0.1.0`) não há banco para copiar, e a linha fica `- Cópia do banco: nenhuma`. Não edite o bloco à mão. Se algo mudou (por exemplo, nova verificação), rode `registrar` de novo.
