#!/bin/bash

CSV_FILE="/media/nvidia/177d5801-095d-441b-88e2-959056c30fac/scratch/save_data/consommation_energie_jetson_pue.csv"
OUTFILE="/tmp/outxx.txt"

echo "timestamp,total_power" > "$CSV_FILE"

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
        cpu_power=$(echo "$line" | grep -oP 'CPU \K\d+')
        sys_power=$(echo "$line" | grep -oP 'SYS5V \K\d+')
	soc_power=$(echo "$line" | grep -oP 'SOC \K\d+')
	cv_power=$(echo "$line" | grep -oP 'CV \K\d+')
        vddq_power=$(echo "$line" | grep -oP 'VDDRQ \K\d+')

        # Calculate total power
        total_power=$((gpu_power + cpu_power + sys_power + soc_power + cv_power + vddq_power))

        current_time=$(date +%s.%3N)
        elapsed_time=$(echo "$current_time - $start_time" | bc)

        if [ -n "$total_power" ]; then
            echo "$elapsed_time,$total_power" >> "$CSV_FILE"
        fi
    done
) &
LOOP_PID=$!
echo $LOOP_PID > /tmp/loop_pid.txt
echo "Boucle lancée avec le PID : $LOOP_PID"
