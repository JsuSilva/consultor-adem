#!/usr/bin/env bash
# Serve a raiz do repositório em localhost; as peças geradas ficam em /saida/.
#
#   bash scripts/servir.sh [porta]
set -euo pipefail
PORTA="${1:-9797}"
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
cd "$RAIZ"

if lsof -nP -iTCP:"$PORTA" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "ERRO: porta $PORTA já está em uso:"
  lsof -nP -iTCP:"$PORTA" -sTCP:LISTEN | tail -n +2 | awk '{print "  "$1" (pid "$2")"}'
  echo "Rode com outra porta:  bash scripts/servir.sh 9798"
  exit 1
fi

echo
echo "  Para deixar rodando em segundo plano:"
echo "    nohup python3 scripts/servidor.py $PORTA > /tmp/servidor.log 2>&1 & disown"
echo
exec python3 scripts/servidor.py "$PORTA"
