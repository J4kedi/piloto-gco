# Execução do piloto

Passo a passo dos dois autores, em ordem. Marque a caixa de cada passo ao concluí-lo. Entrega: segunda, 16/11/2026, até as 23h59.

| Dia | O que |
|---|---|
| sexta, 13/11 | preparo e execução de GCO 1 a 4; simulação: preparo, C3 e C1 |
| sábado, 14/11 | liberação e auditoria (GCO 5); indicadores; simulação: C4, script avulso, C5 e C7 |
| domingo, 15/11 | avaliação, ajustes para a nova versão do TO-BE, entrevista e parecer do avaliador externo |
| segunda, 16/11 | conferência final, documento e entrega |

## Regras que valem do início ao fim

- **Nada da empresa entra neste repositório:** nome, código, URL, IP, credencial, dado de cliente, nome de pessoa.
- **Pasta privada:** os autores mantêm uma pasta fora deste repositório, fora do clone do repositório da empresa e fora de qualquer repositório público. Nela ficam o termo, as cópias preenchidas dos artefatos (plano, checklist, notas da versão, registro de liberação, nota de incidente) e qualquer captura de tela.
- **O que vem para cá:** as fichas e o relatório, escritos sem identificação, e só a evidência que o termo permitir. Em geral: hash curto, etiqueta, data, duração e contagem. Nunca código, credencial, dado de cliente nem nome.
- **Papéis:** o Autor A executa, porque é quem tem acesso ao repositório da empresa. O Autor B revisa e audita. Na simulação, os papéis são os de `cenarios.md`.
- **Marcadores:** `[PREENCHER - autores]` é o que os autores escrevem neste repositório. `[PREENCHER]`, nos modelos de `artefatos/`, é campo do modelo, preenchido na cópia da pasta privada.
- **Resultado só depois de executar.** Passo que não ocorrer é declarado como não ocorrido, com o motivo, na ficha e no relatório.

## O que preencher e o que guardar, por resultado

| Resultado | Artefato (cópia preenchida na pasta privada) | Evidência que pode vir para cá, se o termo permitir | Onde registrar |
|---|---|---|---|
| GCO 1 | Plano de Gerência de Configuração | data e duração; quantas das dez seções ficaram preenchidas; quantos itens na lista e quantos completos | `fichas/GCO1.md`, "Executar" |
| GCO 2 | Procedimento de repositórios, branches, versões e releases: conferência da seção 1, branch, pull request, versão e release | data; quantos pontos da seção 1 conferem; se o nome da branch seguiu o padrão; se houve revisão de outra pessoa e quando; hash curto da integração | `fichas/GCO2.md`, "Executar" |
| GCO 3 | Definição de baseline: notas da versão e etiqueta | etiqueta, hash curto e data; quantos dos sete componentes foram identificados | `fichas/GCO3.md`, "Executar" |
| GCO 4 | Orientação de commits; registro de liberação; nota de incidente, se houver falha | quantos commits e quantos no formato; data da liberação e resultado da verificação | `fichas/GCO4.md`, "Executar" |
| GCO 5 | Checklist de auditoria de configuração, respondido | data e duração; contagem de C, NC e NA por bloco; quantas não conformidades ficaram com responsável e prazo; restauração aprovada, reprovada ou não executada | `fichas/GCO5.md`, "Executar" |

O que não ficou bom vai em "Estudar" da mesma ficha, e o ajuste, em "Agir".

## Antes de começar

- [x] **0. Portão: termo assinado.** O piloto real só começa com o termo assinado pela empresa e com a cláusula de aplicação: "aplicar os artefatos em mudanças do estudante, sem alterar regra de negócio, fluxo de implantação ou produção". Guardem o termo na pasta privada e anotem o que ele permite divulgar. **Sem o termo, o piloto real não começa:** rodem só a simulação (passos 12, 13 e 17 a 19), avisem a orientadora no mesmo dia e declarem a situação no relatório.
- [x] **1. Decidir como o Autor B revisa e audita.** Se o Autor B tiver acesso ao repositório da empresa, ele revisa e audita lá. Se não tiver, a decisão é dos autores, registrada no "Planejar" das fichas GCO2 e GCO5:
  - a) chamada com tela compartilhada: o Autor A mostra o pull request e as evidências, e o Autor B decide. Nada sai da empresa.
  - b) resumo exportado da mudança, sem código: quantidade de arquivos e de linhas e as mensagens de commit, se o termo permitir. O Autor B não vê o código, e a ficha declara esse limite.
  - c) revisão, neste repositório, só dos artefatos e das fichas. O Autor B não revisa a mudança: a revisão dela precisa ser de alguém da empresa, ou o critério da ficha GCO2 fica não atendido.
- [x] **2. Escolher a mudança real.** Uma mudança do Autor A no repositório da empresa que atenda a todos os critérios:
  - já estava prevista no trabalho dele e cabe em um pull request pequeno, de um dia;
  - não altera regra de negócio (por exemplo: teste automatizado, correção de texto ou de mensagem, documentação técnica, refatoração local sem comportamento novo);
  - não altera o fluxo de implantação nem a produção: se for liberada, é pela rotina normal da empresa, sem passo novo;
  - passa pelos cinco resultados: toca item que entra na lista do plano (GCO 1), exige branch e pull request (GCO 2), entra numa versão identificável (GCO 3), gera commits e registro (GCO 4) e pode ser auditada (GCO 5);
  - pode ser descrita sem identificar a empresa.
- [x] **3. Preparar a pasta privada.** Copiem para ela os cinco arquivos de `artefatos/` e os modelos de notas da versão e de registro de liberação (`processo/4-versao-e-notas.md`) e de nota de incidente (`processo/6-nota-de-incidente.md`). Anotem o hash curto da `main` do repositório da empresa antes da mudança: é a `<base>` das contagens do passo 16.
- [x] **4. Planejar.** No "Planejar" das cinco fichas, confirmem ou troquem o critério de sucesso e escrevam quem faz o quê e quando. Isso vem antes de executar.

## Sexta, 13/11: preparo e GCO 1 a 4

- [x] **5. GCO 1: preencher o plano.** O Autor A preenche a cópia do Plano de Gerência de Configuração para o projeto, ou a parte dele, em que está a mudança. O Autor B lê e aponta a seção que ficou vaga. Anotem o início e o fim.
- [x] **6. GCO 2: conferir o repositório.** Comparem o repositório da empresa com a seção 1 do procedimento, sem alterar nada, e anotem o que confere e o que não confere.
- [x] **7. GCO 2: criar a branch** da mudança, com o nome do procedimento (seção 2).
- [x] **8. GCO 4: implementar,** com os commits no formato da Orientação de commits.
- [x] **9. GCO 2: pull request, revisão e integração.** O pull request leva demanda, classificação, evidência de teste e forma de reversão. O Autor B revisa pela alternativa do passo 1. A integração segue a rotina da empresa.
- [x] **10. GCO 3: criar a baseline.** Depois da homologação pela rotina da empresa, escrevam as notas da versão, na pasta privada, e criem a etiqueta `vX.Y.Z` no commit homologado, conforme a Definição de baseline. Antes de criar etiqueta no repositório da empresa, confirmem com a empresa que ela não dispara implantação nem pipeline. Se não puderem criá-la, registrem a baseline na pasta privada, identificada pelo hash do commit homologado, e anotem o motivo na ficha GCO3.
- [x] **11. Fichas.** Preencham o "Executar" das fichas GCO1 a GCO4 com o que ocorreu no dia.
- [x] **12. Simulação: preparo.** `README.md`, "Simulação: preparo", até a baseline `v0.1.0`.
- [ ] **13. Simulação: C3 e C1,** pelos roteiros de `cenarios.md`. *Parcial ou não executado em 16/11: `RELATORIO.md`, seção 2.*

## Sábado, 14/11: liberação e auditoria (GCO 5)

- [x] **14. GCO 2 e GCO 4: liberação.** Pela rotina da empresa, sem passo novo. Verifiquem a versão e preencham o registro de liberação, na pasta privada. Se a verificação falhar, escrevam a nota de incidente. Se a empresa não liberar até sábado, declarem a liberação como não ocorrida e auditem até a baseline.
- [x] **15. GCO 5: auditoria.** O Autor B responde os vinte itens na cópia do checklist, com o Autor A mostrando as evidências. Item que o termo não permite executar na empresa, como o teste de restauração, fica `NA`, com o motivo; a simulação cobre esse caminho em C7. Cada não conformidade fica com responsável e prazo, na pasta privada.
- [x] **16. Indicadores de GC do piloto real.** Ver "Indicadores", abaixo.
- [ ] **17. Simulação: C4, script avulso e C5,** nesta ordem. *Parcial ou não executado em 16/11: `RELATORIO.md`, seção 2.*
- [ ] **18. Simulação: C7,** auditoria e restauração, com a tabela do checklist respondida no registro. *Parcial ou não executado em 16/11: `RELATORIO.md`, seção 2.*
- [ ] **19. Indicadores da simulação.** Com as planilhas e os registros em commit na `main`: `python indicadores/indicadores.py coletar` e `python indicadores/indicadores.py`. *Parcial ou não executado em 16/11: `RELATORIO.md`, seção 2.*
- [x] **20. Fichas.** Preencham o "Executar" da ficha GCO5 e completem o das outras com a liberação e com os cenários da simulação.

## Domingo, 15/11: avaliação, ajustes e parecer

- [x] **21. Estudar e agir.** Em cada uma das cinco fichas: o critério foi atendido, o que não ficou bom e a decisão (`manter`, `ajustar` ou `abandonar`).
- [ ] **22. Entrevista de validação.** Apliquem `ENTREVISTA.md` a quem usou o processo na empresa (quem revisou, liberou ou acompanhou a mudança), identificado só pela função. Se ninguém além dos autores participou, declarem isso no relatório: a entrevista fica para a validação com a empresa.
- [x] **23. Relatório, seções 1 a 4 e 6.** Preencham `RELATORIO.md` a partir das fichas, dos registros e de `registros/indicadores.md`.
- [x] **24. Avaliação dos resultados do piloto.** Seção 5 do relatório: uma linha por resultado de GCO, com o que foi proposto, o que foi usado, o que não funcionou e o ajuste.
- [x] **25. Nova versão do TO-BE.** Da coluna "Ajuste" e do "Agir" das fichas, listem o que muda no TO-BE e em cada artefato. Essa lista vai para o documento do Projeto Final. Os arquivos de `artefatos/` só mudam depois, na nova versão.
- [ ] **26. Parecer do avaliador externo.** Enviem ao avaliador o endereço do repositório e a folha de parecer assim que as fichas estiverem preenchidas. O parecer recebido até 15/11 vai para a seção 7 do relatório, com a identificação que o avaliador autorizar.

## Segunda, 16/11: documento e entrega até as 23h59

- [ ] **27. Zerar os marcadores.** O comando abaixo não pode devolver nenhuma linha:
  ```
  git grep -n --untracked "PREENCHER - autores" -- README.md RELATORIO.md fichas registros
  ```
- [ ] **28. Conferir que nada da empresa entrou.** Leiam o que mudou desde o início (`git diff v0.1.0..HEAD -- README.md RELATORIO.md fichas registros`) e procurem nome de empresa, de produto, de cliente e de pessoa, URL, IP e trecho de código. Confiram também o autor dos commits (`git log --format="%an <%ae>"`): nenhum e-mail corporativo.
- [ ] **29. Autotestes, commit final e etiqueta.**
  ```
  node --test app/teste.mjs
  node scripts/gco.mjs autoteste
  python indicadores/indicadores.py autoteste
  git status
  git tag -a entrega -m "Entrega do piloto"
  git push origin main entrega
  ```
  A etiqueta só é criada com tudo em commit na `main`. Se for preciso corrigir depois, criem `entrega-2`: etiqueta não se move.
- [ ] **30. Documento.** Preencham o documento do Projeto Final com o que ocorreu, a avaliação por resultado e a nova versão do TO-BE, com o endereço `https://github.com/J4kedi/piloto-gco/tree/entrega`.
- [ ] **31. Entregar no Canvas,** com o mesmo endereço, até as 23h59.

## Indicadores

**Da auditoria (passo 15).** No checklist respondido, contem C, NC e NA em cada bloco, de A a E. A conformidade do bloco é C dividido por C mais NC. Só os números vêm para a ficha GCO5 e para o relatório.

**Do histórico do repositório da empresa (passo 16).** No clone do repositório da empresa, em Git Bash. Os comandos só leem e só mostram números na tela; `<base>` é o hash anotado no passo 3, e `<branch>`, a branch da mudança.

```
git log <base>..<branch> --no-merges --format=%s | wc -l
git log <base>..<branch> --no-merges --format=%s | grep -c -E "^(feat|fix|perf|refactor|build|ci|test|docs|chore|revert)!?: .+ \(#[0-9]+\)$"
git fetch origin
git log <base>..origin/main --first-parent --no-merges --oneline | wc -l
```

O primeiro número são os commits da mudança; o segundo, os que seguem a orientação; o último, os commits que chegaram à `main` sem merge desde a base. Se a empresa integra por squash ou por rebase, o último número não distingue commit direto: confiram pelos pull requests.

**O script `indicadores/indicadores.py` é da simulação.** Ele lê a pasta em que está, exige a etiqueta `v0.1.0`, só conta commits em `app/`, `infra/`, `scripts/` e `.github/` e depende do log de `gco.mjs`. A coleta grava `registros/historico.json` com título e corpo de pull request, login e nome de arquivo. Por isso:

- não rodem `coletar` com este repositório apontado para o repositório da empresa, nem copiem `historico.json` ou `indicadores.md` de lá para cá;
- se quiserem usá-lo sobre o repositório da empresa, façam tudo na pasta privada: um clone separado, só para leitura, com a pasta `indicadores/` copiada para dentro dele e uma etiqueta local `v0.1.0` na `<base>`, nunca enviada. O que o script grava fica em `registros/` desse clone. Esse uso não foi ensaiado, não serve se o repositório da empresa já tiver uma etiqueta `v0.1.0`, e os indicadores 5, 6, 7 e 9 saem "sem ocorrência", por falta do log;
- para este repositório vêm só os números, digitados na ficha.

## Simulação complementar

Os roteiros estão em `cenarios.md`. O calendário recomendado é C3 e C1 na sexta (passo 13) e C4, script avulso, C5 e C7 no sábado (passos 17 e 18). C2 e C6 ficam fora, como não ocorridos; se sobrar tempo, C2 entra antes de C1, e C6, depois de C5. Se faltar tempo, C4 sai. O piloto real tem prioridade sobre a simulação.
