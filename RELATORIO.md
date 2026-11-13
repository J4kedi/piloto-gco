# Relatório do piloto

Escreva sem nome de empresa, de pessoa ou de cliente, e sem código, URL ou IP. A evidência com dado da empresa fica fora deste repositório; aqui entra só o que o termo de autorização permitir divulgar.

## 1. Período e quem executou

- Período: [PREENCHER - autores]
- Piloto real, projeto e mudança executada, descritos sem identificar a empresa: [PREENCHER - autores]
- Piloto real, quem fez a mudança e quem auditou (Autor A ou Autor B): [PREENCHER - autores]
- Autorização da empresa (data do termo e o que ele permite divulgar): [PREENCHER - autores]
- Simulação, Autor A (Desenvolvedor(a) e Responsável por configuração): [PREENCHER - autores]
- Simulação, Autor B (Solicitante, Revisor(a) e Aprovador emergencial; conferências da auditoria): [PREENCHER - autores]
- Repositório: [PREENCHER - autores]

## 2. O que foi executado e o que não ocorreu

### Piloto real

Etapas do `EXECUCAO.md`.

| Etapa | Resultado | Artefato | Data | Executado? | Onde está a evidência |
|---|---|---|---|---|---|
| Preencher o plano | GCO 1 | Plano de Gerência de Configuração | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| Conferir o repositório e criar a branch | GCO 2 | Procedimento de repositórios, branches, versões e releases | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| Implementar, revisar e integrar | GCO 4 e GCO 2 | Orientação de commits; Procedimento | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| Criar a baseline | GCO 3 | Definição de baseline | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| Liberar, verificar e registrar | GCO 2 e GCO 4 | Procedimento; registro de liberação; nota de incidente | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| Auditar com o checklist | GCO 5 | Checklist de auditoria de configuração | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |

### Simulação (complemento)

| Cenário | Complementa | Data | Executado? | Observação |
|---|---|---|---|---|
| C1 Mudança normal | GCO 2, 3 e 4 | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| C2 Revisão reprovada | GCO 2 | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| C3 Commit direto | GCO 2 e 5 | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| C4 Mudança emergencial | GCO 2 | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| C5 Falha na liberação | GCO 3 e 4 | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| C6 Serviço fora da lista | GCO 1 e 5 | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| C7 Auditoria e restauração | GCO 5 | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| Script avulso | GCO 4 | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |

O que não ocorreu, no piloto real e na simulação, e por quê: [PREENCHER - autores]

## 3. Critérios

Situação: atendido, não atendido ou sem ocorrência. O critério de sucesso de cada artefato e a situação dele estão nas fichas (`fichas/GCO1.md` a `fichas/GCO5.md`).

| Critério da simulação | Situação | Evidência |
|---|---|---|
| Cada cenário percorre o caminho previsto | [PREENCHER - autores] | [PREENCHER - autores] |
| Cada mudança tem solicitação, decisão, alteração identificada, evidência de teste e referência de liberação | [PREENCHER - autores] | [PREENCHER - autores] |
| A auditoria detecta os desvios de C3 e C6 | [PREENCHER - autores] | [PREENCHER - autores] |
| A restauração termina com os dados conferidos | [PREENCHER - autores] | [PREENCHER - autores] |

## 4. Indicadores da simulação

Fonte: `registros/indicadores.md`, gerado por `python indicadores/indicadores.py` a partir de `registros/` e da coleta `python indicadores/indicadores.py coletar`.

- Data da coleta: [PREENCHER - autores]
- Divergências entre planilha, log e histórico: [PREENCHER - autores]
- Leitura dos indicadores: [PREENCHER - autores]
- Adesão: [PREENCHER - autores]
- Dificuldades: [PREENCHER - autores]
- Exceções: [PREENCHER - autores]
- Tempo gasto nas tarefas de controle: [PREENCHER - autores]

## 5. Avaliação dos resultados do piloto

Uma linha por resultado de GCO, a partir das fichas. O ajuste é o que muda na nova versão do TO-BE.

| Resultado e artefato | O que foi proposto | O que foi usado | O que não funcionou | Ajuste |
|---|---|---|---|---|
| GCO 1: Plano de Gerência de Configuração | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| GCO 2: Procedimento de repositórios, branches, versões e releases | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| GCO 3: Definição de baseline | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| GCO 4: Orientação de commits | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| GCO 5: Checklist de auditoria de configuração | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |

Ajustes que não cabem num só resultado (fluxo, funções, ferramenta): [PREENCHER - autores]

Indicadores de GC do piloto real (contagem do checklist por bloco e do histórico; `EXECUCAO.md`, "Indicadores"): [PREENCHER - autores]

Entrevistas de validação feitas (data e função de quem respondeu; `ENTREVISTA.md`): [PREENCHER - autores]

## 6. Limites

Limites declarados do kit: ver `README.md`, "Limites declarados".

Limites observados na execução: [PREENCHER - autores]

## 7. Parecer do avaliador externo

[PREENCHER - autores]
