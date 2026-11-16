# Ficha GCO 2: Procedimento de repositórios, branches, versões e releases

Ficha no ciclo PDSA: Planejar, Executar, Estudar e Agir. Escreva sem nome de empresa, de pessoa ou de cliente, e sem código, URL ou IP; a evidência com dado da empresa fica fora deste repositório.

- Resultado: GCO 2, sistema de gerência de configuração e mudanças
- Artefato proposto: Procedimento de repositórios, branches, versões e releases (`artefatos/gco2-procedimento-de-repositorios-branches-versoes-e-releases.md`)
- Piloto real (`EXECUCAO.md`): passos 6 e 7, repositório e branch; passo 9, pull request, revisão e integração; passo 14, versão e release; passo 15, itens 5 a 8 do checklist
- Simulação (complemento): C2, revisão reprovada; C3, commit direto, acusado em C7; C4, mudança emergencial; C1, fluxo completo. A classificação da mudança na simulação é `processo/2-classificacao.md`

## Planejar

*O que se quer verificar com o artefato, quem faz o quê e quando, e o critério de sucesso adotado. Confirmem ou troquem o critério antes de executar.*

Critério de sucesso proposto: a mudança do piloto segue o procedimento do início ao fim (branch com o nome previsto, pull request revisado por outra pessoa, versão numerada pela regra, release publicada a partir da etiqueta), sem passo que precise ser explicado fora do procedimento.

Critério mantido. Na sexta, 13/11, o Autor A confere o repositório da empresa contra a seção 1 do procedimento, cria a branch, abre o pull request e integra. O Autor B não tem acesso ao repositório da empresa (passo 1, alternativa c): a revisão é de um membro da equipe da empresa que não participou da mudança, depois de assinar a ciência, registrada no próprio pull request, na plataforma, antes da integração. A liberação, se ocorrer, segue a rotina da empresa no sábado, 14/11.

## Executar

*O que foi feito de fato: data, quem fez (Autor A ou B), tempo gasto, onde está a evidência. Na simulação, os cenários executados e os endereços dos registros.*

- 13/11, 17h09, Autor A: demanda registrada como issue. Na rotina da equipe as demandas chegam por conversa e não viram issue.
- 13/11, 17h10, Autor A: branch criada da `main` atualizada, no padrão `<tipo>/<nº da demanda>-<resumo>`.
- 13/11, 17h15, Autor A, com apoio de IA: conferência do repositório contra a seção 1 do procedimento, sem alterar nada. Confere: repositório privado com `main`; README, `.gitignore`, build e implantação no repositório; segredos de produção fora dele. Não confere: não há modelo de demanda nem de pull request; três métodos de merge habilitados (merge, squash e rebase); branch não é apagada depois da integração (mais de 100 no remoto); a `main` não tem proteção, porque o plano da plataforma não oferece; todos os desenvolvedores administram o repositório. Confere em parte: uma única etiqueta, de julho, sem baseline desde então.
- 13/11, 17h16, Autor A: pull request aberto com demanda, classificação (normal), itens afetados, risco, evidência de teste, forma de reversão e checklist de revisão. A verificação automática da plataforma passou.
- 13/11, noite: o revisor da equipe assinou a ciência. O pedido de revisão foi feito por mensagem, sem marcar o revisor no pull request.
- 14/11, 15h10: a plataforma não registrava nenhuma revisão; a integração aguarda a revisão registrada, que a equipe faz em horário de trabalho.
- Ciclo 2, com o ajuste do Agir abaixo: 16/11, 09h09, Autor A, demanda registrada como issue; 09h10, branch no padrão, 1 commit só de teste (5 testes, com apoio de IA) e pull request com o revisor marcado na plataforma, na conta pessoal dele, com prazo (16/11, 18h) e substituto. 09h19, revisor: revisão registrada no pull request (Approve), com a conta pessoal, 8 minutos depois do pedido; a verificação automática passou às 09h19; 09h20, o revisor integrou com a mesma conta, por merge commit. A conferência rápida do corpo do pull request não foi marcada. 09h33, Autor A: branch apagada; a demanda fica aberta até a liberação.
- No período, desde a base: 1 pull request de outro desenvolvedor foi integrado à `main`, sem revisão registrada; nenhum commit direto.
- 16/11, 08h41: pull request integrado à `main` por merge commit, pelo próprio revisor, com uma conta administrativa da organização que ele usa, e não com a conta pessoal dele. O revisor revisou fora da plataforma (relato do Autor A); a plataforma não registra revisão nem pedido de revisão no pull request (conferido às 08h48). A demanda continua aberta.
- 16/11, 08h50, Autor A: branch da mudança apagada do remoto depois da integração, como manda o procedimento, porque a exclusão automática está desligada.

## Estudar

*O critério foi atendido? O que não ficou bom: passo que a rotina real não comporta, regra que conflita com o que a equipe já faz, configuração que a plataforma não oferece, tempo gasto.*

Critério não atendido. A branch e o pull request seguiram o procedimento sem passo extra, e a integração ocorreu no primeiro dia útil, 16/11; mas o pull request foi integrado com zero revisões registradas, como os demais da equipe (ficha GCO5). A versão e a release dependem da baseline (ficha GCO3).

Ciclo 2, com o ajuste: critério atendido. Revisão registrada na plataforma, por outra pessoa, com a conta pessoal, antes da integração, e integração pela mesma conta, 9 minutos depois do pedido; só a conferência rápida do corpo do pull request ficou sem marcar.

O que não ficou bom:
- Ciclo 1: o pedido de revisão foi feito por mensagem; o revisor não foi marcado no pull request, e a revisão não entrou na fila dele na plataforma.
- A equipe revisa e integra só em horário de trabalho; um piloto de fim de semana não comporta a espera.
- A plataforma, no plano em uso, não protege a `main`: a regra de revisão vale só por procedimento, e no mesmo período outro pull request foi integrado sem revisão.
- A configuração do repositório diverge do procedimento em quatro pontos da seção 1 (modelos, método de merge, exclusão de branch, proteção).
- A integração foi feita pelo revisor com uma conta administrativa da organização, e não com a conta pessoal, e sem revisão registrada: pela plataforma não dá para saber quem integrou, nem se houve revisão antes da integração.

## Agir

*`manter`, `ajustar` ou `abandonar` o artefato, com o motivo. Se `ajustar`: o que muda no artefato e no fluxo, para a nova versão do TO-BE.*

`ajustar`, com o ajuste já verificado no ciclo 2. O procedimento passa a exigir que cada pessoa revise e integre com a própria conta, que o revisor seja marcado no pull request (pedido de revisão na plataforma, não por mensagem) e a fixar um prazo de revisão, com um revisor substituto quando o prazo vence. A seção 1 ganha os ajustes de configuração que a plataforma permite no plano gratuito: um único método de merge, exclusão automática da branch e modelos de demanda e de pull request. Sem proteção técnica da `main`, quem integra confere antes a revisão registrada (Approve) de quem não fez a mudança, e a auditoria mensal confere a revisão de todo pull request integrado. A conferência rápida sai do corpo do pull request e vira o texto sugerido do comentário da revisão, porque no ciclo 2 o revisor aprovou sem marcá-la.
