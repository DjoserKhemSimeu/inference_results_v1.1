#!/bin/bash

CSV_FILE="/media/nvidia/177d5801-095d-441b-88e2-959056c30fac/scratch/save_data/consommation_energie_jetson.csv"
OUTFILE="/tmp/outxx.txt"

echo "timestamp,gpu_power" > "$CSV_FILE"

# Lancer tegrastats en arrière-plan
tegrastats --interval 50 --logfile "$OUTFILE" > /dev/null 2>&1 &
TEGRASTATS_PID=$!
echo $TEGRASTATS_PID > /tmp/tegrastats_pid.txt
echo "TegraStats lancé avec le PID : $TEGRASTATS_PID"

# Attendre que le fichier commence à être rempli
while [ ! -s "$OUTFILE" ]; do
    sleep 0.1
done

start_time=$(date +%s.%3N)

# Lancer toute la boucle dans un sous-processus & stocker le PID
(
    tail -f "$OUTFILE" | while read -r line; do
        gpu_power=$(echo "$line" | grep -oP 'GPU \K\d+')

        current_time=$(date +%s.%3N)
        elapsed_time=$(echo "$current_time - $start_time" | bc)

        if [ -n "$gpu_power" ]; then
            echo "$elapsed_time,$gpu_power" >> "$CSV_FILE"
        fi
    done
) &
LOOP_PID=$!
echo $LOOP_PID > /tmp/loop_pid.txt
echo "Boucle lancée avec le PID : $LOOP_PID"
