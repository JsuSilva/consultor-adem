#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A forma canônica de um telefone brasileiro — regra única deste repositório.

Por que existe: o mesmo celular aparece escrito de duas formas. Lista antiga e base pública
guardam muito celular sem o nono dígito (`48 9903-3594`), e o que sai do WhatsApp e do CRM
vem com ele (`48 99903-3594`). Sem uma forma canônica, a mesma pessoa vira dois cards na
cadência, e a busca do card no CRM erra, porque lá o cadastro tem onze dígitos.

A regra (**uma regra, um lugar, um formato no disco**): o número é normalizado **na escrita**,
e quem lê só compara string com string. Nenhum consumidor reimplementa isto — importa daqui.

    from telefone import canonico
    canonico("(48) 9903-3594")   → "48999033594"
    canonico("+55 37 3229-1234") → "3732291234"   (fixo, fica com dez)

A regra:
  1. fica só com os dígitos;
  2. 12 ou 13 dígitos começando em 55 → tira o código do país;
  3. 10 dígitos e o assinante começando em 6, 7, 8 ou 9 → celular antigo, insere o 9 depois
     do DDD;
  4. 10 dígitos e o assinante começando em 2, 3, 4 ou 5 → é fixo e fica com dez. No Brasil
     fixo não começa em 6–9, então não há zona cinzenta;
  5. 11 dígitos com assinante em 9 → já é canônico;
  6. qualquer outra forma — oito dígitos sem DDD, onze sem o 9 — **não se adivinha**:
     `canonico` devolve os dígitos como estão e `suspeito` devolve True, para quem chamou
     sinalizar em vez de seguir.
"""
import re

__all__ = ["so_digitos", "canonico", "suspeito"]


def so_digitos(valor):
    return re.sub(r"\D", "", valor or "")


def _sem_ddi(d):
    return d[2:] if len(d) in (12, 13) and d.startswith("55") else d


def canonico(valor):
    """Devolve o telefone na forma canônica, só dígitos. Ver a regra no topo do módulo."""
    d = _sem_ddi(so_digitos(valor))
    if len(d) == 10 and d[2] in "6789":
        return d[:2] + "9" + d[2:]
    return d


def suspeito(valor):
    """True quando o número não cai em nenhuma forma reconhecida — quem chamou sinaliza."""
    d = _sem_ddi(so_digitos(valor))
    if len(d) == 10:
        return d[2] not in "23456789"
    if len(d) == 11:
        return d[2] != "9"
    return True


if __name__ == "__main__":
    import sys
    for bruto in sys.argv[1:]:
        print(f"{bruto!r} → {canonico(bruto)}" + ("  [suspeito]" if suspeito(bruto) else ""))
