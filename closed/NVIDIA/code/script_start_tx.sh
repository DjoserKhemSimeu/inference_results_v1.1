#!/bin/bash

LOG_DIR="/tmp/scratch/save_data"
LOG_FILE="${LOG_DIR}/consommation_energie_gpu.csv"
PID_FILE="/tmp/nv_measure.pid"

# Création du dossier de log si nécessaire
mkdir -p "$LOG_DIR"

# En-tête du fichier CSV
echo "timestamp,gpu_power" > "$LOG_FILE"

# Boucle de mesure en tâche de fond
(
    START_TIME=$(date +%s.%N)
    while true; do
        CURRENT_TIME=$(date +%s.%N)
        ELAPSED=$(echo "$CURRENT_TIME - $START_TIME" | bc)
        POWER=$(nvidia-smi --query-gpu=power.draw --format=csv,noheader,nounits | head -n 1)
        echo "${ELAPSED},${POWER}" >> "$LOG_FILE"
        sleep 0.01
    done
) &

# Enregistre le PID du processus en arrière-plan
echo $! > "$PID_FILE"
echo "Mesure de puissance GPU lancée avec PID $(cat $PID_FILE)"
