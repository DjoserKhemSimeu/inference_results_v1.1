#!/bin/bash

# Check if the qc parameter is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <qc>"
    exit 1
fi

qc=$1

# Loop to run the command 10 times
for i in {1..10}; do
    echo "Running iteration $i"

    # Run the make command
    make run_harness RUN_ARGS="--benchmarks=bert --scenarios=singlestream"

    # Rename the output CSV file
    mv /media/nvidia/177d5801-095d-441b-88e2-959056c30fac/scratch/save_data/consommation_energie_jetson_pue.csv \
       /media/nvidia/177d5801-095d-441b-88e2-959056c30fac/scratch/save_data/consommation_energie_single_xavier_QC_${qc}_${i}_pue.csv

    echo "Finished iteration $i"
done

echo "All iterations completed."
