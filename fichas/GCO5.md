# Ficha GCO 5: Checklist de auditoria de configuração

Ficha no ciclo PDSA: Planejar, Executar, Estudar e Agir. Escreva sem nome de empresa, de pessoa ou de cliente, e sem código, URL ou IP; a evidência com dado da empresa fica fora deste repositório.

- Resultado: GCO 5, auditorias
- Artefato proposto: Checklist de auditoria de configuração (`artefatos/gco5-checklist-de-auditoria-de-configuracao.md`)
- Piloto real (`EXECUCAO.md`): passo 15, auditoria da mudança do piloto, com os vinte itens do checklist; passo 16, indicadores
- Simulação (complemento): C7, auditoria que tem de acusar os desvios plantados em C3 e em C6, e teste de restauração; o roteiro é `processo/8-auditoria-e-restauracao.md`

## Planejar

*O que se quer verificar com o artefato, quem faz o quê e quando, e o critério de sucesso adotado. Confirmem ou troquem o critério antes de executar.*

Critério de sucesso proposto: a auditoria é feita por quem não fez a mudança; todos os itens do checklist recebem resposta (conforme, não conforme ou não se aplica), com a evidência indicada; cada não conformidade fica registrada com responsável e prazo.

Critério mantido. O Autor B, que não fez a mudança, audita no sábado, 14/11, por chamada com tela compartilhada (passo 1, alternativa a): o Autor A mostra as evidências e o Autor B responde os vinte itens na cópia do checklist, na pasta privada. O teste de restauração fica NA na empresa, a menos que o responsável pela homologação assine a ciência; a simulação cobre esse caminho em C7.

## Executar

*O que foi feito de fato: data, quem auditou (Autor A ou B), tempo gasto, onde está o checklist respondido. Na simulação, o endereço do registro em `registros/auditorias/`.*

- 14/11, 15h27, com apoio de IA: evidência dos 20 itens do checklist levantada só por leitura do repositório e da plataforma da empresa, em duas lentes: desde a última etiqueta, de julho, e a mudança do piloto. Cada item recebeu uma sugestão de resposta. Sugestão: 3 C, 13 NC e 4 NA; conformidade sugerida de 25% no bloco A, 0% no B, 33% no C, 25% no D e 0% no E.
- O que a evidência mostra: nenhum dos pull requests integrados desde julho tem revisão registrada; 121 commits entraram na `main` sem pull request (nenhum desde setembro); uma única etiqueta e liberações sem etiqueta; nenhum registro de liberação nem de script avulso; 587 branches integradas não removidas.
- O que não se verificou sem acesso ao servidor: versão e artefato em produção e em homologação, quantidade de liberações, existência das cópias do banco.
- Teste de restauração na empresa: não autorizado (ninguém assinou a ciência como responsável pela homologação); previsto na simulação, em C7, que não foi executada.
- 16/11, até as 10h, Autor A, com apoio de IA: evidência atualizada para a situação de 16/11, às 10h, já com as baselines `v1.1.0` e `v1.1.1` do piloto e os registros da ferramenta de implantação; sugestão de 6 C, 12 NC e 2 NA. A evidência e a sugestão foram ao Autor B num pacote, com uma tabela por item.
- 16/11, 20h25, Autor B, por mensagem e não por chamada, porque não tem acesso à empresa: confirmou as 20 sugestões, sem trocar nenhuma, e aceitou a função responsável e o prazo de cada uma das 12 NC (responsável por configuração, até 20/11 ou 27/11; direção com o responsável por configuração, até 27/11, nas que tratam de pull request e revisão). Apontou que o pacote listava entre as ações o item 11, que é conforme e não exige ação. Resultado: 6 C, 12 NC e 2 NA, 33% de conformidade; por bloco, A 25%, B 0%, C 75%, D 40% e E 0%. Tempo do Autor B: não medido; as respostas das três partes do pacote foram enviadas juntas às 20h25.
- Checklist respondido: cópia na pasta privada.

## Estudar

*O critério foi atendido? O que não ficou bom: item que não deu para verificar, item que faltou, evidência a que o auditor não teve acesso, tempo gasto. O que a auditoria revelou sobre os outros quatro artefatos vai na ficha de cada um.*

Critério atendido, com uma diferença do planejado: quem não fez a mudança auditou, os 20 itens tiveram resposta com a evidência indicada, e cada NC tem função responsável e prazo. A decisão veio por mensagem, e não por chamada, a partir da evidência levantada pelo Autor A; o Autor B não conferiu a evidência na fonte.

O que não ficou bom:
- O item 12 não diz se a aprovação do comitê precisa vir antes da criação da etiqueta ou só antes da liberação. A dúvida apareceu justamente no ciclo 2 (ficha GCO3), em que a etiqueta saiu 4 minutos antes da mensagem de aprovação, e o auditor manteve C porque a aprovação veio antes da liberação.
- O teste de restauração (item 19) ficou NA: não foi autorizado na empresa, e a simulação não chegou ao C7.
- O comando do item 6 mistura commit direto com squash ou rebase de pull request (36 dos 157 eram de pull request), e separar os dois exigiu a API da plataforma; o comando do item 8 não detecta branch integrada por squash e dá um piso.
- Os itens 9, 11, 14, 15 e 18 dependem do mesmo fato, liberar sem baseline; contados separados, pesam cinco vezes no resultado.
- As NC ainda não viraram demandas na empresa, como o checklist pede.
- Sem acesso à empresa, o auditor depende de quem fez a mudança para ver a evidência; a separação entre quem faz e quem audita fica só na decisão.

## Agir

*`manter`, `ajustar` ou `abandonar` o artefato, com o motivo. Se `ajustar`: o que muda no artefato e no fluxo, para a nova versão do TO-BE.*

`ajustar`. O item 12 passa a dizer a ordem: a aprovação do comitê vem antes da criação da etiqueta e, portanto, antes da liberação, como a definição de baseline já pede (ficha GCO3). O item 13 confere o formato com o escopo opcional que a orientação de commits passa a aceitar (ficha GCO4), e o item 7 confere a revisão registrada de todo pull request integrado (ficha GCO2). Os comandos dos itens 6 e 8 passam a separar squash e rebase de commit direto, e os itens que dependem de liberar sem baseline são agrupados. Cada NC vira demanda no dia da auditoria, com o número anotado no checklist. O auditor precisa de acesso de leitura ao repositório e aos registros, para não depender de quem fez a mudança.
