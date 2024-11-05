#!/bin/bash

# Check if a file and number of iterations are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <result_file> <iterations>"
    exit 1
fi

# Assign arguments to variables
result_file="$1"
iterations="$2"

# Validate that the iterations input is a positive integer
if ! [[ "$iterations" =~ ^[0-9]+$ ]] || [ "$iterations" -le 0 ]; then
    echo "Error: Iterations must be a positive integer."
    exit 1
fi

# Create the result file if it does not exist
if [ ! -f "$result_file" ]; then
    touch "$result_file"
    echo "Created output file: $result_file"
fi

# Run the python script for the specified number of iterations
for ((i=1; i<=iterations; i++)); do
    python othello.py | grep -v "pygame" >> "$result_file"

    percent=$(( i * 100 / iterations ))
    echo "Progress: $percent% completed ($i of $iterations games)"
done

echo "Completed $iterations iterations, results saved to $result_file"
