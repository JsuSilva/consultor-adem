# Registro de Decisões

> Registro **append-only**. Cada decisão do consultor ganha um `D-0XX` e nunca é editada no lugar —
> se muda, entra uma decisão nova que supera a anterior. Aqui vive o *porquê*.
> O *que falta / em andamento / entregue* está no [`BACKLOG.md`](./BACKLOG.md).
> Como os dois funcionam: [`README.md`](./README.md).

## Formato de cada entrada

```markdown
### D-001 — Título curto, que já diz a decisão
**Data:** AAAA-MM-DD · **Estado:** vigente · **fonte:** consultor (DD/MM) · **supera** D-0XX

**Contexto:** o que aconteceu, ou o que estava em aberto, e levou à decisão.

**Decisão:** o que fica valendo, em itens numerados quando houver mais de um.

**Aval:** a palavra do consultor, citável — trecho entre aspas da mensagem em que ele aprovou.
```

- **Numeração** sequencial, sem pular e sem reaproveitar número.
- **Estado:** `vigente` ao nascer. A entrada antiga não é editada: quem a supera é a nova, que diz
  qual supera.
- **supera / complementa / corrige** D-0XX, quando for o caso; omitir quando não houver.
- Entradas separadas por `---`, a mais nova embaixo.
- Sem aval citável, não entra aqui: vira pergunta ao consultor.

---
