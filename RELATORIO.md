# Relatório do piloto

Escreva sem nome de empresa, de pessoa ou de cliente, e sem código, URL ou IP. A evidência com dado da empresa fica fora deste repositório; aqui entra só o que o termo de autorização permitir divulgar.

## 1. Período e quem executou

- Período: 13 a 16/11/2026.
- Piloto real, projeto e mudança executada, descritos sem identificar a empresa: sistema web de uma empresa de pequeno porte, mantido por uma equipe de poucos desenvolvedores. A mudança acrescentou quatro testes automatizados de casos de borda a uma regra já existente, sem alterar código de produção, regra de negócio nem implantação (classificação normal).
- Piloto real, quem fez a mudança e quem auditou (Autor A ou Autor B): o Autor A fez a mudança; a revisão cabe a um membro da equipe da empresa, porque o Autor B não tem acesso ao repositório dela; o Autor B audita por chamada.
- Autorização da empresa (data do termo e o que ele permite divulgar): termo recebido assinado em 13/11/2026. Permite citar a empresa e o produto no trabalho acadêmico e divulgar a equipe por função, os indicadores do processo de mudança e o processo modelado, sem código-fonte, credenciais, dados de clientes ou nomes de pessoas; autoriza aplicar os artefatos, em caráter de piloto, a mudanças do estudante que integra a equipe, sem alterar regra de negócio, fluxo de implantação ou produção. O revisor da equipe assinou a ciência.
- Simulação, Autor A (Desenvolvedor(a) e Responsável por configuração): [PREENCHER - autores]
- Simulação, Autor B (Solicitante, Revisor(a) e Aprovador emergencial; conferências da auditoria): [PREENCHER - autores]
- Repositório: este repositório, público, com o kit, as fichas e este relatório; a evidência com dado da empresa fica na pasta privada dos autores.

## 2. O que foi executado e o que não ocorreu

### Piloto real

Etapas do `EXECUCAO.md`.

| Etapa | Resultado | Artefato | Data | Executado? | Onde está a evidência |
|---|---|---|---|---|---|
| Preencher o plano | GCO 1 | Plano de Gerência de Configuração | 13/11 | sim; leitura do Autor B pendente em 14/11 | pasta privada; `fichas/GCO1.md` |
| Conferir o repositório e criar a branch | GCO 2 | Procedimento de repositórios, branches, versões e releases | 13/11 | sim | pasta privada; `fichas/GCO2.md` |
| Implementar, revisar e integrar | GCO 4 e GCO 2 | Orientação de commits; Procedimento | 13/11 | implementação e pull request, sim; revisão registrada e integração, não até 14/11 | plataforma da empresa; `fichas/GCO2.md` e `fichas/GCO4.md` |
| Criar a baseline | GCO 3 | Definição de baseline | — | não até 14/11: depende da integração | `fichas/GCO3.md` |
| Liberar, verificar e registrar | GCO 2 e GCO 4 | Procedimento; registro de liberação; nota de incidente | — | não até 14/11: depende da baseline | `fichas/GCO2.md` |
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
| GCO 1: Plano de Gerência de Configuração | plano com itens, níveis, funções, acessos, baselines, mudança, liberação e auditoria | rascunho a partir do repositório e respostas da equipe num formulário; 12 itens, 6 funções | 18 campos só a equipe sabia; o plano expôs acesso total de todos os desenvolvedores e ausência de cópia e de registro de demandas | questionário fechado junto do modelo e seção de achados |
| GCO 2: Procedimento de repositórios, branches, versões e releases | branch por demanda, pull request com revisão de outra pessoa, versão e release | demanda em issue, branch no padrão, pull request completo, verificação automática | revisão não registrada na janela do piloto; pedido feito por mensagem; repositório diverge em quatro pontos da seção 1 | revisor marcado na plataforma, prazo e substituto; ajustes de configuração possíveis no plano gratuito |
| GCO 3: Definição de baseline | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |
| GCO 4: Orientação de commits | `<tipo>: <resumo> (#n)`, corpo em mudança de risco | 1 commit com tipo, escopo, resumo e demanda; verificações da equipe passaram | a orientação não prevê o escopo que a equipe já usa | aceitar escopo opcional |
| GCO 5: Checklist de auditoria de configuração | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] | [PREENCHER - autores] |

Ajustes que não cabem num só resultado (fluxo, funções, ferramenta): [PREENCHER - autores]

Indicadores de GC do piloto real (contagem do checklist por bloco e do histórico; `EXECUCAO.md`, "Indicadores"): no histórico, desde a base, 1 commit na mudança, que segue a orientação com escopo (0 de 1 pelo comando sem escopo); nenhum commit direto na `main`; 1 pull request de outro desenvolvedor integrado sem revisão registrada. Contagem do checklist por bloco: [PREENCHER - autores]

Entrevistas de validação feitas (data e função de quem respondeu; `ENTREVISTA.md`): [PREENCHER - autores]

## 6. Limites

Limites declarados do kit: ver `README.md`, "Limites declarados".

Limites observados na execução: a janela do piloto caiu num fim de semana, e a equipe revisa e integra só em horário de trabalho; uma única mudança, só de teste, não percorre emergência nem falha de liberação; o Autor B não tem acesso ao repositório da empresa e depende de chamada; o rascunho do plano, os testes da mudança e a conferência do repositório foram feitos com apoio de IA e revisados pelo Autor A.

## 7. Parecer do avaliador externo

[PREENCHER - autores]
