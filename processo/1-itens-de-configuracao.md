# 1. Itens de configuração

Seção 2 do Plano de Gerência de Configuração (`artefatos/gco1-plano-de-gerencia-de-configuracao.md`), preenchida para a aplicação de exemplo da simulação.

Quem mantém a lista: Responsável por configuração. Mudou um item (entrou, saiu, mudou de lugar), a lista muda junto. A auditoria confere a lista contra a composição de produção (`processo/8-auditoria-e-restauracao.md`).

| Item | Tipo | Local oficial | Responsável | Nível de controle |
|---|---|---|---|---|
| Código da aplicação | código-fonte | `app/servidor.mjs` e `app/teste.mjs`, na `main` | Desenvolvedor(a) | PR obrigatório |
| Dockerfile da aplicação | definição de imagem | `app/Dockerfile`, na `main` | Desenvolvedor(a) | PR obrigatório |
| Composição de homologação (serviço `app`) | configuração de implantação | `infra/homologacao.yml`, na `main` | Responsável por configuração | PR obrigatório |
| Composição de produção (serviços `app-azul`, `app-verde` e `proxy`) | configuração de implantação | `infra/producao.yml`, na `main` | Responsável por configuração | PR obrigatório |
| Configuração do proxy | configuração de implantação | bloco `configs` de `infra/producao.yml`, na `main` | Responsável por configuração | PR obrigatório |
| Lista de serviços da liberação | configuração de implantação | `infra/servicos-da-liberacao.txt`, na `main` | Responsável por configuração | PR obrigatório |
| Variáveis de homologação | configuração de ambiente | `infra/homologacao.env`, na `main` | Responsável por configuração | PR obrigatório |
| Modelo das variáveis de produção | configuração de ambiente | `infra/producao.env.exemplo`, na `main` | Responsável por configuração | PR obrigatório |
| Variáveis de produção | configuração de ambiente | `infra/producao.env`, na máquina que hospeda os contêineres (fora do repositório) | Responsável por configuração | registro obrigatório |
| Script do processo | script de operação | `scripts/gco.mjs`, na `main` | Responsável por configuração | PR obrigatório |
| Modelos de issue e de pull request | modelo de processo | `.github/`, na `main` | Responsável por configuração | PR obrigatório |
| Imagem da aplicação | artefato de construção | `exemplo-gco:<versão>` na máquina que hospeda os contêineres; ID gravado na baseline | Responsável por configuração | registro obrigatório |
| Estado dos slots | estado da implantação | `infra/.slots.env`, na máquina que hospeda os contêineres (fora do repositório) | Responsável por configuração | registro obrigatório |
| Banco de produção | dados | volume `dados` do projeto `gco-prod` | Responsável por configuração | registro obrigatório |
| Cópias do banco | cópia de dados | `copias/antes-<versão>.db` (de `liberar`) e `copias/restaurada-<versão>.db` (de `restaurar`), na máquina que hospeda os contêineres (fora do repositório) | Responsável por configuração | registro obrigatório |
| Documentos e ferramentas do piloto | documentação | `artefatos/`, `processo/`, `fichas/`, `cenarios.md`, `README.md`, `EXECUCAO.md`, `ENTREVISTA.md`, `RELATORIO.md` e `indicadores/`, na `main` | Responsável por configuração | livre |

## Níveis de controle

- **PR obrigatório:** muda só por pull request integrado na `main`, com rótulo e revisão (`processo/2-classificacao.md`). São os caminhos controlados: `app/`, `infra/`, `scripts/` e `.github/`.
- **Registro obrigatório:** o item fica fora do repositório ou é gerado. Não passa por PR, mas toda mudança deixa registro:
  - Variáveis de produção: o PR que exige variável nova diz o que pôr no arquivo (seção "Itens de configuração afetados"), e as notas da versão também. Correção feita por causa de incidente vai no campo `Correção` da nota de incidente.
  - Imagem, estado dos slots e cópias do banco: alterados só pelos comandos do `gco.mjs`, que registram cada execução em `registros/execucoes.csv`. A imagem e a cópia de cada liberação também ficam no bloco "Registro de liberação" da Release.
  - Banco de produção: muda pela aplicação. Fora dela, só por script avulso registrado em `registros/scripts-avulsos.csv` (`processo/7-registro-de-script-avulso.md`).
- **Livre:** entra direto na `main`, sem PR. O histórico do git é o registro.

Um item está **completo** quando tem tipo, responsável e nível de controle preenchidos.
