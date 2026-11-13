# Plano de Gerência de Configuração

Artefato proposto para o resultado GCO 1 (itens e níveis de controle) do MPS-SW. É um modelo: copie este arquivo para o projeto, substitua cada `[PREENCHER]` e apague as instruções em itálico. O plano preenchido contém dados da organização e não entra neste repositório.

A estrutura segue as atividades de gerência de configuração da IEEE Std 828-2012 (planejamento, identificação, controle de mudanças, registro da situação, auditoria e gerência de liberação) e cobre o que o Guia Geral MPS de Software:2024 espera do processo Gerência de Configuração (GCO). A redação é dos autores.

| Projeto | Versão do plano | Data | Elaborado por (função) | Aprovado por (função) |
|---|---|---|---|---|
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |

## 1. Escopo

- Sistema ou produto: [PREENCHER]
- Repositórios e ambientes cobertos: [PREENCHER]
- Fora do escopo, com o motivo: [PREENCHER]
- Revisão do plano: [PREENCHER] *(sugestão: a cada auditoria e sempre que mudar a ferramenta, o ambiente ou a equipe)*

## 2. Itens de configuração e critério de escolha

Critério de escolha: [PREENCHER] *(sugestão: é item de configuração tudo o que, alterado sem controle, muda o que executa em produção ou impede reconstruir uma versão liberada)*

| Item | Tipo | Local oficial | Responsável | Nível de controle |
|---|---|---|---|---|
| [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] | [PREENCHER] |

*Uma linha por item. Tipos usuais: código-fonte, script de banco de dados, definição de build, configuração de implantação, configuração de ambiente (variáveis e segredos, pelo nome, nunca pelo valor), artefato gerado, dados e cópias de segurança, documentos e diagramas do projeto (requisitos, arquitetura, modelos de processo) e modelos do processo. A gerência de configuração cobre documentos e diagramas, não só código. O responsável é uma função da seção 3.*

Níveis de controle:

- **PR obrigatório:** o item fica no repositório e só muda por pull request revisado e integrado à branch principal.
- **Registro obrigatório:** o item fica fora do repositório ou é gerado; não passa por pull request, mas toda mudança deixa registro (notas da versão, registro de liberação ou nota de incidente).
- **Livre:** o item muda sem pull request; o histórico do repositório é o registro.

## 3. Responsabilidades por função

| Função | Responsabilidade na gerência de configuração | Quem exerce |
|---|---|---|
| Solicitante | Registra a demanda e recebe as notas da versão. | [PREENCHER] |
| Desenvolvedor(a) | Classifica a mudança, implementa em branch própria, escreve os commits e abre o pull request. | [PREENCHER] |
| Revisor(a) | Revisa mudança que não é sua e registra a decisão. | [PREENCHER] |
| Responsável por configuração | Mantém este plano e a lista de itens, integra, cria baselines, libera, registra e conduz a auditoria. | [PREENCHER] |
| Aprovador emergencial | Aprova a emergência antes da implementação. | [PREENCHER] |
| Comitê de controle de mudanças | Aprova as mudanças de risco e as baselines; nenhuma baseline muda sem a permissão dele. Numa equipe pequena, é a direção com o Responsável por configuração. | [PREENCHER] |

*Uma pessoa pode acumular funções, mas ninguém revisa nem audita a própria mudança.*

## 4. Controle de acesso

| Recurso | Leitura | Escrita | Administração |
|---|---|---|---|
| Repositório | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Branch principal | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Ambiente de homologação | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Ambiente de produção | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Segredos e variáveis de produção | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Cópias de segurança | [PREENCHER] | [PREENCHER] | [PREENCHER] |

*Preencha por função, não por pessoa.*

- Como o acesso é concedido e revogado, e por quem: [PREENCHER]
- Revisão dos acessos: [PREENCHER] *(sugestão: a cada auditoria e a cada entrada ou saída de pessoa)*

## 5. Ferramenta

- Controle de versão e hospedagem dos repositórios: [PREENCHER]
- Registro de demandas: [PREENCHER]
- Build e implantação: [PREENCHER]
- Onde ficam os registros de liberação, de incidente e de auditoria: [PREENCHER]
- Cópia de segurança dos repositórios e dos registros: [PREENCHER]

## 6. Nomenclatura

| Elemento | Padrão | Exemplo |
|---|---|---|
| Repositório | [PREENCHER] | [PREENCHER] |
| Branch | `<tipo>/<nº da demanda>-<resumo>` | `fix/128-limite-de-texto` |
| Mensagem de commit | `<tipo>: <resumo> (#<nº da demanda>)` | `fix: recusa texto acima do limite (#128)` |
| Versão, etiqueta e release | `vX.Y.Z` | `v1.4.2` |
| Registros | [PREENCHER] | [PREENCHER] |

As regras completas estão no Procedimento de repositórios, branches, versões e releases e na Orientação de commits.

## 7. Baselines

- Tipos de baseline e momento de criação: [PREENCHER]
- Quem cria e quem aprova: [PREENCHER]
- Retenção de artefatos e de cópias de segurança: [PREENCHER]

Composição e controle: Definição de baseline.

## 8. Controle de mudança

- Onde a mudança é solicitada e registrada: [PREENCHER]

| Classe | Critério | Quem aprova | Revisão exigida |
|---|---|---|---|
| Normal | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| De risco | [PREENCHER] | [PREENCHER] | [PREENCHER] |
| Emergencial | [PREENCHER] | [PREENCHER] | [PREENCHER] |

## 9. Liberação

- Quem libera e em que janela: [PREENCHER]
- Condições para liberar (homologação, baseline, cópia de segurança): [PREENCHER]
- Verificação depois de liberar e critério para voltar à versão anterior: [PREENCHER]
- Registros gerados: notas da versão, registro de liberação e, havendo falha, nota de incidente.

## 10. Auditoria

- Periodicidade: [PREENCHER]
- Quem audita: [PREENCHER] *(não audita mudança própria)*
- Instrumento: Checklist de auditoria de configuração.
- Tratamento das não conformidades (responsável e prazo): [PREENCHER]
- Teste de restauração (periodicidade e ambiente): [PREENCHER]

## Referências

IEEE. IEEE Std 828-2012: IEEE Standard for Configuration Management in Systems and Software Engineering. New York: IEEE, 2012.

SOFTEX. Guia Geral MPS de Software:2024. Junho de 2024.
