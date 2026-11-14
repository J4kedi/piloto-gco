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
- Teste de restauração na empresa: não autorizado (ninguém assinou a ciência como responsável pela homologação); coberto pela simulação, em C7.
- Decisão do Autor B, item a item, por chamada, com responsável e prazo de cada NC: [PREENCHER - autores]

## Estudar

*O critério foi atendido? O que não ficou bom: item que não deu para verificar, item que faltou, evidência a que o auditor não teve acesso, tempo gasto. O que a auditoria revelou sobre os outros quatro artefatos vai na ficha de cada um.*

[PREENCHER - autores]

## Agir

*`manter`, `ajustar` ou `abandonar` o artefato, com o motivo. Se `ajustar`: o que muda no artefato e no fluxo, para a nova versão do TO-BE.*

[PREENCHER - autores]
