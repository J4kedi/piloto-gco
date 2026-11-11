# Piloto de gerência de configuração

Piloto de aplicabilidade de um processo de gerência de configuração (resultados GCO 1 a 5 do MPS-SW 2024), executado em simulação sobre uma aplicação de exemplo.

Projeto Final I, Engenharia de Software, Grupo 13.
Autores: [PREENCHER - autores]

## O que é

- Um processo de gerência de configuração escrito em `processo/`, com modelos de issue e de pull request em `.github/`.
- Uma aplicação de exemplo (mural de recados) com homologação e produção locais, em contêineres.
- Um script, `scripts/gco.mjs`, que executa homologação, baseline, liberação, reversão e restauração, e grava cada execução em `registros/execucoes.csv`.
- Sete cenários (`cenarios.md`) executados por dois autores em cinco ciclos de adoção gradual (G1 a G5), com uma ficha por ciclo em `fichas/`.
- Um script de indicadores, `indicadores/indicadores.py`, que lê os registros e o histórico do GitHub.

O repositório traz a ferramenta e os modelos em branco. Registros, tempos e resultados são preenchidos pelos autores durante o piloto.

## O que não é

- Não mede efeito do processo em empresa. O piloto verifica se o processo é aplicável, num ambiente simulado.
- Não contém dado de nenhuma empresa. Aplicação, dados e ambiente são de exemplo.

## Preparo

O Autor A hospeda os contêineres. Na máquina dele: Docker Desktop, Node 24, Python 3.14, git e gh autenticado (`gh auth status`). O Autor B precisa de conta no GitHub; os comandos `gh` dos roteiros também podem ser feitos pela página do GitHub.

Uma vez, na máquina do Autor A, na raiz do repositório:

1. Primeiro commit e repositório público:
   ```
   git add -A
   git commit -m "Kit do piloto"
   gh repo create <nome> --public --source . --push
   ```
2. Só merge commit (sem squash nem rebase):
   ```
   gh repo edit --enable-merge-commit --enable-squash-merge=false --enable-rebase-merge=false
   ```
3. Rótulos de classificação, com estes nomes exatos:
   ```
   gh label create normal
   gh label create risco
   gh label create emergencial
   ```
4. Autor B como colaborador com escrita (Settings → Collaborators); B aceita o convite.
5. Variáveis de produção, fora do repositório: `cp infra/producao.env.exemplo infra/producao.env` e preencha.
6. Baseline inicial `v0.1.0` e primeira liberação. Abra uma issue "Preparo do piloto" pelo modelo Demanda e escreva as notas em `registros/notas-v0.1.0.md` (modelo em `processo/4-versao-e-notas.md`).
   ```
   node scripts/gco.mjs homologar
   node scripts/gco.mjs baseline v0.1.0 --notas registros/notas-v0.1.0.md
   node scripts/gco.mjs liberar v0.1.0
   node scripts/gco.mjs ativar v0.1.0
   node scripts/gco.mjs verificar v0.1.0
   node scripts/gco.mjs registrar v0.1.0 --demanda <n>
   node scripts/gco.mjs situacao
   ```
   A etiqueta `v0.1.0` é o marco do piloto: só conta o que está em `v0.1.0..main`, e as linhas do log com versão `v0.1.0` ficam fora dos indicadores.
7. Autotestes: `node scripts/gco.mjs autoteste` e `python indicadores/indicadores.py autoteste`.

Durante o piloto:

- `registros/`, `fichas/`, `processo/`, `cenarios.md`, `README.md`, `RELATORIO.md` e `indicadores/` entram direto na `main`. `app/`, `infra/`, `scripts/` e `.github/` só por PR.
- A baseline etiqueta o commit do último `homologar` ok e recusa se `app/`, `infra/`, `scripts/` ou `.github/` mudaram entre ele e o `HEAD`; commit em `registros/`, `fichas/` e afins não atrapalha.
- Portas publicadas só em `127.0.0.1`: 8080 (produção) e 8081 (homologação), ajustáveis por `PORTA_PROD` e `PORTA_HOMOLOG`.
- `liberar` e `restaurar` mostram no terminal um aviso de recurso experimental do `node:sqlite`; é inofensivo.
- As planilhas `registros/tarefas-autor-a.csv`, `registros/tarefas-autor-b.csv` e `registros/scripts-avulsos.csv` usam `;` e UTF-8 com BOM, formato em que a planilha em português abre e salva.

## Comandos

`node scripts/gco.mjs <comando>`, na raiz do repositório, na máquina do Autor A.

| Comando | Tarefa | O que faz |
|---|---|---|
| `homologar` | Implantar em homologação | Único comando que constrói imagem, a partir do commit em `HEAD`; recusa se houver alteração não commitada em caminho controlado. Sobe a homologação (porta 8081) e confere `/saude` e `/versao`. |
| `baseline <versão> --notas <arquivo>` | Criar baseline | Exige versão `vX.Y.Z`, arquivo de notas não vazio e um `homologar` ok; recusa se a etiqueta já existir ou se houver mudança em caminho controlado entre o commit homologado e o `HEAD`. Etiqueta o commit homologado e envia a etiqueta, cria a Release com as notas, etiqueta a imagem e grava o ID dela. |
| `liberar <versão>` | Liberar em produção | Recusa se a imagem não for a gravada na baseline ou se faltar `infra/producao.env`. Copia o banco do slot ativo para `copias/` e calcula a impressão digital; sobe a versão no slot inativo; confere só a identidade (`/versao`). |
| `ativar <versão>` | Ativar nova versão | Aponta o proxy (porta 8080) para o slot que recebeu a versão. |
| `verificar <versão>` | Verificar nova versão | Pela porta pública: `/versao` igual ao commit da etiqueta e `/saude` 200. Sai com código 1 se falhar. |
| `registrar <versão> --demanda <n>` | Registrar liberação | Reescreve o bloco "Registro de liberação" da Release a partir do log. |
| `reverter` | Restaurar versão anterior | Volta o proxy para o slot anterior, que continua no ar. |
| `restaurar <versão>` | Testar restauração | Restaura `copias/antes-<versão>.db` na homologação e recalcula a impressão digital; `ok` só se for igual à gravada. |
| `situacao` | — | Slot ativo, versão em cada slot e em homologação, login do `gh`, e a comparação entre os serviços da composição de produção e `infra/servicos-da-liberacao.txt`. |
| `autoteste` | — | Asserts das funções puras. |

## Indicadores

Com as planilhas e `registros/execucoes.csv` em commit na `main`:

```
python indicadores/indicadores.py coletar
python indicadores/indicadores.py
```

O primeiro grava `registros/historico.json` (foto do git e do GitHub). O segundo calcula sem rede e grava `registros/indicadores.md`: divergências entre planilha, log e histórico; os nove indicadores com numerador, denominador e fonte; e os apoios para a análise (caminho percorrido × previsto, os cinco elementos por mudança, minutos nas tarefas de controle). Denominador zero sai como "sem ocorrência".

## Mapa: cenário → tarefas → artefato → indicador

| Cenário | Tarefas que o marcam | Artefato | Indicador |
|---|---|---|---|
| C1 Mudança normal | Fluxo inteiro, de Registrar demanda a Registrar liberação | Issue; PR com rótulo `normal`; etiqueta e Release com notas e registro; linhas do log | 2, 3, 5, 6, 9 |
| C2 Revisão reprovada | Revisar mudança (reprovada) → Corrigir mudança → Submeter pull request → Revisar mudança (aprovada) | PR com uma revisão que reprova e outra que aprova | 2 |
| C3 Commit direto | Implementar mudança direto na `main`; acusado em Conferir registros (C7) | Commit sem PR; registro de auditoria | 3, 8 |
| C4 Mudança emergencial | Aprovar emergência antes de Implementar mudança; Revisar mudança depois da liberação | Comentário `Aprovação emergencial:`; PR com rótulo `emergencial`; Release | 4, 2, 5, 6, 9 |
| C5 Falha na liberação | Verificar nova versão (com falha) → Restaurar versão anterior → Investigar causa → Registrar incidente → Corrigir configuração | Linha `reverter` no log; nota em `registros/incidentes/`; Release | 7, 5, 6, 9 |
| C6 Serviço fora da lista | Liberar em produção com serviço fora de `infra/servicos-da-liberacao.txt`; acusado em Conferir itens de configuração (C7) | `situacao`; campo `Divergências` do registro de auditoria | 1, 8 |
| C7 Auditoria e restauração | Verificar baselines → Conferir itens de configuração → Conferir registros → Testar restauração → Registrar auditoria | `registros/auditorias/AAAA-MM-DD.md`; linha `restaurar` no log | 1, 8 |
| Script avulso | Executar script avulso | `registros/scripts-avulsos.csv` | nenhum |

Todos os cenários alimentam o caminho percorrido × previsto e os minutos nas tarefas de controle, a partir das planilhas.

## Onde está cada coisa

| Caminho | Conteúdo |
|---|---|
| `app/` | Aplicação de exemplo (mural de recados), teste e Dockerfile |
| `infra/` | Composições de homologação e produção, variáveis, lista de serviços da liberação |
| `scripts/gco.mjs` | Comandos do processo |
| `.github/` | Modelos de issue (demanda) e de pull request |
| `processo/` | Regras: itens de configuração, classificação, versão e notas, nota de incidente, script avulso, auditoria e restauração |
| `cenarios.md` | Caminho previsto e roteiro de cada cenário, papéis e calendário |
| `fichas/` | Ficha de cada ciclo (G1 a G5) |
| `registros/` | Planilhas de tarefas, log `execucoes.csv`, notas das versões, incidentes, auditorias, scripts avulsos, indicadores |
| `indicadores/` | Script dos indicadores e dados fictícios do autoteste |
| `RELATORIO.md` | Relatório do piloto |
| Fora do repositório | `infra/producao.env`, `infra/.slots.env` e `copias/`, na máquina do Autor A |

## Limites declarados

- `ativar` e `reverter` recriam o proxy: a porta pública fica fora do ar por cerca de 1 s a cada troca de slot.
- `liberar` confere só a identidade da versão (`/versao`). A saúde (`/saude`) é conferida por `verificar`, depois de `ativar`: uma falha de configuração, como a de C5, chega à porta pública antes de ser percebida.
- A `main` não tem proteção técnica, de propósito: commit direto é possível (C3), e quem o acusa é a auditoria.
- Amostra pequena: dois autores, sete cenários, três dias. Os indicadores descrevem este piloto e não se generalizam.
- Homologação e produção rodam na mesma máquina.
