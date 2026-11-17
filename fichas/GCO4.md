# Ficha GCO 4: Orientação de commits

Ficha no ciclo PDSA: Planejar, Executar, Estudar e Agir. Escreva sem nome de empresa, de pessoa ou de cliente, e sem código, URL ou IP; a evidência com dado da empresa fica fora deste repositório.

- Resultado: GCO 4, registros
- Artefato proposto: Orientação de commits (`artefatos/gco4-orientacao-de-commits.md`), com as notas da versão e o registro de liberação (`processo/4-versao-e-notas.md`) e a nota de incidente (`processo/6-nota-de-incidente.md`)
- Piloto real (`EXECUCAO.md`): passo 8, commits da mudança; passos 10 e 14, notas da versão e registro de liberação; passo 15, itens 13 a 17 do checklist
- Simulação (complemento): C5, falha na liberação com nota de incidente; script avulso; C1, registro de liberação gerado por `gco.mjs registrar`

## Planejar

*O que se quer verificar com o artefato, quem faz o quê e quando, e o critério de sucesso adotado. Confirmem ou troquem o critério antes de executar.*

Critério de sucesso proposto: todos os commits da mudança do piloto seguem a orientação; quem não participou da mudança diz, só pelo histórico entre as duas etiquetas e pelas notas da versão, o que mudou da versão anterior para a nova; o registro de liberação fica completo.

Critério mantido. O Autor A faz os commits da mudança no formato da orientação, na sexta, 13/11, e preenche o registro de liberação no sábado, 14/11, se houver liberação. Quem não participou da mudança é o Autor B: no sábado, por chamada, diz o que mudou só pelo histórico e pelas notas da versão; sem etiqueta anterior, o histórico vai da base anotada no passo 3 até a baseline.

## Executar

*O que foi feito de fato: data, quem fez (Autor A ou B), tempo gasto, onde está a evidência. Na simulação, os cenários executados e os endereços dos registros.*

- 13/11, 17h12 a 17h15, Autor A, com apoio de IA: 4 testes escritos para casos de borda de uma regra já existente (de 23 para 27 testes, todos passando), sem mudar código de produção.
- 13/11, 17h15, Autor A: 1 commit, com tipo, escopo, resumo no presente e número da demanda, e corpo com o motivo, os itens afetados e o efeito na implantação (nenhum). As verificações automáticas da equipe no commit passaram (formatação, análise estática e formato da mensagem).
- Indicador do passo 16: 1 commit na mudança; pelo comando do roteiro, que não aceita escopo, 0 de 1 segue a orientação; aceitando escopo, 1 de 1.
- Registro de liberação: 16/11, liberação às 09h14 e troca do slot público às 09h22, pelo Autor A, do commit homologado com a mudança; registro preenchido na pasta privada com commit, artefato, slot e horário. cópia do banco antes da liberação, com nome e data; smoke de saúde e de websocket sem falha. As notas da versão e o registro de liberação foram publicados na release da etiqueta, às 09h26.
- Ciclo 2, 16/11: commit da segunda mudança no mesmo formato (tipo, escopo, resumo e demanda), com corpo; liberação às 09h47 e troca do slot às 09h54, registradas nas notas da release `v1.1.1`.

## Estudar

*O critério foi atendido? O que não ficou bom: tipo que faltou ou sobrou, regra que conflita com o que a equipe já usa, campo do registro que a liberação real não fornece, tempo gasto.*

Critério atendido em parte: os commits dos dois ciclos seguiram a orientação, com escopo; as notas e o registro das duas liberações saíram; e o Autor B, que não fez a baseline, localizou commit, artefato e reversão só pelas notas da `v1.1.1` (ficha GCO3). O registro não tinha a impressão digital da cópia do banco.

O que não ficou bom: a orientação não prevê o escopo (`<tipo>(<escopo>): ...`), que a equipe já usa e que a verificação automática dela aceita. Seguir a orientação à risca obrigaria a equipe a abandonar uma convenção que já funciona, e o indicador do roteiro contou o commit como fora do padrão.

## Agir

*`manter`, `ajustar` ou `abandonar` o artefato, com o motivo. Se `ajustar`: o que muda no artefato e no fluxo, para a nova versão do TO-BE.*

`ajustar`. A orientação de commits passa a aceitar escopo opcional, `<tipo>(<escopo>): <resumo> (#<nº da demanda>)`, compatível com o Conventional Commits e com a verificação que a equipe já tem; o comando do indicador muda junto. O registro de liberação passa a incluir a impressão digital da cópia do banco.
