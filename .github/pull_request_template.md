<!--
Preencha todas as seções antes de pedir revisão.
Na linha da demanda, o número da issue depois do #.
Na classificação, normal, risco ou emergencial (processo/2-classificacao.md), e o rótulo de mesmo nome neste PR.
O link da aprovação emergencial só vale para emergencial: o comentário de aprovação, feito por outra pessoa antes do primeiro commit.
Nos itens de configuração afetados, os nomes de processo/1-itens-de-configuracao.md, inclusive os que ficam fora do repositório (como infra/producao.env), e o que muda em cada um.
No risco, o que pode falhar em produção e como se percebe.
Na evidência de teste, comando e resultado; no mínimo, node --test app/teste.mjs.
Na forma de reversão, como voltar se a verificação falhar, e se precisa de algo além de node scripts/gco.mjs reverter.
-->
Demanda: #

Classificação:

Link da aprovação emergencial:

## O que muda

## Itens de configuração afetados

## Risco

## Evidência de teste

## Forma de reversão

## Revisão

Preenche o(a) Revisor(a), que não pode ser quem fez a mudança. Decisão registrada com "Approve" ou "Request changes".

### Conferência rápida (toda mudança)

- [ ] `Demanda: #N` aponta uma issue existente, e o PR faz o que ela pede.
- [ ] O rótulo de classificação está no PR e segue o critério.
- [ ] A seção "Evidência de teste" está preenchida, o teste passou e cobre o que mudou.
- [ ] A forma de reversão está preenchida.
- [ ] Se `emergencial`: a aprovação é anterior ao primeiro commit e de outro login.

### Checklist completo (obrigatório para `risco`)

- [ ] Todos os itens de configuração afetados estão listados, inclusive os de fora do repositório.
- [ ] Variável de ambiente nova: está em `infra/homologacao.env` e em `infra/producao.env.exemplo`, e o PR diz o que pôr em `infra/producao.env`.
- [ ] Serviço novo ou removido em `infra/producao.yml`: `infra/servicos-da-liberacao.txt` e `processo/1-itens-de-configuracao.md` acompanham.
- [ ] Mudança no banco de dados: a forma de reversão diz o que acontece com os dados se a versão for revertida.
- [ ] O risco descrito confere com o que o diff mostra.
