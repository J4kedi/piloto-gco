# Cenários da simulação

A simulação complementa o piloto real (`EXECUCAO.md`): cobre os caminhos que não se pode provocar num ambiente real, como emergência, falha na liberação e desvios plantados para a auditoria achar. O nome do ramo segue a seção 2 de `artefatos/gco2-procedimento-de-repositorios-branches-versoes-e-releases.md` e a mensagem de commit segue `artefatos/gco4-orientacao-de-commits.md`; nas demandas sugeridas, `<tipo>` é `feat` em C1, C2, C5 e C6 e `fix` em C4.

A primeira tabela deste arquivo é lida por `indicadores/indicadores.py`. Não mude as colunas nem os nomes das tarefas: eles são a lista fechada da planilha.

| Cenário | Caminho previsto |
|---|---|
| C1 Mudança normal | Registrar demanda → Classificar mudança → Implementar mudança → Submeter pull request → Revisar mudança → Integrar pull request → Implantar em homologação → Criar baseline → Liberar em produção → Ativar nova versão → Verificar nova versão → Registrar liberação |
| C2 Revisão reprovada | Registrar demanda → Classificar mudança → Implementar mudança → Submeter pull request → Revisar mudança → Corrigir mudança → Submeter pull request → Revisar mudança → Integrar pull request |
| C3 Commit direto | Implementar mudança |
| C4 Mudança emergencial | Registrar demanda → Classificar mudança → Aprovar emergência → Implementar mudança → Submeter pull request → Integrar pull request → Implantar em homologação → Criar baseline → Liberar em produção → Ativar nova versão → Verificar nova versão → Registrar liberação → Revisar mudança |
| C5 Falha na liberação | Registrar demanda → Classificar mudança → Implementar mudança → Submeter pull request → Revisar mudança → Integrar pull request → Implantar em homologação → Criar baseline → Liberar em produção → Ativar nova versão → Verificar nova versão → Restaurar versão anterior → Investigar causa → Registrar incidente → Corrigir configuração → Liberar em produção → Ativar nova versão → Verificar nova versão → Registrar liberação |
| C6 Serviço fora da lista | Registrar demanda → Classificar mudança → Implementar mudança → Submeter pull request → Revisar mudança → Integrar pull request → Implantar em homologação → Criar baseline → Liberar em produção → Ativar nova versão → Verificar nova versão → Registrar liberação |
| C7 Auditoria e restauração | Verificar baselines → Conferir itens de configuração → Conferir registros → Testar restauração → Registrar auditoria |

Observações sobre os caminhos:

- C2 termina na integração. A mudança dele vai para produção junto com a de C1, na `v0.2.0`.
- C3 é só o commit direto. Quem o acusa é a auditoria, em C7 (tarefa Conferir registros).
- C5 volta a liberar a **mesma versão** depois de corrigir `infra/producao.env`: a imagem não muda, só a configuração fora do repositório.
- C6 percorre o mesmo caminho de C1. Quem acusa a divergência é a auditoria, em C7 (tarefa Conferir itens de configuração).

## Papéis

- **Autor A**: Desenvolvedor(a) e Responsável por configuração. Hospeda os contêineres e roda todos os comandos do `gco.mjs`.
- **Autor B**: Solicitante, Revisor(a) e Aprovador emergencial.
- Na auditoria (C7), B faz as conferências no papel de Responsável por configuração, porque os desvios de C3 e C6 foram plantados por A. A só executa a restauração.
- Ninguém revisa a própria mudança.
- O que os roteiros mostram com `gh` também pode ser feito pela página do GitHub.

## Como lançar na planilha

Cada autor lança as próprias tarefas no próprio arquivo: A em `registros/tarefas-autor-a.csv`, B em `registros/tarefas-autor-b.csv`. Uma linha por tarefa, anotada na hora (início e fim).

Colunas: `ciclo;cenario;tarefa;papel;quem;data;inicio;fim;demanda;pr;versao;resultado;artefato;desvio;dificuldade`

- `ciclo`: não é usada; deixe vazia. `cenario`: C1 a C7.
- `tarefa` e `papel`: só os nomes da lista fechada, como aparecem nos roteiros abaixo.
- `quem`: login do GitHub. `data`: `AAAA-MM-DD` ou `DD/MM/AAAA`. `inicio` e `fim`: `HH:MM`.
- `demanda`: número da issue. `pr`: número do PR, puro (ex.: `7`); commit direto vai como `commit <hash curto>` (ex.: `commit a1b2c3d`), para a planilha não converter o hash em número. `versao`: `vX.Y.Z` quando houver.
- `resultado`: o valor indicado em cada passo; quando o passo diz "vazio", deixe em branco.
- `artefato`: endereço ou caminho do que a tarefa gerou.
- `desvio` e `dificuldade`: texto dos autores, quando houver.

No Excel: feche o arquivo antes de `git pull`. Ao salvar, use "CSV UTF-8 (delimitado por vírgulas)" ou mantenha o formato em que o arquivo abriu; o leitor aceita `;` ou `,`.

Os registros (`registros/`, `fichas/`) entram direto na `main`, sem PR, a qualquer momento. A baseline etiqueta o commit do último `homologar` ok e recusa se `app/`, `infra/`, `scripts/` ou `.github/` mudaram entre ele e o `HEAD`.

## Calendário de referência

A ordem do piloto inteiro, com o piloto real, está em `EXECUCAO.md`. Na simulação:

| Dia | O que | Versão sugerida |
|---|---|---|
| sexta, 13/11 | preparo (`README.md`); C3; C1 | `v0.1.0` (preparo); `v0.2.0` (C1, com C3) |
| sábado, 14/11 | C4; script avulso; C5; C7; indicadores | `v0.2.1` (C4); `v0.3.0` (C5) |

As versões seguem a seção 3 de `artefatos/gco2-procedimento-de-repositorios-branches-versoes-e-releases.md`; na simulação, X fica em 0. Se algo mudar a ordem, ajuste o número. Mantenha o script avulso antes de C5: leva poucos minutos e põe recados no banco para a restauração de C7 ter o que conferir.

C2 e C6 ficam fora desse calendário e sem ocorrência:

- C2: nenhuma reprovação nem tarefa Corrigir mudança.
- C6: nenhuma divergência plantada; a auditoria só tem o desvio de C3 para achar, `Divergências` fica 0 e C7 restaura `v0.3.0`.

**Se sobrar tempo:** C2 antes de C1 (a mudança dele sai na `v0.2.0`) e C6 depois de C5 (`v0.4.0`), antes de C7.

**Se faltar tempo:** deixe C4 de fora. Não há emergência, o indicador 4 sai "sem ocorrência" e as versões passam a ser `v0.2.0` (C1, com C3) e `v0.3.0` (C5).

Declare no `RELATORIO.md`, em "O que não ocorreu", o que ficou de fora.

## C1 Mudança normal

Pré-condição: preparo feito, `v0.1.0` ativa em produção. C2 e C3 já feitos (a `v0.2.0` leva as mudanças deles). Sugestão de demanda: `GET /recados` passa a listar do mais novo para o mais antigo.

1. **Autor B · Solicitante.** Abre a demanda pelo modelo "Demanda", urgência normal: `gh issue create` (escolha o modelo "Demanda").
   - Planilha: **Registrar demanda** · resultado vazio · artefato: endereço da issue
2. **Autor A · Desenvolvedor(a).** Classifica pelo critério de `processo/2-classificacao.md` e põe o rótulo na issue: `gh issue edit <n> --add-label normal`
   - Planilha: **Classificar mudança** · resultado `normal` · artefato: endereço da issue
3. **Autor A · Desenvolvedor(a).** Implementa num ramo, com teste.
   ```
   git switch main
   git pull
   git switch -c <tipo>/<n>-<resumo>
   node --test app/teste.mjs
   git add app
   git commit -m "<tipo>: <resumo> (#<n>)"
   git push -u origin <tipo>/<n>-<resumo>
   ```
   - Planilha: **Implementar mudança** · resultado vazio · artefato: `<tipo>/<n>-<resumo>`
4. **Autor A · Desenvolvedor(a).** Abre o PR e preenche todas as seções do modelo (`Demanda: #<n>`, `## Evidência de teste` com a saída do teste): `gh pr create --label normal`
   - Planilha: **Submeter pull request** · resultado vazio · artefato: endereço do PR
5. **Autor B · Revisor(a).** Faz a conferência rápida (marca os itens no corpo do PR) e aprova: `gh pr review <pr> --approve`
   - Planilha: **Revisar mudança** · resultado `aprovada` · artefato: endereço da revisão
6. **Autor A · Responsável por configuração.** Integra: `gh pr merge <pr> --merge`
   - Planilha: **Integrar pull request** · resultado vazio · artefato: endereço do PR
7. **Autor A · Responsável por configuração.** Implanta em homologação a partir da `main` atualizada.
   ```
   git switch main
   git pull
   node scripts/gco.mjs homologar
   ```
   - Planilha: **Implantar em homologação** · resultado vazio · artefato: `registros/execucoes.csv`
8. **Autor A · Responsável por configuração.** Escreve `registros/notas-v0.2.0.md` pelo modelo de `processo/4-versao-e-notas.md` (pode fazer commit dele na `main`) e cria a baseline: `node scripts/gco.mjs baseline v0.2.0 --notas registros/notas-v0.2.0.md`
   - Planilha: **Criar baseline** · resultado vazio · artefato: endereço da Release
9. **Autor A · Responsável por configuração.** `node scripts/gco.mjs liberar v0.2.0`
   - Planilha: **Liberar em produção** · resultado vazio · artefato: `copias/antes-v0.2.0.db`
10. **Autor A · Responsável por configuração.** `node scripts/gco.mjs ativar v0.2.0`
    - Planilha: **Ativar nova versão** · resultado vazio · artefato: `registros/execucoes.csv`
11. **Autor A · Responsável por configuração.** `node scripts/gco.mjs verificar v0.2.0`
    - Planilha: **Verificar nova versão** · resultado `sem falha` · artefato: `registros/execucoes.csv`
12. **Autor A · Responsável por configuração.** `node scripts/gco.mjs registrar v0.2.0 --demanda <n>`. Depois, commit dos registros na `main`.
    - Planilha: **Registrar liberação** · resultado vazio · artefato: endereço da Release

## C2 Revisão reprovada

Pré-condição: preparo feito. Sugestão de demanda: recusar recado com texto acima de 280 caracteres. Para a reprovação, a primeira entrega vai sem teste do comportamento novo.

1. **Autor B · Solicitante.** `gh issue create` (modelo "Demanda").
   - Planilha: **Registrar demanda** · resultado vazio · artefato: endereço da issue
2. **Autor A · Desenvolvedor(a).** `gh issue edit <n> --add-label normal`
   - Planilha: **Classificar mudança** · resultado `normal` · artefato: endereço da issue
3. **Autor A · Desenvolvedor(a).** Implementa no ramo `<tipo>/<n>-<resumo>` (comandos do passo 3 de C1), sem teste para o limite novo.
   - Planilha: **Implementar mudança** · resultado vazio · artefato: `<tipo>/<n>-<resumo>`
4. **Autor A · Desenvolvedor(a).** `gh pr create --label normal`
   - Planilha: **Submeter pull request** · resultado vazio · artefato: endereço do PR
5. **Autor B · Revisor(a).** Na conferência rápida, a evidência de teste não cobre o que mudou. Reprova: `gh pr review <pr> --request-changes --body "<motivo>"`
   - Planilha: **Revisar mudança** · resultado `reprovada` · artefato: endereço da revisão
6. **Autor A · Desenvolvedor(a).** Acrescenta o teste no mesmo ramo, roda `node --test app/teste.mjs`, faz commit e `git push`.
   - Planilha: **Corrigir mudança** · resultado vazio · artefato: `commit <hash curto>` da correção
7. **Autor A · Desenvolvedor(a).** Atualiza `## Evidência de teste` no corpo do PR e pede nova revisão: `gh pr edit <pr> --add-reviewer <login de B>`
   - Planilha: **Submeter pull request** · resultado vazio · artefato: endereço do PR (o mesmo)
8. **Autor B · Revisor(a).** Nova conferência rápida e aprovação: `gh pr review <pr> --approve`
   - Planilha: **Revisar mudança** · resultado `aprovada` · artefato: endereço da revisão
9. **Autor A · Responsável por configuração.** `gh pr merge <pr> --merge`
   - Planilha: **Integrar pull request** · resultado vazio · artefato: endereço do PR

## C3 Commit direto

Pré-condição: preparo feito. O desvio é de propósito e fica sem demanda, sem PR e sem aviso a B, que só o procura na auditoria (C7).

1. **Autor A · Desenvolvedor(a).** Faz uma alteração pequena, que não quebra o teste, num arquivo de `app/` (por exemplo, um comentário) e envia direto para a `main`.
   ```
   git switch main
   git pull
   node --test app/teste.mjs
   git add app
   git commit -m "<resumo>"
   git push origin main
   ```
   - Planilha: **Implementar mudança** · resultado vazio · artefato: `commit <hash curto>` · `pr`: `commit <hash curto>` (ex.: `commit a1b2c3d`) · `desvio`: texto dos autores

## C4 Mudança emergencial

Pré-condição: `v0.2.0` ativa (C1 feito). Sugestão de demanda: `GET /recados/` (com barra no fim) responde 404 e deve responder como `GET /recados`, tratado como urgente na simulação. A aprovação tem de vir **antes** do primeiro commit.

1. **Autor B · Solicitante.** `gh issue create` (modelo "Demanda"), urgência: urgente, com o motivo.
   - Planilha: **Registrar demanda** · resultado vazio · artefato: endereço da issue
2. **Autor A · Desenvolvedor(a).** `gh issue edit <n> --add-label emergencial`
   - Planilha: **Classificar mudança** · resultado `emergencial` · artefato: endereço da issue
3. **Autor B · Aprovador emergencial.** Comenta na issue, em linha que começa com `Aprovação emergencial:`
   ```
   gh issue comment <n> --body "Aprovação emergencial: <motivo>"
   ```
   - Planilha: **Aprovar emergência** · resultado `aprovada` · artefato: endereço do comentário
4. **Autor A · Desenvolvedor(a).** Só depois do passo 3: implementa no ramo `<tipo>/<n>-<resumo>` (comandos do passo 3 de C1).
   - Planilha: **Implementar mudança** · resultado vazio · artefato: `<tipo>/<n>-<resumo>`
5. **Autor A · Desenvolvedor(a).** `gh pr create --label emergencial`, com o link do comentário de aprovação no modelo.
   - Planilha: **Submeter pull request** · resultado vazio · artefato: endereço do PR
6. **Autor A · Responsável por configuração.** Integra sem revisão prévia: `gh pr merge <pr> --merge`
   - Planilha: **Integrar pull request** · resultado vazio · artefato: endereço do PR
7. **Autor A · Responsável por configuração.** `git switch main`, `git pull`, `node scripts/gco.mjs homologar`
   - Planilha: **Implantar em homologação** · resultado vazio · artefato: `registros/execucoes.csv`
8. **Autor A · Responsável por configuração.** Notas em `registros/notas-v0.2.1.md`; `node scripts/gco.mjs baseline v0.2.1 --notas registros/notas-v0.2.1.md`
   - Planilha: **Criar baseline** · resultado vazio · artefato: endereço da Release
9. **Autor A · Responsável por configuração.** `node scripts/gco.mjs liberar v0.2.1`
   - Planilha: **Liberar em produção** · resultado vazio · artefato: `copias/antes-v0.2.1.db`
10. **Autor A · Responsável por configuração.** `node scripts/gco.mjs ativar v0.2.1`
    - Planilha: **Ativar nova versão** · resultado vazio · artefato: `registros/execucoes.csv`
11. **Autor A · Responsável por configuração.** `node scripts/gco.mjs verificar v0.2.1`
    - Planilha: **Verificar nova versão** · resultado `sem falha` · artefato: `registros/execucoes.csv`
12. **Autor A · Responsável por configuração.** `node scripts/gco.mjs registrar v0.2.1 --demanda <n>`
    - Planilha: **Registrar liberação** · resultado vazio · artefato: endereço da Release
13. **Autor B · Revisor(a).** Em até um dia útil depois da liberação, revisa no PR já integrado (conferência rápida; checklist completo se a mudança também tocar banco de dados, autenticação, pagamentos ou implantação): `gh pr review <pr> --approve`
    - Planilha: **Revisar mudança** · resultado `aprovada` · artefato: endereço da revisão

## C5 Falha na liberação

Pré-condição: `v0.2.1` ativa (C4 feito) e recados carregados pelo script avulso. A mudança passa a exigir uma variável de ambiente nova (sugestão: `LIMITE_RECADOS`, máximo de recados por listagem, com o nome acrescentado em `EXIGIDAS`, em `app/servidor.mjs`); sem ela, `/saude` responde 503. O PR acrescenta a variável só em `infra/homologacao.env`; `infra/producao.env` fica sem ela, de propósito.

1. **Autor B · Solicitante.** `gh issue create` (modelo "Demanda").
   - Planilha: **Registrar demanda** · resultado vazio · artefato: endereço da issue
2. **Autor A · Desenvolvedor(a).** Exige configuração nova para implantar, logo é risco: `gh issue edit <n> --add-label risco`
   - Planilha: **Classificar mudança** · resultado `risco` · artefato: endereço da issue
3. **Autor A · Desenvolvedor(a).** Implementa no ramo `<tipo>/<n>-<resumo>`: acrescenta o nome da variável em `EXIGIDAS` (`app/servidor.mjs`) e a linha `<NOME>=<valor>` em `infra/homologacao.env`; não mexe em `infra/producao.env` (`git add app infra`).
   - Planilha: **Implementar mudança** · resultado vazio · artefato: `<tipo>/<n>-<resumo>`
4. **Autor A · Desenvolvedor(a).** `gh pr create --label risco`. Em "Itens de configuração afetados", lista só `infra/homologacao.env`.
   - Planilha: **Submeter pull request** · resultado vazio · artefato: endereço do PR
5. **Autor B · Revisor(a).** Checklist completo. Deixa passar, de propósito, o item da variável nova em produção, e aprova: `gh pr review <pr> --approve`
   - Planilha: **Revisar mudança** · resultado `aprovada` · artefato: endereço da revisão · `desvio`: texto dos autores
6. **Autor A · Responsável por configuração.** `gh pr merge <pr> --merge`
   - Planilha: **Integrar pull request** · resultado vazio · artefato: endereço do PR
7. **Autor A · Responsável por configuração.** `git switch main`, `git pull`, `node scripts/gco.mjs homologar`
   - Planilha: **Implantar em homologação** · resultado vazio · artefato: `registros/execucoes.csv`
8. **Autor A · Responsável por configuração.** Notas em `registros/notas-v0.3.0.md`; `node scripts/gco.mjs baseline v0.3.0 --notas registros/notas-v0.3.0.md`
   - Planilha: **Criar baseline** · resultado vazio · artefato: endereço da Release
9. **Autor A · Responsável por configuração.** `node scripts/gco.mjs liberar v0.3.0`
   - Planilha: **Liberar em produção** · resultado vazio · artefato: `copias/antes-v0.3.0.db`
10. **Autor A · Responsável por configuração.** `node scripts/gco.mjs ativar v0.3.0`
    - Planilha: **Ativar nova versão** · resultado vazio · artefato: `registros/execucoes.csv`
11. **Autor A · Responsável por configuração.** `node scripts/gco.mjs verificar v0.3.0` (deve sair com código 1).
    - Planilha: **Verificar nova versão** · resultado `com falha` · artefato: `registros/execucoes.csv`
12. **Autor A · Responsável por configuração.** `node scripts/gco.mjs reverter`
    - Planilha: **Restaurar versão anterior** · resultado vazio · artefato: `registros/execucoes.csv`
13. **Autor A · Desenvolvedor(a).** Procura a causa: a linha `verificar` de `registros/execucoes.csv` mostra `/saude 503`; compare a lista `EXIGIDAS` de `app/servidor.mjs` com as variáveis de `infra/homologacao.env` e de `infra/producao.env`.
    - Planilha: **Investigar causa** · resultado `confirmada` · artefato: caminho da nota de incidente
14. **Autor A · Responsável por configuração.** Copia o modelo de `processo/6-nota-de-incidente.md` para `registros/incidentes/AAAA-MM-DD-<slug>.md` e preenche.
    - Planilha: **Registrar incidente** · resultado vazio · artefato: caminho da nota
15. **Autor A · Responsável por configuração.** Acrescenta a variável em `infra/producao.env` e descreve a alteração no campo `Correção` da nota. Se `infra/producao.env.exemplo` também precisar dela, isso é outra demanda, por PR, fora deste cenário.
    - Planilha: **Corrigir configuração** · resultado vazio · artefato: `infra/producao.env` (fora do repositório)
16. **Autor A · Responsável por configuração.** Libera de novo a mesma versão: `node scripts/gco.mjs liberar v0.3.0`
    - Planilha: **Liberar em produção** · resultado vazio · artefato: `copias/antes-v0.3.0.db`
17. **Autor A · Responsável por configuração.** `node scripts/gco.mjs ativar v0.3.0`
    - Planilha: **Ativar nova versão** · resultado vazio · artefato: `registros/execucoes.csv`
18. **Autor A · Responsável por configuração.** `node scripts/gco.mjs verificar v0.3.0`
    - Planilha: **Verificar nova versão** · resultado `sem falha` · artefato: `registros/execucoes.csv`
19. **Autor A · Responsável por configuração.** `node scripts/gco.mjs registrar v0.3.0 --demanda <n>`
    - Planilha: **Registrar liberação** · resultado vazio · artefato: endereço da Release

## C6 Serviço fora da lista

Pré-condição: `v0.3.0` ativa (C5 fechado). O PR acrescenta um serviço novo por slot em `infra/producao.yml` (sugestão de nomes: `relatorio-azul` e `relatorio-verde`) e **não** toca em `infra/servicos-da-liberacao.txt` nem em `processo/1-itens-de-configuracao.md`, de propósito. B não roda `situacao` antes da auditoria.

1. **Autor B · Solicitante.** `gh issue create` (modelo "Demanda").
   - Planilha: **Registrar demanda** · resultado vazio · artefato: endereço da issue
2. **Autor A · Desenvolvedor(a).** Mexe na composição de produção, logo é risco: `gh issue edit <n> --add-label risco`
   - Planilha: **Classificar mudança** · resultado `risco` · artefato: endereço da issue
3. **Autor A · Desenvolvedor(a).** Implementa no ramo `<tipo>/<n>-<resumo>` (`git add infra`).
   - Planilha: **Implementar mudança** · resultado vazio · artefato: `<tipo>/<n>-<resumo>`
4. **Autor A · Desenvolvedor(a).** `gh pr create --label risco`
   - Planilha: **Submeter pull request** · resultado vazio · artefato: endereço do PR
5. **Autor B · Revisor(a).** Checklist completo. Deixa passar, de propósito, o item do serviço novo, e aprova: `gh pr review <pr> --approve`
   - Planilha: **Revisar mudança** · resultado `aprovada` · artefato: endereço da revisão · `desvio`: texto dos autores
6. **Autor A · Responsável por configuração.** `gh pr merge <pr> --merge`
   - Planilha: **Integrar pull request** · resultado vazio · artefato: endereço do PR
7. **Autor A · Responsável por configuração.** `git switch main`, `git pull`, `node scripts/gco.mjs homologar`
   - Planilha: **Implantar em homologação** · resultado vazio · artefato: `registros/execucoes.csv`
8. **Autor A · Responsável por configuração.** Notas em `registros/notas-v0.4.0.md`; `node scripts/gco.mjs baseline v0.4.0 --notas registros/notas-v0.4.0.md`
   - Planilha: **Criar baseline** · resultado vazio · artefato: endereço da Release
9. **Autor A · Responsável por configuração.** `node scripts/gco.mjs liberar v0.4.0`
   - Planilha: **Liberar em produção** · resultado vazio · artefato: `copias/antes-v0.4.0.db`
10. **Autor A · Responsável por configuração.** `node scripts/gco.mjs ativar v0.4.0`
    - Planilha: **Ativar nova versão** · resultado vazio · artefato: `registros/execucoes.csv`
11. **Autor A · Responsável por configuração.** `node scripts/gco.mjs verificar v0.4.0`
    - Planilha: **Verificar nova versão** · resultado `sem falha` · artefato: `registros/execucoes.csv`
12. **Autor A · Responsável por configuração.** `node scripts/gco.mjs registrar v0.4.0 --demanda <n>`
    - Planilha: **Registrar liberação** · resultado vazio · artefato: endereço da Release

## C7 Auditoria e restauração

Pré-condição: C3 e C6 feitos; todas as planilhas e `registros/execucoes.csv` com commit na `main`. A auditoria roda na máquina do Autor A, na raiz do repositório, com B no teclado nas conferências. Comandos e critérios completos em `processo/8-auditoria-e-restauracao.md`; os itens verificados são os de `artefatos/gco5-checklist-de-auditoria-de-configuracao.md`.

1. **Autor B · Responsável por configuração.** Verifica as baselines.
   ```
   git tag --list "v*" --sort=v:refname
   gh release list
   node scripts/gco.mjs situacao
   ```
   - Planilha: **Verificar baselines** · resultado: número de desvios (esperado `0`) · artefato: `registros/auditorias/AAAA-MM-DD.md`
2. **Autor B · Responsável por configuração.** Confere os itens de configuração.
   ```
   docker compose -p gco-prod --env-file infra/.slots.env -f infra/producao.yml config --services
   docker compose -p gco-prod ps --format "table {{.Service}}\t{{.State}}"
   node scripts/gco.mjs situacao
   ```
   - Planilha: **Conferir itens de configuração** · resultado: número de desvios (esperado `1`, o serviço de C6) · artefato: `registros/auditorias/AAAA-MM-DD.md`
3. **Autor B · Responsável por configuração.** Confere os registros.
   ```
   git fetch origin --tags
   git log --first-parent --no-merges --date=iso --format="%h %an %ad %s" v0.1.0..origin/main -- app infra scripts .github
   gh api "repos/{owner}/{repo}/commits/<hash>/pulls" --jq length
   python indicadores/indicadores.py coletar
   python indicadores/indicadores.py
   ```
   - Planilha: **Conferir registros** · resultado: número de desvios (esperado `1`, o commit de C3) · artefato: `registros/auditorias/AAAA-MM-DD.md`
4. **Autor A · Responsável por configuração.** Executa a restauração da última versão liberada; B confere os recados em `http://localhost:8081/recados`: `node scripts/gco.mjs restaurar v0.4.0`
   - Planilha: **Testar restauração** · resultado `aprovada` · artefato: `registros/execucoes.csv`
5. **Autor B · Responsável por configuração.** Copia o modelo de `processo/8-auditoria-e-restauracao.md` para `registros/auditorias/AAAA-MM-DD.md`, preenche, cola abaixo dos campos a tabela do checklist respondida e abre uma issue para cada desvio encontrado.
   - Planilha: **Registrar auditoria** · resultado: número de desvios (esperado `2`) · artefato: `registros/auditorias/AAAA-MM-DD.md`

Depois de C7, com tudo em commit na `main`: `python indicadores/indicadores.py coletar` e `python indicadores/indicadores.py`. A saída fica em `registros/indicadores.md` e alimenta o `RELATORIO.md`.

## Script avulso

Não pertence a nenhum cenário: na planilha, deixe `cenario` vazio. Pré-condição: `v0.2.x` ativa. Sugestão: carregar alguns recados em produção, para que a cópia do banco feita em C5 e C6 tenha dados e a restauração de C7 tenha o que conferir.

1. **Autor A · Responsável por configuração.** Executa o script contra a porta de produção:
   ```
   node -e "[1, 2, 3, 4, 5].forEach(i => fetch('http://localhost:8080/recados', {method: 'POST', headers: {'content-type': 'application/json'}, body: JSON.stringify({texto: 'recado ' + i})}).then(r => console.log(i, r.status)))"
   ```
   Registra a execução em `registros/scripts-avulsos.csv`, conforme `processo/7-registro-de-script-avulso.md`.
   - Planilha: **Executar script avulso** · resultado vazio · artefato: `registros/scripts-avulsos.csv`
