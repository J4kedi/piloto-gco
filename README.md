# Piloto de gerência de configuração

Kit do piloto de um processo de gerência de configuração (resultados GCO 1 a 5 do MPS-SW 2024). O piloto é executado pelos autores num projeto real de uma empresa de software: uma mudança pequena, que passa pelos cinco artefatos propostos e termina numa auditoria de configuração. Uma simulação com aplicação de exemplo complementa o piloto nos caminhos que não se pode provocar num ambiente real, como emergência e falha na liberação.

Este README e o `EXECUCAO.md` descrevem o piloto como foi planejado. O que ocorreu (duas mudanças, em dois ciclos, a segunda com revisão registrada por um membro da equipe; simulação só com o preparo e o C3) está no `RELATORIO.md` e nas fichas. Os arquivos de `artefatos/` são a versão usada no piloto; os ajustes estão no `RELATORIO.md`, seção 5, e no "Agir" de cada ficha.

Projeto Final I, Engenharia de Software, Grupo 13.
Autores: Grupo 13, Projeto Final I, Engenharia de Software, PUCPR, 2026/2 (Autor A e Autor B).

**Para executar o piloto, comece por [`EXECUCAO.md`](EXECUCAO.md):** o passo a passo dos autores, em ordem, do termo assinado à entrega.

## O que é

- Cinco artefatos propostos, um por resultado de GCO, em `artefatos/`. São modelos genéricos, para implantar na empresa.
- O passo a passo do piloto, `EXECUCAO.md`, uma ficha PDSA por resultado de GCO, em `fichas/`, e um roteiro de entrevista de validação, `ENTREVISTA.md`.
- A simulação: uma aplicação de exemplo (mural de recados) com homologação e produção locais, em contêineres; o script `scripts/gco.mjs`, que executa homologação, baseline, liberação, reversão e restauração e grava cada execução em `registros/execucoes.csv`; sete cenários (`cenarios.md`); as regras de `processo/`, que aplicam os artefatos à aplicação de exemplo; e os modelos de issue e de pull request em `.github/`.
- Um script de indicadores da simulação, `indicadores/indicadores.py`, que lê os registros e o histórico do GitHub.
- O relatório do piloto, `RELATORIO.md`, com a avaliação por resultado de GCO.

O repositório traz os modelos e a ferramenta em branco. Registros, tempos, fichas, resultados e avaliação são preenchidos pelos autores a partir da execução.

## O que não é

- Não contém dado de nenhuma empresa: nome, código, URL, IP, dado de cliente ou nome de pessoa. O que for preenchido com dado da empresa (plano, checklist, notas, registros) fica fora deste repositório, numa pasta privada dos autores. Aqui entram as fichas e o relatório, escritos sem identificação, e só a evidência que o termo de autorização permitir divulgar.
- Não mede o efeito do processo na empresa. O piloto verifica se os artefatos são aplicáveis num projeto real e o que precisa de ajuste; o efeito é avaliado depois, na implantação nos demais projetos.
- A simulação não é o piloto. A aplicação, os dados e o ambiente dela são de exemplo.

## Artefatos propostos, por resultado de GCO

| Resultado | Artefato | Arquivo | Ficha | Simulação (complemento) |
|---|---|---|---|---|
| GCO 1, itens e níveis de controle | Plano de Gerência de Configuração | `artefatos/gco1-plano-de-gerencia-de-configuracao.md` | `fichas/GCO1.md` | C6; lista de itens em `processo/1-itens-de-configuracao.md` |
| GCO 2, sistema de gerência de configuração e mudanças | Procedimento de repositórios, branches, versões e releases | `artefatos/gco2-procedimento-de-repositorios-branches-versoes-e-releases.md` | `fichas/GCO2.md` | C1, C2, C3 e C4; classificação em `processo/2-classificacao.md` |
| GCO 3, baselines | Definição de baseline | `artefatos/gco3-definicao-de-baseline.md` | `fichas/GCO3.md` | C1 e C5 |
| GCO 4, registros | Orientação de commits, com as notas da versão e o registro de liberação (`processo/4-versao-e-notas.md`) e a nota de incidente (`processo/6-nota-de-incidente.md`) | `artefatos/gco4-orientacao-de-commits.md` | `fichas/GCO4.md` | C1, C5 e script avulso |
| GCO 5, auditorias | Checklist de auditoria de configuração | `artefatos/gco5-checklist-de-auditoria-de-configuracao.md` | `fichas/GCO5.md` | C7; roteiro em `processo/8-auditoria-e-restauracao.md` |

Os campos `[PREENCHER]` de `artefatos/` são do modelo: preenche-se a cópia usada no projeto, na pasta privada, e não o arquivo deste repositório.

## Piloto real

O piloto só começa com o termo assinado pela empresa. A mudança é pequena, do Autor A, e não toca regra de negócio nem o fluxo de implantação; o Autor B revisa e audita. O portão de entrada, o calendário, os papéis e a evidência a guardar estão em `EXECUCAO.md`. Em resumo:

| Etapa | Artefato | Resultado |
|---|---|---|
| Preencher o plano para o projeto, ou parte dele, em que está a mudança | Plano de Gerência de Configuração | GCO 1 |
| Conferir o repositório e criar a branch da mudança | Procedimento de repositórios, branches, versões e releases | GCO 2 |
| Implementar, com os commits no formato da orientação, revisar e integrar | Orientação de commits; Procedimento | GCO 4 e GCO 2 |
| Criar a baseline depois da homologação | Definição de baseline | GCO 3 |
| Liberar pela rotina da empresa, verificar e registrar | Procedimento (seção 4); registro de liberação; nota de incidente | GCO 2 e GCO 4 |
| Auditar a mudança com o checklist | Checklist de auditoria de configuração | GCO 5 |
| Avaliar por resultado e propor os ajustes | `fichas/`, `RELATORIO.md` | GCO 1 a 5 |

Etapa que não puder ser executada no prazo, como uma liberação fora da janela da empresa, é declarada na ficha e no relatório como não ocorrida.

## Simulação: preparo

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
   A etiqueta `v0.1.0` é o marco da simulação: só conta o que está em `v0.1.0..main`, e as linhas do log com versão `v0.1.0` ficam fora dos indicadores.
7. Autotestes: `node scripts/gco.mjs autoteste` e `python indicadores/indicadores.py autoteste`.

Durante a simulação:

- `registros/`, `fichas/`, `artefatos/`, `processo/`, `cenarios.md`, `README.md`, `EXECUCAO.md`, `ENTREVISTA.md`, `RELATORIO.md` e `indicadores/` entram direto na `main`. `app/`, `infra/`, `scripts/` e `.github/` só por PR.
- A baseline etiqueta o commit do último `homologar` ok e recusa se `app/`, `infra/`, `scripts/` ou `.github/` mudaram entre ele e o `HEAD`; commit em `registros/`, `fichas/` e afins não atrapalha.
- Portas publicadas só em `127.0.0.1`: 8080 (produção) e 8081 (homologação), ajustáveis por `PORTA_PROD` e `PORTA_HOMOLOG`.
- `liberar` e `restaurar` mostram no terminal um aviso de recurso experimental do `node:sqlite`; é inofensivo.
- As planilhas `registros/tarefas-autor-a.csv`, `registros/tarefas-autor-b.csv` e `registros/scripts-avulsos.csv` usam `;` e UTF-8 com BOM, formato em que a planilha em português abre e salva.

## Simulação: comandos

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

## Simulação: indicadores

Os indicadores descrevem só a simulação; o piloto real é avaliado nas fichas e no relatório. Com as planilhas e `registros/execucoes.csv` em commit na `main`:

```
python indicadores/indicadores.py coletar
python indicadores/indicadores.py
```

O primeiro grava `registros/historico.json` (foto do git e do GitHub). O segundo calcula sem rede e grava `registros/indicadores.md`: divergências entre planilha, log e histórico; os nove indicadores com numerador, denominador e fonte; e os apoios para a análise (caminho percorrido × previsto, os cinco elementos por mudança, minutos nas tarefas de controle). Denominador zero sai como "sem ocorrência".

## Simulação: cenário → tarefas → artefato → indicador

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
| `artefatos/` | Os cinco artefatos propostos, um por resultado de GCO (modelos genéricos) |
| `processo/` | Aplicação dos artefatos à simulação: lista de itens (seção 2 do plano), classificação da mudança (seção 8 do plano), notas da versão e registro de liberação, nota de incidente, script avulso, roteiro de auditoria e restauração |
| `EXECUCAO.md` | Passo a passo do piloto para os autores: portão, calendário, papéis, evidência, indicadores e fechamento |
| `ENTREVISTA.md` | Roteiro de entrevista de validação, para quem usou o processo na empresa |
| `cenarios.md` | Simulação: caminho previsto e roteiro de cada cenário, papéis e calendário |
| `fichas/` | Uma ficha PDSA por resultado de GCO (GCO1 a GCO5) |
| `registros/` | Planilhas de tarefas, log `execucoes.csv`, notas das versões, incidentes, auditorias, scripts avulsos, indicadores |
| `indicadores/` | Script dos indicadores e dados fictícios do autoteste |
| `RELATORIO.md` | Relatório do piloto |
| Fora do repositório | `infra/producao.env`, `infra/.slots.env` e `copias/`, na máquina do Autor A; a pasta privada dos autores, com tudo o que tem dado da empresa |

## Limites declarados

- O piloto real é uma mudança pequena num projeto: mostra se os artefatos são aplicáveis e o que ajustar, não o efeito deles na empresa.
- A evidência do piloto real fica com os autores, fora deste repositório. Aqui está a avaliação que eles fazem dela.

Na simulação:

- `ativar` e `reverter` recriam o proxy: a porta pública fica fora do ar por cerca de 1 s a cada troca de slot.
- `liberar` confere só a identidade da versão (`/versao`). A saúde (`/saude`) é conferida por `verificar`, depois de `ativar`: uma falha de configuração, como a de C5, chega à porta pública antes de ser percebida.
- A `main` não tem proteção técnica, de propósito: commit direto é possível (C3), e quem o acusa é a auditoria.
- Amostra pequena: dois autores e sete cenários. Os indicadores descrevem a simulação e não se generalizam.
- Homologação e produção rodam na mesma máquina.
