# Ficha GCO 3: Definição de baseline

Ficha no ciclo PDSA: Planejar, Executar, Estudar e Agir. Escreva sem nome de empresa, de pessoa ou de cliente, e sem código, URL ou IP; a evidência com dado da empresa fica fora deste repositório.

- Resultado: GCO 3, baselines
- Artefato proposto: Definição de baseline (`artefatos/gco3-definicao-de-baseline.md`)
- Piloto real (`EXECUCAO.md`): passo 10, criar a baseline da mudança; passo 15, itens 9 a 12 do checklist
- Simulação (complemento): C5, retorno à baseline anterior e nova liberação da mesma versão; C1, criação da baseline pelo comando `gco.mjs baseline`

## Planejar

*O que se quer verificar com o artefato, quem faz o quê e quando, e o critério de sucesso adotado. Confirmem ou troquem o critério antes de executar.*

Critério de sucesso proposto: a baseline da mudança do piloto é criada com todos os componentes da definição identificados, depois da homologação e antes da liberação, por quem a definição indica; a partir da etiqueta, outra pessoa localiza o commit, o artefato e as notas da versão.

Critério mantido. Depois da homologação pela rotina da empresa (sexta, 13/11, ou sábado, 14/11), o Autor A escreve as notas da versão na pasta privada e cria a etiqueta no commit homologado, se a empresa confirmar que a etiqueta não dispara implantação nem pipeline; se não, registra a baseline pelo hash, na pasta privada, e anota o motivo. A outra pessoa que localiza commit, artefato e notas a partir da etiqueta é o Autor B, por chamada, no sábado.

## Executar

*O que foi feito de fato: data, quem fez (Autor A ou B), tempo gasto, onde está a evidência. Na simulação, os cenários executados e os endereços dos registros.*

- 16/11, 08h41: mudança integrada (ficha GCO2).
- 16/11, 08h47: o revisor homologou a `main` com a mudança, junto com outras duas integrações do dia, pela ferramenta de implantação da equipe; a homologação passou. É o commit candidato à baseline.
- 16/11, 09h10 a 09h22, Autor A, na rotina da equipe: nova homologação do mesmo commit, liberação no slot inativo (09h14) e troca do slot público (09h22), as duas sem falha. A liberação no slot inativo veio **antes** da aprovação da baseline; a troca do slot público, depois.
- 14/11: conferido que nenhuma automação da plataforma é disparada por etiqueta; criar a etiqueta não implanta nada.
- Próxima versão pela regra: `v1.1.0`, porque desde a última etiqueta entraram funcionalidades novas.
- 16/11, 09h19, Autor A: pedido de aprovação da baseline `v1.1.0` à direção, por mensagem no canal da equipe. 09h20: a direção aprovou; com o Autor A, que é o responsável por configuração, fecha o comitê de controle de mudanças.
- 16/11, 09h26, Autor A: etiqueta anotada `v1.1.0` no commit homologado e liberado, e release com as notas da versão e o registro de liberação (commit, artefato, homologação, liberação, aprovação, troca do slot, cópia do banco e verificação). A etiqueta não disparou nenhuma automação.
- Localizar commit, artefato e notas a partir da etiqueta, por quem não fez a baseline (Autor B): [PREENCHER - autores]

## Estudar

*O critério foi atendido? O que não ficou bom: componente que não deu para identificar, condição que a rotina real não cumpre, momento de criação que não coube na liberação da empresa, tempo gasto.*

Critério atendido em parte. A baseline reúne todos os componentes da definição e foi criada por quem a definição indica, depois da homologação. A ordem, porém, não foi seguida: a liberação no slot inativo começou 6 minutos antes da aprovação do comitê, e a etiqueta veio 4 minutos depois da troca do slot público.

O que não ficou bom:
- O hábito da equipe é liberar logo depois de homologar, e nada na ferramenta de liberação lembra da aprovação nem da etiqueta.
- O comitê não foi o gargalo: respondeu 1 minuto depois do pedido. O atraso veio de pedir a aprovação depois de começar a liberação.
- A cópia do banco tem nome e data no log da liberação, mas não tem impressão digital registrada.

## Agir

*`manter`, `ajustar` ou `abandonar` o artefato, com o motivo. Se `ajustar`: o que muda no artefato e no fluxo, para a nova versão do TO-BE.*

`ajustar`. A aprovação do comitê e a etiqueta passam a ser a condição de entrada da liberação: quem libera confere a etiqueta aprovada antes de confirmar, e o pedido de aprovação sai junto com o fim da homologação. Como o comitê respondeu em 1 minuto, a regra cabe na rotina; o passo seguinte é a ferramenta de liberação da equipe recusar versão sem etiqueta. A definição passa a pedir a impressão digital da cópia do banco no registro.
