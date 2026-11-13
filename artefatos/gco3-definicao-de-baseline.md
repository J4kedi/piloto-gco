# Definição de baseline

Artefato proposto para o resultado GCO 3 (baselines) do MPS-SW. Define o que compõe cada baseline, quando ela é criada e como é controlada.

**Baseline** é o conjunto de itens de configuração, em versões determinadas, que foi homologado e aprovado para liberação e que só muda por nova mudança controlada. Este processo usa um tipo de baseline, a de produção: uma por versão liberada.

## 1. O que compõe a baseline

| Componente | Onde fica | Como a baseline o identifica |
|---|---|---|
| Código-fonte, testes e scripts de banco de dados | Repositório, na `main` | Commit apontado pela etiqueta `vX.Y.Z` |
| Definição de build e configuração de implantação | Repositório, na `main` | O mesmo commit |
| Versões das dependências | Arquivo de travamento, no repositório | O mesmo commit |
| Artefato gerado (imagem ou pacote) | Registro de artefatos ou servidor | Identificador imutável (hash), no registro de liberação |
| Configuração de ambiente de produção | Fora do repositório | Nomes das variáveis exigidas, nas notas da versão; os valores nunca são registrados |
| Documentos e diagramas do projeto (requisitos, arquitetura, modelos de processo) | Repositório, na `main`, ou o local oficial indicado no Plano | O mesmo commit, ou a versão de cada documento citada nas notas da versão |
| Notas da versão | Release `vX.Y.Z` | Texto da release |
| Cópia de segurança dos dados anterior à liberação | Armazenamento de cópias | Nome e impressão digital, no registro de liberação |

Branches de trabalho e commits que não estão na `main` não fazem parte de nenhuma baseline.

## 2. Quando é criada

- Uma baseline por versão liberada em produção, criada depois da homologação e antes da liberação.
- Condições: todas as mudanças da versão integradas por pull request revisado, ou com aprovação emergencial registrada; homologação concluída sem falha no commit que será etiquetado; notas da versão escritas.
- Baseline inicial: ao adotar o processo num repositório existente, o estado que está em produção recebe a primeira etiqueta, que passa a ser o marco das auditorias.

## 3. Identificação e aprovação

- Identificação: etiqueta anotada `vX.Y.Z` no commit homologado e release de mesmo nome. O número segue o Procedimento de repositórios, branches, versões e releases (seção 3).
- Quem cria: Responsável por configuração.
- Aprovação: o comitê de controle de mudanças aprova a baseline antes da etiqueta. Numa equipe pequena, o comitê não é um grupo novo: é a direção com o Responsável por configuração (Plano, seção 3). A aprovação, com quem aprovou e quando, fica no registro de liberação. Quem cria a etiqueta confere antes as condições da seção 2 e fica identificado nela.

## 4. Controle

- Nenhuma baseline é alterada sem a permissão do comitê de controle de mudanças.
- A etiqueta é imutável: não se move nem se apaga. Erro na baseline corrige-se com nova versão, aprovada pelo comitê.
- O conteúdo só muda por nova demanda, que percorre o controle de mudança e gera nova baseline.
- Produção executa sempre uma baseline: o artefato liberado é o identificado no registro de liberação, gerado do commit da etiqueta, sem reconstrução.
- Correção em componente fora do repositório não cria baseline: a mesma versão é liberada de novo, e a alteração fica no registro de liberação ou na nota de incidente.
- Voltar à versão anterior é voltar à baseline anterior, que permanece disponível até a seguinte ser verificada em produção.
- A retenção de artefatos e de cópias de segurança é a da seção 7 do Plano de Gerência de Configuração.
- A auditoria confere as baselines pelos itens 9 a 12 do Checklist de auditoria de configuração.

## 5. Como consultar

| Pergunta | Comando |
|---|---|
| Quais baselines existem | `git tag --list "v*" --sort=v:refname` |
| Quem criou a baseline, quando e em que commit | `git show vX.Y.Z --no-patch` |
| O que entrou entre duas baselines | `git log vA..vB --oneline --no-merges` |
| Como obter o conteúdo de uma baseline | `git switch --detach vX.Y.Z` |
