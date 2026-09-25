# 04 — Checklist de Bolso · administradora

> **Instrumento de campo.** Levar impresso ou no celular e preencher **na hora**.
> Aqui só a pergunta e o espaço da resposta.
> 🔴 = trava trabalho já feito · 🟡 = importante · ⚪ = bom ter

## ⚡ Se só der tempo de oito

Estas oito destravam as contas do `calculista`, o parecer e a meta do mês 1. **Se o dia render só
isso, foi um bom dia.**

`A-1` taxa de administração · `A-2` fundo de reserva · `A-5` índice de reajuste ·
`B-1` histórico de contemplação · `B-2` % de lance vencedor · `B-3` lance embutido ·
`D-1` análise de crédito na contemplação · `A-9/A-10` meta mensal e antecipação do credenciamento

## 🎯 Antes de sair, peça DOCUMENTO — não resposta oral

Papel responde sozinho metade da lista, não depende de memória e não muda de versão:

- [ ] **Tabela de comissionamento** vigente (por linha e faixa)
- [ ] **Contrato de representação** — cópia integral
- [ ] **Regulamento de um grupo** de imóvel e de um de pesados
- [ ] **Extrato/relatório de assembleias** dos últimos 12 meses de 2 ou 3 grupos
- [ ] **Material de marketing aprovado** + regra de uso da marca
- [ ] Acesso ao **simulador** e ao sistema de vendas

---

# CONVERSA 1 — Gerente / líder de equipe
*Contrato, comissão, operação.*

**🔴 A-9** — Existe meta no período de entrada (credenciamento)? Ela é **mensal** ou **cumulativa**?
→ ______________________________________________

**🔴 A-10** — Superar a meta **antecipa** o credenciamento, ou o período é prazo fixo?
→ ______________________________________________

**🟡 A-11** — Cliente cancela no mês 3: o que acontece com as parcelas restantes da minha comissão? Há devolução do já pago?
→ ______________________________________________

**🟡 A-12** — Existe bônus, campanha ou premiação por volume além da escada de comissão?
→ ______________________________________________

**🔴 E-1** — **Eu escolho o grupo** em que aloco a cota, ou o sistema aloca?
→ ______________________________________________

**🟡 E-4** — Posso **dividir comissão** com parceiro indicador (contador)? Existe formato previsto?
→ ______________________________________________

**⚪ E-2** — Que dados de grupo o sistema me mostra? Dá para exportar?
→ ______________________________________________

**⚪ E-3** — O simulador oficial calcula o quê? O que ele **não** calcula?
→ ______________________________________________

**⚪ E-5** — Regras de uso da marca e quais peças são aprovadas?
→ ______________________________________________

**⚪** — Há custo fixo, exclusividade ou multa no contrato PJ?
→ ______________________________________________

---

# CONVERSA 2 — Produto / operações de grupo
*É a conversa que quase nenhum vendedor pede. Onde está o ouro.*

### Custos

**🔴 A-1** — **Taxa de administração total** por linha e prazo (% sobre o crédito)?
→ imóvel: _________ | pesados: _________ | auto: _________ | serviços: _________

**🔴 A-2** — **Fundo de reserva**: % e em que condições é devolvido?
→ ______________________________________________

**🟡 A-3** — **Seguro** é obrigatório? Qual o % ao mês?
→ ______________________________________________

**🟡 A-4** — **Taxa de adesão** e há antecipação de taxa de administração nas primeiras parcelas?
→ ______________________________________________

**🔴 A-5** — **Índice de reajuste** do crédito (INCC, IPCA, outro) e periodicidade?
→ ______________________________________________

### Contemplação

**🔴 B-1** — **Histórico dos últimos 12 meses**: quantas contemplações por assembleia, quantas por sorteio e quantas por lance?
→ ______________________________________________

**🔴 B-2** — **% de lance vencedor** histórico neste grupo?
→ mín: _________ | médio: _________ | máx: _________

**🔴 B-3** — Modalidades de lance: livre, fixo — e **qual o % máximo de lance embutido**?
→ ______________________________________________

**🟡 B-4** — Existe contemplação garantida por prazo ou algum mecanismo de antecipação?
→ ______________________________________________

**🟡 B-5** — Prazo médio entre lance vencedor e **liberação da carta**?
→ ______________________________________________

### Saúde do grupo

**🟡 C-1** — Índice de **inadimplência** e de **cancelamento** por grupo?
→ ______________________________________________

**⚪ C-2** — Nº de participantes × cotas. Quais grupos estão em formação e quais em andamento?
→ ______________________________________________

**🟡 C-3** — Quem desiste: como é a devolução, quando e com que desconto?
→ ______________________________________________

**⚪ C-4** — Existem grupos por perfil (PJ, imóvel comercial, frota)?
→ ______________________________________________

---

# CONVERSA 3 — Crédito
*A conversa que evita estorno. Quase ninguém faz.*

**🔴 D-1** — **Análise de crédito na contemplação**: quais critérios a PJ precisa atender para a carta ser liberada?
→ ______________________________________________

**🟡 D-2** — Que **garantias** são exigidas para liberar a carta (imóvel, avalista, alienação do bem)?
→ ______________________________________________

**🔴 D-3** — A carta pode ser usada para **quitar financiamento existente**? *(binário: decide se uma tese de substituição de financiamento existe)*
→ ______________________________________________

**🟡 D-3b** — Outras restrições de uso: imóvel pronto, terreno, construção, reforma?
→ ______________________________________________

**🟡 D-4** — Prazo de **validade da carta** após a contemplação?
→ ______________________________________________

---

## Depois da visita

- [ ] Lançar as respostas em `config/consultor.json` (`produto.*`, `comissao.*`), **com documento e
  data de origem** — sem fonte, o número não entra
- [ ] Refazer as contas e as teses que dependiam de valor que mudou
- [ ] Se **A-9/A-10** mudarem a conta, revisitar a meta do mês 1
- [ ] Se **D-3** for negativo, marcar como morta a tese que dependa de quitar financiamento — não só
  vetada
- [ ] Se **E-1** for "eu escolho o grupo", isso vira **produto seu** — registrar em
  `governanca/decisions-log.md`
