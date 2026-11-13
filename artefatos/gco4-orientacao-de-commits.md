# Orientação de commits

Artefato proposto para o resultado GCO 4 (registros) do MPS-SW. O histórico de commits é o registro do que mudou em cada item de configuração. Esta orientação padroniza a mensagem, para que a diferença entre duas versões possa ser lida diretamente no histórico.

Completam este resultado as notas da versão e o registro de liberação (`processo/4-versao-e-notas.md`) e a nota de incidente (`processo/6-nota-de-incidente.md`).

O formato é uma adaptação do Conventional Commits 1.0.0 (CONVENTIONAL COMMITS, 2019).

## 1. Formato

```
<tipo>: <resumo> (#<nº da demanda>)

<corpo>

<rodapé>
```

- **Tipo:** um dos tipos da seção 2. Acrescente `!` antes dos dois-pontos em mudança incompatível.
- **Resumo:** o que a mudança faz, no presente, em minúsculas, sem ponto final e com até 72 caracteres. Descreva o efeito para quem usa ou opera, não o arquivo alterado.
- **Demanda:** toda mudança em item de nível "PR obrigatório" cita o número da demanda.
- **Corpo:** opcional em mudança normal e obrigatório em mudança de risco ou emergencial. Diz por que a mudança foi feita, quais itens de configuração afeta e o que muda na implantação (variável nova, alteração no banco de dados).
- **Rodapé:** `BREAKING CHANGE: <o que deixa de funcionar e o que fazer>`, em mudança incompatível.

## 2. Tipos

| Tipo | Uso | Efeito na versão |
|---|---|---|
| `feat` | Funcionalidade nova. | Sobe Y |
| `fix` | Correção de defeito. | Sobe Z |
| `perf` | Melhoria de desempenho, sem comportamento novo. | Sobe Z |
| `refactor` | Reorganização do código, sem comportamento novo. | Sobe Z |
| `build`, `ci` | Build, dependências ou pipeline. | Sobe Z, se altera o que é implantado |
| `test` | Só testes. | Nenhum |
| `docs` | Só documentação. | Nenhum |
| `chore` | Manutenção sem efeito no produto. | Nenhum |
| `revert` | Desfaz um commit anterior, citado no corpo. | Conforme o que foi desfeito |
| qualquer tipo com `!` | Mudança incompatível. | Sobe X |

A versão sobe pelo maior efeito entre os commits desde a última baseline. Mudança que pede configuração nova para implantar sobe Y, qualquer que seja o tipo (Procedimento de repositórios, branches, versões e releases, seção 3).

## 3. Regras

- Um commit contém uma mudança lógica. Correção e funcionalidade não vão no mesmo commit.
- Segredo, dado pessoal e dado de cliente não entram no commit nem na mensagem.
- Commit integrado à `main` não é reescrito. O erro corrige-se com novo commit, `fix` ou `revert`.
- O título do pull request segue o mesmo formato; o commit de merge gerado pela plataforma fica como está.

## 4. Exemplos

```
feat: lista os pedidos do mais novo para o mais antigo (#131)
```

```
fix: aceita o endereço com barra no fim (#140)

A rota respondia 404 quando o endereço terminava com barra.
Itens afetados: código da aplicação. Sem mudança na implantação.
```

```
feat!: troca o formato da data na resposta (#152)

BREAKING CHANGE: a data passa a sair em UTC; quem lê o campo como hora local precisa converter.
```

## 5. O que mudou entre duas versões

| Pergunta | Comando |
|---|---|
| Quais mudanças entraram | `git log vA..vB --oneline --no-merges` |
| Só funcionalidades e correções | `git log vA..vB --oneline --no-merges --grep "^feat" --grep "^fix"` |
| Quais arquivos mudaram | `git diff --stat vA..vB` |
| Em que versão um commit entrou | `git tag --contains <hash>` |

As notas da versão partem da primeira lista: uma linha por demanda, na linguagem de quem usa, mais a configuração nova que a versão exige e a forma de voltar. O registro de liberação tem, no mínimo, versão, demanda, commit, quem liberou, quando e o resultado da verificação.

## Referência

CONVENTIONAL COMMITS. Conventional Commits 1.0.0. 2019. Disponível em: https://www.conventionalcommits.org/en/v1.0.0/.
