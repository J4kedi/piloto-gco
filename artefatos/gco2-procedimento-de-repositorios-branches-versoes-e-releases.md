# Procedimento de repositórios, branches, versões e releases

Artefato proposto para o resultado GCO 2 (sistema de gerência de configuração e mudanças) do MPS-SW. Descreve como usar o Git e a plataforma de hospedagem como sistema de gerência de configuração. As funções, os acessos e os padrões de nome citados são os do Plano de Gerência de Configuração (seções 3, 4 e 6).

A numeração das versões segue o Semantic Versioning 2.0.0 (PRESTON-WERNER, 2013).

## 1. Criar um repositório

Quem: Responsável por configuração.

1. Crie o repositório privado, com o nome no padrão do Plano e `main` como branch principal.
2. Inclua no primeiro commit: `README` (o que é, como executar e como testar), `.gitignore`, os modelos de demanda e de pull request e a configuração de build e de implantação. Segredos não entram: variáveis de produção ficam fora do repositório e constam da lista de itens pelo nome.
3. Conceda acesso por função, conforme a seção 4 do Plano.
4. Configure a integração: um único método de merge e exclusão da branch depois de integrada. Ative a proteção da `main` (pull request e revisão obrigatórios) quando a plataforma oferecer; sem proteção técnica, a regra vale por procedimento e a auditoria a confere.
5. Registre o repositório na lista de itens do Plano e crie a baseline inicial (Definição de baseline).

## 2. Trabalhar com branches

- `main` é a única branch permanente. Está sempre em condição de ser liberada, e toda versão sai dela.
- Cada demanda tem uma branch própria, criada da `main` atualizada, com o nome `<tipo>/<nº da demanda>-<resumo>`. O tipo é o da Orientação de commits. Exemplo: `feat/131-exportar-relatorio`.
- A branch dura o tempo da demanda: é integrada por pull request e apagada depois da integração.
- Alteração em item de nível "PR obrigatório" só chega à `main` por pull request com a demanda, a classificação, a evidência de teste e a forma de reversão preenchidas, e com revisão de outra pessoa.
- Correção urgente segue o mesmo caminho, em branch `fix/...` criada da `main`, com a aprovação emergencial registrada antes do primeiro commit. A revisão pode ocorrer depois da liberação, no prazo da seção 8 do Plano.

| Passo | Comando |
|---|---|
| Criar a branch | `git switch main`, `git pull`, `git switch -c <tipo>/<n>-<resumo>` |
| Publicar | `git push -u origin <tipo>/<n>-<resumo>` e abertura do pull request |
| Integrar | merge do pull request revisado; a branch é apagada |

## 3. Numerar versões

Toda versão liberada tem o número `vX.Y.Z`.

| Sobe | Quando | Exemplo |
|---|---|---|
| Z (correção) | Correção sem comportamento novo, inclusive emergencial. | `v1.4.1` → `v1.4.2` |
| Y (menor) | Funcionalidade nova, ou mudança que pede configuração nova para implantar (variável de ambiente, serviço). | `v1.4.2` → `v1.5.0` |
| X (maior) | Mudança incompatível: interface que some ou muda de formato, banco de dados que a versão anterior não lê. | `v1.5.0` → `v2.0.0` |

- Ao subir um número, os da direita voltam a 0.
- Correção no código sai sempre com número novo; número publicado não é reutilizado.
- Correção só em item fora do repositório (por exemplo, variável de produção) libera de novo a mesma versão, com registro.

## 4. Publicar uma release

Quem: Responsável por configuração, depois da homologação.

1. Liste o que entrou desde a última versão (`git log <última versão>..main --oneline --no-merges`) e defina o número pela seção 3.
2. Escreva as notas da versão: o que mudou, para quem e como voltar.
3. Crie a baseline: etiqueta anotada no commit homologado da `main` e release de mesmo nome, com as notas (Definição de baseline).
   ```
   git tag -a vX.Y.Z <commit homologado> -m "vX.Y.Z"
   git push origin vX.Y.Z
   ```
4. Libere a partir da etiqueta, nunca de uma branch nem de um commit sem etiqueta.
5. Verifique a versão em produção e preencha o registro de liberação. Se a verificação falhar, volte à versão anterior e escreva a nota de incidente.

## Referência

PRESTON-WERNER, Tom. Semantic Versioning 2.0.0. 2013. Disponível em: https://semver.org/spec/v2.0.0.html.
