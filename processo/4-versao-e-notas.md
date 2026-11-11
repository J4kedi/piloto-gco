# 4. Versão, notas e registro de liberação

## Número da versão: `vX.Y.Z`

Toda baseline tem etiqueta `vX.Y.Z` no git e Release com o mesmo nome no GitHub. Quem cria: Responsável por configuração, com `gco.mjs baseline`.

| Sobe | Quando | Exemplo |
|---|---|---|
| Z (correção) | Correção sem comportamento novo, inclusive emergencial. | `v0.2.0` → `v0.2.1` |
| Y (menor) | Funcionalidade nova, ou mudança que pede configuração nova para implantar (variável de ambiente, serviço na composição). | `v0.2.1` → `v0.3.0` |
| X (maior) | Mudança incompatível: rota que some ou muda de formato, banco que a versão anterior não lê. | `v0.9.0` → `v1.0.0` |

- Ao subir um número, os da direita voltam a 0. No piloto, X fica em 0.
- Correção no código sai sempre com número novo. Correção só em item fora do repositório (por exemplo, `infra/producao.env`) libera de novo a mesma versão.

## Criar a baseline

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
