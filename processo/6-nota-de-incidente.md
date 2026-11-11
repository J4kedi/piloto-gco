# 6. Nota de incidente

- **Quando:** toda vez que se usa `node scripts/gco.mjs reverter`, ou que produção falha depois de uma liberação. Uma nota por incidente.
- **Quem:** Desenvolvedor(a) investiga a causa (tarefa Investigar causa); Responsável por configuração escreve a nota (tarefa Registrar incidente).
- **Onde:** `registros/incidentes/AAAA-MM-DD-<slug>.md`, com a data da detecção e um slug curto, sem acento, com hífens.

## Como preencher

- **Versão:** a versão que falhou, `vX.Y.Z`.
- **Demanda:** `#N` da demanda que gerou a versão.
- **Detectado em:** data e hora, `AAAA-MM-DDTHH:MM-03:00` (pode vir da linha `verificar` do log).
- **Efeito:** o que deixou de funcionar e para quem.
- **Reversão usada:** o comando ou meio usado para voltar.
- **Causa confirmada:** `sim` se a causa foi comprovada (reproduzida ou vista no ambiente); senão, `não`.
- **Causa:** o que provocou a falha.
- **Correção:** o que foi feito e onde ficou registrado (PR, issue ou alteração em item fora do repositório).

Depois da nota:

- Causa em item fora do repositório, como `infra/producao.env`: tarefa Corrigir configuração, descrita no campo `Correção`.
- Causa no código: tarefa Solicitar correção urgente, que abre nova demanda e segue `processo/2-classificacao.md` (em geral, `emergencial`).

## Modelo

```markdown
# Incidente AAAA-MM-DD <título curto>

- Versão: [PREENCHER - autores]
- Demanda: [PREENCHER - autores]
- Detectado em: [PREENCHER - autores]
- Efeito: [PREENCHER - autores]
- Reversão usada: [PREENCHER - autores]
- Causa confirmada: [PREENCHER - autores]
- Causa: [PREENCHER - autores]
- Correção: [PREENCHER - autores]
```
