# Ficha GCO 1: Plano de Gerência de Configuração

Ficha no ciclo PDSA: Planejar, Executar, Estudar e Agir. Escreva sem nome de empresa, de pessoa ou de cliente, e sem código, URL ou IP; a evidência com dado da empresa fica fora deste repositório.

- Resultado: GCO 1, itens e níveis de controle
- Artefato proposto: Plano de Gerência de Configuração (`artefatos/gco1-plano-de-gerencia-de-configuracao.md`)
- Piloto real (`EXECUCAO.md`): passo 5, preencher o plano para o projeto escolhido; passo 15, itens 1 a 4 do checklist
- Simulação (complemento): C6, serviço fora da lista de itens, acusado em C7; a lista de itens da aplicação de exemplo é `processo/1-itens-de-configuracao.md`

## Planejar

*O que se quer verificar com o artefato, quem faz o quê e quando, e o critério de sucesso adotado. Confirmem ou troquem o critério antes de executar.*

Critério de sucesso proposto: o plano é preenchido para o projeto sem seção em branco; todo item tocado pela mudança do piloto consta da lista, com tipo, responsável e nível de controle; a auditoria não encontra item em uso fora da lista.

Critério mantido. O Autor A preenche a cópia do plano para a parte do projeto em que está a mudança, na sexta, 13/11, e anota início e fim. O Autor B lê no mesmo dia, por chamada, e aponta a seção que ficou vaga. A conferência da lista contra o que a mudança tocou fica para a auditoria de sábado (GCO 5).

## Executar

*O que foi feito de fato: data, quem fez (Autor A ou B), tempo gasto, onde está a evidência. Na simulação, os cenários executados e os endereços dos registros.*

- 13/11, 17h12 a 17h14, Autor A, com apoio de IA: rascunho do plano para a parte do projeto em que está a mudança, só com o que o repositório mostra (guia do projeto, documentação da implantação, configuração do banco e verificações do pull request). Ficaram 18 lacunas que só a equipe sabia: quem exerce cada função, acessos, registro de demandas, cópias de segurança, aprovação da baseline, retenção, prazo de emergência e janela de liberação.
- 13/11, por volta das 17h28, Autor A: respondeu as 18 lacunas num formulário. Resultado: plano sem seção em branco, com 12 itens de configuração (código, testes, base consultada pela IA, esquema e migrations, build, implantação, verificações do pull request, variáveis pelo nome, imagem gerada, cópia do banco, documentos e diagramas, artefatos do processo), 6 funções e 7 achados.
- O item tocado pela mudança (um arquivo de teste) consta da lista, no nível "PR obrigatório".
- 16/11, por mensagem, Autor B: leu o plano preenchido e apontou a seção 2 como vaga para quem é de fora: os artefatos do processo ficam na pasta privada com nível "Livre", mas esse nível usa o histórico do repositório como registro, e não fica claro como as alterações serão rastreadas se a pasta não for versionada.
- 16/11, auditoria (ficha GCO5): item 1 NC, plano sem aprovação e com as seções 2, 4 e 7 diferentes do repositório; item 2 NC, componentes em uso fora da lista; item 3 C.
- Evidência: cópia preenchida do plano na pasta privada.

## Estudar

*O critério foi atendido? O que não ficou bom: seção que faltou ou sobrou, instrução que não deu para seguir, informação que a equipe não tinha, tempo gasto.*

Critério atendido em parte: o plano ficou sem seção em branco e o item tocado está na lista, mas a auditoria encontrou componentes em uso fora da lista (item 2) e um plano sem aprovação, que já diverge do repositório (item 1).

O que não ficou bom:
- O modelo sozinho não basta: o rascunho saiu do repositório em minutos, mas 18 campos só a equipe sabia responder, e eles só foram respondidos quando viraram perguntas fechadas num formulário.
- O plano expôs práticas que o TO-BE não supõe: todos os desenvolvedores administram tudo, inclusive produção e segredos; a revogação de acesso não tem rotina; não há cópia do repositório fora da plataforma; demandas chegam por conversa e não ficam registradas.
- O plano não tinha a função de comitê de controle de mudanças; ela entrou antes da execução, pedida pela orientação.
- Para quem é de fora, a seção 2 não explica como se rastreia a alteração do que fica fora do repositório (leitura do Autor B).

## Agir

*`manter`, `ajustar` ou `abandonar` o artefato, com o motivo. Se `ajustar`: o que muda no artefato e no fluxo, para a nova versão do TO-BE.*

`ajustar`. O modelo do plano passa a vir com um questionário curto, de perguntas fechadas, para o que só a equipe sabe (funções, acessos por recurso, demandas, cópias, aprovação da baseline, prazos e janela), e com uma seção "Achados ao preencher" que alimenta a análise de lacunas. A matriz de acesso fica por recurso e por função, como no piloto. A seção 2 diz como se registra a alteração dos itens guardados fora do repositório, e o plano passa a ser aprovado pelo comitê antes de valer.
