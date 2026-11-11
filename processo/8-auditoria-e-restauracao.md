# 8. Auditoria e restauração

Mensal; no piloto, uma vez, no cenário C7. Quem audita não fez as mudanças auditadas: no piloto, o Autor B faz as conferências (papel Responsável por configuração) e o Autor A só executa a restauração. Os comandos rodam na máquina que hospeda os contêineres, na raiz do repositório, em PowerShell ou Git Bash. Na planilha, cada tarefa abaixo tem `resultado` = número de desvios, menos Testar restauração (`aprovada` ou `reprovada`).

## Checklist

### 1. Verificar baselines

```
git tag --list "v*" --sort=v:refname
gh release list
node scripts/gco.mjs situacao
```

Confira: cada versão liberada tem etiqueta e Release com notas e com o bloco "Registro de liberação"; a versão de cada slot e a da homologação, em `situacao`, têm baseline. Desvio: o que faltar.

### 2. Conferir itens de configuração

```
docker compose -p gco-prod --env-file infra/.slots.env -f infra/producao.yml config --services
docker compose -p gco-prod ps --format "table {{.Service}}\t{{.State}}"
node scripts/gco.mjs situacao
```

Regra: todo serviço que não seja `proxy` tem de ser `<nome em servicos-da-liberacao.txt>-<slot>` e constar da lista de itens (`processo/1-itens-de-configuracao.md`). Divergência: serviço fora da lista, ou nome da lista sem serviço na composição; um serviço novo por slot conta uma vez. Conte também, na lista de itens, quantos itens há (`Itens identificados`) e quantos têm tipo, responsável e nível (`Itens completos`).

### 3. Conferir registros

```
git fetch origin --tags
git log --first-parent --no-merges --date=iso --format="%h %an %ad %s" v0.1.0..origin/main -- app infra scripts .github
gh api "repos/{owner}/{repo}/commits/<hash>/pulls" --jq length
```

O `git log` lista commits de caminho controlado feitos fora de merge. Rode o `gh api` para cada hash: `0` = commit sem PR (desvio). Contraprova:

```
python indicadores/indicadores.py coletar
python indicadores/indicadores.py
```

Em `registros/indicadores.md`, leia a seção "Divergências" e o indicador 3 (mudanças diretas). Confira também se cada linha de `registros/scripts-avulsos.csv` está completa.

### 4. Testar restauração (roteiro)

1. Escolha a última versão liberada depois de `v0.1.0`; a cópia dela é `copias/antes-<versão>.db`.
2. Autor A: `node scripts/gco.mjs restaurar <última versão>`
3. Na última linha de `registros/execucoes.csv`, o comando `restaurar` tem `resultado` `ok`.
4. Abra `http://localhost:8081/recados` e confira os recados que estavam em produção antes daquela liberação.
5. Os passos 3 e 4 conferem: `aprovada`. Senão: `reprovada`, com o motivo no texto livre e uma issue aberta.

### 5. Registrar auditoria

Copie o modelo abaixo para `registros/auditorias/AAAA-MM-DD.md` e preencha. Abra uma issue para cada desvio. **Desvio tratado** = tem issue aberta com a correção ou com a decisão, e o número dela está no registro.

## Modelo do registro

- `Período`: `AAAA-MM-DD a AAAA-MM-DD` (desde a auditoria anterior; na primeira, desde a `v0.1.0`).
- `Itens identificados`, `Itens completos`, `Divergências`, `Baselines conferidas`, `Desvios encontrados`, `Desvios tratados`: números inteiros.
- `Restauração`: `aprovada` ou `reprovada`. `Versão restaurada`: `vX.Y.Z`.
- Abaixo dos campos, texto livre: cada desvio com hash, serviço ou versão, e o número da issue aberta.

```markdown
# Auditoria AAAA-MM-DD

- Período: [PREENCHER - autores]
- Itens identificados: [PREENCHER - autores]
- Itens completos: [PREENCHER - autores]
- Divergências: [PREENCHER - autores]
- Baselines conferidas: [PREENCHER - autores]
- Desvios encontrados: [PREENCHER - autores]
- Desvios tratados: [PREENCHER - autores]
- Restauração: [PREENCHER - autores]
- Versão restaurada: [PREENCHER - autores]

[PREENCHER - autores]
```
