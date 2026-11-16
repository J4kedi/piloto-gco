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
- 16/11, 09h10 a 09h22, Autor A, na rotina da equipe: nova homologação do mesmo commit, liberação no slot inativo (09h14) e troca do slot público (09h22), as duas sem falha. A liberação e a troca vieram **antes** da aprovação da baseline pelo comitê, pedida à direção por mensagem às 09h; a ordem do procedimento (aprovação e etiqueta antes da liberação) não foi seguida.
- 14/11: conferido que nenhuma automação da plataforma é disparada por etiqueta; criar a etiqueta não implanta nada.
- Próxima versão pela regra: `v1.1.0`, porque desde a última etiqueta entraram funcionalidades novas.
- Aprovação da baseline pelo comitê de controle de mudanças (direção com o responsável por configuração), criação da etiqueta e notas da versão: [PREENCHER - autores]

## Estudar

*O critério foi atendido? O que não ficou bom: componente que não deu para identificar, condição que a rotina real não cumpre, momento de criação que não coube na liberação da empresa, tempo gasto.*

[PREENCHER - autores]

## Agir

*`manter`, `ajustar` ou `abandonar` o artefato, com o motivo. Se `ajustar`: o que muda no artefato e no fluxo, para a nova versão do TO-BE.*

[PREENCHER - autores]
