#!/bin/bash

PID_FILE="/tmp/nv_measure.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    echo "Arrêt du processus de mesure avec PID $PID"
    kill "$PID"
    rm -f "$PID_FILE"
else
    echo "Aucun processus de mesure trouvé."
fi
