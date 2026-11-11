# 7. Registro de script avulso

**Script avulso** é qualquer comando ou script rodado à mão contra produção, ou contra o banco dela, fora do fluxo de liberação. Exemplos: carga ou correção de dados, limpeza, consulta que altera estado.

- **Quando registrar:** toda execução, inclusive a que falhou, logo depois de executar.
- **Quem registra:** quem executou, no papel de Responsável por configuração.
- **Onde:** `registros/scripts-avulsos.csv`, uma linha por execução. Separador `;`, UTF-8 com BOM (o formato em que a planilha em português abre e salva).

| Coluna | O que vai |
|---|---|
| `data` | `AAAA-MM-DD` ou `DD/MM/AAAA` |
| `script` | O comando exato, ou o caminho do arquivo executado |
| `versao` | Versão ativa em produção no momento, `vX.Y.Z` |
| `motivo` | Por que foi preciso |
| `quem` | Login do GitHub |
| `resultado` | `ok` ou `falha` |

Se o comando tiver `;`, a planilha põe o campo entre aspas. Editando o arquivo à mão, ponha você as aspas.

Na planilha de tarefas, a execução vira uma linha com a tarefa Executar script avulso e `artefato` = `registros/scripts-avulsos.csv`.

Este registro não alimenta indicador. A auditoria confere se cada linha está completa (`processo/8-auditoria-e-restauracao.md`, Conferir registros).
