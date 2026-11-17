# Relatório do piloto

Escreva sem nome de empresa, de pessoa ou de cliente, e sem código, URL ou IP. A evidência com dado da empresa fica fora deste repositório; aqui entra só o que o termo de autorização permitir divulgar.

## 1. Período e quem executou

- Período: 13 a 16/11/2026.
- Piloto real, projeto e mudança executada, descritos sem identificar a empresa: sistema web de uma empresa de pequeno porte, mantido por uma equipe de poucos desenvolvedores. Duas mudanças, em dois ciclos: cada uma acrescentou testes automatizados de casos de borda a uma regra já existente (4 e 5 testes), sem alterar código de produção, regra de negócio nem implantação (classificação normal).
- Piloto real, quem fez a mudança e quem auditou (Autor A ou Autor B): o Autor A fez as mudanças; a revisão foi de um membro da equipe da empresa, porque o Autor B não tem acesso ao repositório dela; a direção aprovou as baselines, como parte do comitê de controle de mudanças; o Autor B audita a partir da evidência levantada pelo Autor A.
- Autorização da empresa (data do termo e o que ele permite divulgar): termo recebido assinado em 13/11/2026. Permite citar a empresa e o produto no trabalho acadêmico e divulgar a equipe por função, os indicadores do processo de mudança e o processo modelado, sem código-fonte, credenciais, dados de clientes ou nomes de pessoas; autoriza aplicar os artefatos, em caráter de piloto, a mudanças do estudante que integra a equipe, sem alterar regra de negócio, fluxo de implantação ou produção. O revisor da equipe assinou a ciência.
- Simulação, Autor A (Desenvolvedor(a) e Responsável por configuração): preparo (versão v0.1.0 no ar) e cenário C3, em 14/11, com apoio de IA.
- Simulação, Autor B (Solicitante, Revisor(a) e Aprovador emergencial; conferências da auditoria): os passos dele não foram executados (seção 2).
- Repositório: este repositório, público, com o kit, as fichas e este relatório; a evidência com dado da empresa fica na pasta privada dos autores.

## 2. O que foi executado e o que não ocorreu

### Piloto real

Etapas do `EXECUCAO.md`.

| Etapa | Resultado | Artefato | Data | Executado? | Onde está a evidência |
|---|---|---|---|---|---|
| Preencher o plano | GCO 1 | Plano de Gerência de Configuração | 13/11 | sim; leitura do Autor B em 16/11, por mensagem | pasta privada; `fichas/GCO1.md` |
| Conferir o repositório e criar a branch | GCO 2 | Procedimento de repositórios, branches, versões e releases | 13/11 | sim | pasta privada; `fichas/GCO2.md` |
| Implementar, revisar e integrar | GCO 4 e GCO 2 | Orientação de commits; Procedimento | 13 a 16/11 | implementação, pull request e integração (16/11, 08h41), sim; revisão registrada na plataforma, não | plataforma da empresa; `fichas/GCO2.md` e `fichas/GCO4.md` |
| Criar a baseline | GCO 3 | Definição de baseline | 16/11 | sim: aprovada pelo comitê às 09h20 e etiqueta às 09h26, depois de a liberação começar (09h14) | `fichas/GCO3.md` |
| Liberar, verificar e registrar | GCO 2 e GCO 4 | Procedimento; registro de liberação; nota de incidente | 16/11 | sim: liberação às 09h14 (antes da aprovação), troca do slot às 09h22 (depois), verificação sem falha, registro publicado com as notas | `fichas/GCO2.md` |
| Auditar com o checklist | GCO 5 | Checklist de auditoria de configuração | 16/11 | sim: situação de 16/11 às 10h; evidência levantada pelo Autor A com apoio de IA e decisão do Autor B por mensagem, item a item; 6 C, 12 NC e 2 NA, cada NC com função e prazo | `fichas/GCO5.md` |

### Simulação (complemento)

| Cenário | Complementa | Data | Executado? | Observação |
|---|---|---|---|---|
| C1 Mudança normal | GCO 2, 3 e 4 | — | não | ficou para a implantação no Projeto Final II (abaixo) |
| C2 Revisão reprovada | GCO 2 | — | não | ficou para a implantação no Projeto Final II (abaixo) |
| C3 Commit direto | GCO 2 e 5 | 14/11 | sim | commit direto na `main` feito de propósito pelo Autor A, sem aviso ao Autor B; a detecção caberia à auditoria do C7, que não foi executada |
| C4 Mudança emergencial | GCO 2 | — | não | ficou para a implantação no Projeto Final II (abaixo) |
| C5 Falha na liberação | GCO 3 e 4 | — | não | ficou para a implantação no Projeto Final II (abaixo) |
| C6 Serviço fora da lista | GCO 1 e 5 | — | não | ficou para a implantação no Projeto Final II (abaixo) |
| C7 Auditoria e restauração | GCO 5 | — | não | ficou para a implantação no Projeto Final II (abaixo) |
| Script avulso | GCO 4 | — | não | ficou para a implantação no Projeto Final II (abaixo) |

O que não ocorreu, no piloto real e na simulação, e por quê: no piloto real não houve mudança emergencial, falha de liberação, reversão nem script avulso, e o teste de restauração não foi autorizado no ambiente da empresa. Da simulação, só o preparo e o C3 foram executados: os autores priorizaram aplicar os cinco artefatos a mudanças reais, em dois ciclos, com baselines e liberações em produção, e o tempo da entrega não comportou os demais cenários, que dependem do Autor B na plataforma. Esses caminhos ficam para a implantação no Projeto Final II.

## 3. Critérios

Situação: atendido, não atendido ou sem ocorrência. O critério de sucesso de cada artefato e a situação dele estão nas fichas (`fichas/GCO1.md` a `fichas/GCO5.md`).

| Critério da simulação | Situação | Evidência |
|---|---|---|
| Cada cenário percorre o caminho previsto | sem ocorrência | só o C3 foi executado (seção 2) |
| Cada mudança tem solicitação, decisão, alteração identificada, evidência de teste e referência de liberação | sem ocorrência na simulação; no piloto real, atendido nos dois ciclos, exceto a revisão registrada no ciclo 1 | demandas, pull requests e releases na plataforma da empresa (pasta privada); `fichas/GCO2.md` a `GCO4.md` |
| A auditoria detecta os desvios de C3 e C6 | sem ocorrência | C6 e C7 não executados |
| A restauração termina com os dados conferidos | sem ocorrência | teste não autorizado na empresa; C7 não executado |

## 4. Indicadores da simulação

Fonte: `registros/indicadores.md`, gerado por `python indicadores/indicadores.py` a partir de `registros/` e da coleta `python indicadores/indicadores.py coletar`.

- Data da coleta: não se aplica: a simulação não chegou aos cenários com registro (seção 2); os indicadores do piloto real estão na seção 5.
- Divergências entre planilha, log e histórico: não se aplica: a simulação não chegou aos cenários com registro (seção 2); os indicadores do piloto real estão na seção 5.
- Leitura dos indicadores: não se aplica: a simulação não chegou aos cenários com registro (seção 2); os indicadores do piloto real estão na seção 5.
- Adesão: não se aplica: a simulação não chegou aos cenários com registro (seção 2); os indicadores do piloto real estão na seção 5.
- Dificuldades: não se aplica: a simulação não chegou aos cenários com registro (seção 2); os indicadores do piloto real estão na seção 5.
- Exceções: não se aplica: a simulação não chegou aos cenários com registro (seção 2); os indicadores do piloto real estão na seção 5.
- Tempo gasto nas tarefas de controle, no piloto real: do pedido de revisão à integração, 9 min no ciclo 2; aprovação do comitê, 1 min no ciclo 1 e 5 min no ciclo 2; etiqueta, notas da versão e registro de liberação, cerca de 6 min na v1.1.0, com apoio de IA.

## 5. Avaliação dos resultados do piloto

Uma linha por resultado de GCO, a partir das fichas. O ajuste é o que muda na nova versão do TO-BE.

| Resultado e artefato | O que foi proposto | O que foi usado | O que não funcionou | Ajuste |
|---|---|---|---|---|
| GCO 1: Plano de Gerência de Configuração | plano com itens, níveis, funções, acessos, baselines, mudança, liberação e auditoria | rascunho a partir do repositório e respostas da equipe num formulário; 12 itens, 6 funções | 18 campos só a equipe sabia; o plano expôs acesso total de todos os desenvolvedores e ausência de cópia e de registro de demandas | questionário fechado junto do modelo e seção de achados; seção 2 diz como se registra o que fica fora do repositório; plano aprovado pelo comitê |
| GCO 2: Procedimento de repositórios, branches, versões e releases | branch por demanda, pull request com revisão de outra pessoa, versão e release | demanda em issue, branch no padrão, pull request completo, verificação automática | ciclo 1: revisão por mensagem e integração por outra conta, sem revisão registrada; repositório diverge em quatro pontos da seção 1. Ciclo 2, com o ajuste: revisão registrada antes da integração | revisor marcado na plataforma, prazo e substituto, cada pessoa com a própria conta; ajustes de configuração possíveis no plano gratuito |
| GCO 3: Definição de baseline | baseline depois da homologação, aprovada pelo comitê, com etiqueta e notas, antes da liberação | baselines v1.1.0 e v1.1.1 com commit, artefato, notas, registro de liberação e cópia do banco | ciclo 1: liberação antes da aprovação; ciclo 2: etiqueta 4 min antes da mensagem de aprovação | etiqueta aprovada como condição para liberar, criada só com a aprovação à vista; impressão digital da cópia do banco |
| GCO 4: Orientação de commits | `<tipo>: <resumo> (#n)`, corpo em mudança de risco | 2 commits com tipo, escopo, resumo e demanda; notas da versão e registro de liberação nas duas releases | a orientação não prevê o escopo que a equipe já usa; o registro não tinha a impressão digital da cópia do banco | aceitar escopo opcional; impressão digital no registro |
| GCO 5: Checklist de auditoria de configuração | 20 itens em cinco blocos, por quem não fez a mudança, com evidência, e cada NC com responsável e prazo | 20 itens respondidos pelo Autor B a partir da evidência do Autor A; 6 C, 12 NC e 2 NA (33%); as 12 NC com função e prazo | comandos dos itens 6 e 8 confundem squash com commit direto; 5 itens contam o mesmo fato; o item 12 não diz se a aprovação vem antes da etiqueta ou só antes da liberação; restauração NA; auditor sem acesso à fonte, com a sugestão de resposta feita pelo Autor A com apoio de IA; NC ainda sem demanda | comandos corrigidos e itens repetidos agrupados; item 12 com a ordem (aprovação antes da etiqueta); itens 7 e 13 alinhados aos ajustes do GCO 2 e do GCO 4; NC vira demanda no dia; auditor com acesso de leitura |

Ajustes que não cabem num só resultado (fluxo, funções, ferramenta): a aprovação do comitê e a etiqueta passam a ser condição de entrada da ferramenta de liberação da equipe; cada pessoa usa a própria conta na plataforma; o repositório ganha um único método de merge, exclusão automática de branch e modelos de issue e de pull request.

Indicadores de GC do piloto real (contagem do checklist por bloco e do histórico; `EXECUCAO.md`, "Indicadores"): no histórico, desde a base até 16/11 às 10h, 2 commits nas mudanças do piloto, os 2 no formato com escopo (0 de 2 pelo comando sem escopo); nenhum commit direto na `main`; dos 5 pull requests integrados, 1 com revisão registrada (o do ciclo 2); 2 baselines aprovadas pelo comitê; 2 liberações das baselines sem falha e nenhuma reversão em 61 execuções da ferramenta de implantação. Contagem do checklist por bloco, conformidade = C / (C + NC): A, plano e itens, 1 de 4 (25%); B, repositórios e mudanças, 0 de 4 (0%); C, baselines, 3 de 4 (75%); D, registros, 2 de 5 (40%); E, integridade e recuperação, 0 de 1, com 2 NA (0%). No total, 6 C, 12 NC e 2 NA: 33% de conformidade.

Entrevistas de validação feitas (data e função de quem respondeu; `ENTREVISTA.md`): nenhuma completa. A do revisor da equipe chegou incompleta em 16/11 e não foi usada nas fichas nem neste relatório; fica para o Projeto Final II.

## 6. Limites

Limites declarados do kit: ver `README.md`, "Limites declarados".

Limites observados na execução: a janela do piloto caiu num fim de semana, e a equipe revisa e integra só em horário de trabalho; as duas mudanças, só de teste, não percorrem emergência nem falha de liberação; a simulação parou no C3; o Autor B não tem acesso ao repositório da empresa e audita a partir da evidência levantada pelo Autor A; o rascunho do plano, os testes das mudanças, a conferência do repositório, o levantamento da evidência e a sugestão de resposta da auditoria, as etiquetas, as notas e o registro de liberação das duas versões e o preparo e o C3 da simulação foram feitos com apoio de IA e revisados pelos autores.

## 7. Parecer do avaliador externo

Não se aplica: o termo foi assinado e o piloto ocorreu na empresa; o parecer externo só valia se a empresa não aceitasse o piloto (documento, Seção 4.6). A avaliação vem do parecer da empresa, resumido no documento.
