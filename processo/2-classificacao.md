# 2. Classificação da mudança

Quem classifica: Desenvolvedor(a), na tarefa Classificar mudança, **antes** de implementar.
Como registra: rótulo na issue (`gh issue edit <n> --add-label <classe>`) e o mesmo rótulo no PR (`gh pr create --label <classe>`). Na planilha, `resultado` = a classe.

| Classe | Quando | Revisão |
|---|---|---|
| `normal` | Não se encaixa nas outras duas. | Conferência rápida, antes de integrar. |
| `risco` | Toca banco de dados, autenticação, pagamentos ou implantação. | Checklist completo, antes de integrar. |
| `emergencial` | Produção com falha que não pode esperar o fluxo normal. | Aprovação antes de implementar; revisão depois da liberação, em até um dia útil. |

Neste repositório:

- **Implantação** é qualquer mudança em `infra/`, em `scripts/` ou na imagem (Dockerfile), e toda mudança que exige configuração nova em produção (variável de ambiente, serviço na composição).
- **Banco de dados** é mudança na tabela `recados` ou na forma como a aplicação grava nela.
- Na dúvida entre `normal` e `risco`, use `risco`.

## Emergência

1. Desenvolvedor(a) classifica como `emergencial` e põe o rótulo na issue.
2. Aprovador emergencial, com login diferente de quem vai implementar, comenta na issue (ou no PR) **antes do primeiro commit**, em linha que começa com `Aprovação emergencial:`
   ```
   gh issue comment <n> --body "Aprovação emergencial: <motivo>"
   ```
3. Só então se implementa. O PR leva o rótulo `emergencial` e o link do comentário de aprovação.
4. O PR pode ser integrado e liberado sem revisão prévia. A revisão, por outra pessoa, fica registrada no PR em até um dia útil depois da liberação: conferência rápida, ou checklist completo se a mudança também for de risco.
5. Aprovação negada: comente `Emergência negada: <motivo>`, troque o rótulo da issue para `normal` ou `risco` e siga o fluxo comum.

Na planilha: tarefa Aprovar emergência, `resultado` `aprovada` ou `negada`, artefato = endereço do comentário.

## Regras que valem para todas

- Ninguém revisa a própria mudança.
- Mudança em caminho controlado (`app/`, `infra/`, `scripts/`, `.github/`) só entra na `main` por PR com um dos três rótulos.
- Revisão reprovada: o autor corrige no mesmo ramo, atualiza o PR e pede nova revisão.
