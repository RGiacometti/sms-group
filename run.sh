#!/usr/bin/env bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

if [ -f ".env" ]; then
    echo "Fichier .env detecte (charge par python-dotenv)"
fi

echo "Demarrage de la passerelle SMS..."
nohup python main.py >> gateway.log 2>&1 &
PID=$!
echo "Passerelle SMS demarree en arriere-plan (PID: $PID)"
echo "Logs: tail -f gateway.log"
echo "Arret: kill $PID"
