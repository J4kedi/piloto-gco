# Checklist de auditoria de configuração

Artefato proposto para o resultado GCO 5 (auditorias) do MPS-SW. Verifica se os itens de configuração, as baselines e os registros estão íntegros e se o que foi definido nos demais artefatos está sendo seguido.

- **Quando:** na periodicidade da seção 10 do Plano de Gerência de Configuração e ao fim do piloto.
- **Quem:** Responsável por configuração ou outra pessoa indicada no Plano, desde que não audite mudança própria.
- **Como:** copie a tabela, responda cada item com `C` (conforme), `NC` (não conforme) ou `NA` (não se aplica, com o motivo) e indique a evidência consultada. O checklist respondido é o registro da auditoria.
- **Não conformidade:** vira demanda, com responsável e prazo; o número dela vai na observação.

| Campo | Valor |
|---|---|
| Projeto e período auditado | [PREENCHER] |
| Data e auditor(a), pela função | [PREENCHER] |
| Baselines do período | [PREENCHER] |

| Nº | Verificação | Onde olhar | Resultado | Observação |
|---|---|---|---|---|
| | **A. Plano e itens de configuração (GCO 1)** | | | |
| 1 | O Plano de Gerência de Configuração está aprovado e descreve a ferramenta, os ambientes e a equipe atuais. | Plano | | |
| 2 | Todo componente em uso em produção e em homologação consta da lista de itens, e todo item da lista existe. | Lista de itens; ambientes; repositório | | |
| 3 | Cada item tem tipo, local oficial, responsável e nível de controle. | Lista de itens | | |
| 4 | Os acessos efetivos ao repositório, aos ambientes e aos segredos são os da seção 4 do Plano. | Configuração de acesso da plataforma e dos servidores | | |
| | **B. Repositórios, branches e mudanças (GCO 2)** | | | |
| 5 | O repositório segue o procedimento: nome, modelos de demanda e de pull request, método de merge e nenhum segredo versionado. | Configuração e conteúdo do repositório | | |
| 6 | Toda alteração em item de nível "PR obrigatório" chegou à `main` por pull request; não há commit direto. | `git log --first-parent --no-merges <baseline anterior>..main` | | |
| 7 | Cada pull request do período tem demanda, classificação, evidência de teste e revisão de outra pessoa; os emergenciais têm aprovação anterior ao primeiro commit e revisão posterior. | Pull requests integrados no período | | |
| 8 | As branches seguem o padrão de nome, e não há branch integrada sem remoção. | `git branch -r --merged origin/main` | | |
| | **C. Baselines (GCO 3)** | | | |
| 9 | Cada versão liberada no período tem etiqueta `vX.Y.Z` e release de mesmo nome, com número coerente com as mudanças. | `git tag --list "v*"`; releases | | |
| 10 | Cada baseline identifica os componentes da Definição de baseline: commit, artefato, configuração exigida, notas e cópia de segurança. | Release e registro de liberação | | |
| 11 | A versão em execução em produção e em homologação corresponde a uma baseline, e o artefato em execução é o registrado. | Ambientes; registro de liberação | | |
| 12 | Nenhuma etiqueta foi movida ou apagada, e cada baseline tem a aprovação do comitê de controle de mudanças registrada. | `git show vX.Y.Z --no-patch`, contra o commit do registro de liberação; registro de liberação | | |
| | **D. Registros (GCO 4)** | | | |
| 13 | As mensagens de commit do período seguem a Orientação de commits. | `git log <baseline anterior>..main --oneline --no-merges` | | |
| 14 | As notas de cada versão dizem o que mudou, para quem e como voltar, e conferem com o histórico entre as duas etiquetas. | Release; `git log vA..vB` | | |
| 15 | Cada liberação tem registro com versão, demanda, commit, quem liberou, quando e resultado da verificação. | Registro de liberação | | |
| 16 | Cada falha de liberação ou retorno à versão anterior tem nota de incidente com causa e correção. | Notas de incidente | | |
| 17 | Cada intervenção manual em produção, fora do fluxo de liberação, está registrada. | Registro de scripts avulsos | | |
| | **E. Integridade e recuperação (GCO 5)** | | | |
| 18 | Existe cópia de segurança dos dados anterior a cada liberação, identificada no registro. | Registro de liberação; armazenamento de cópias | | |
| 19 | O teste de restauração do período foi executado e os dados restaurados foram conferidos. | Registro do teste | | |
| 20 | As não conformidades da auditoria anterior foram tratadas ou têm decisão registrada. | Registro da auditoria anterior; demandas | | |

## Resultado da auditoria

- Itens conformes, não conformes e não aplicáveis: [PREENCHER]
- Não conformidades, com a demanda aberta, o responsável e o prazo: [PREENCHER]
- Restauração: `aprovada` ou `reprovada`, e a versão restaurada: [PREENCHER]
- Observações do(a) auditor(a) sobre o processo e sobre este checklist: [PREENCHER]
