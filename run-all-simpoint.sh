#!/bin/bash

# Run the gem5 commands in parallel
./build/ALL/gem5.opt -re --outdir=outputs/simpoint0-run configs/tutorial/chapter2/9/simpoint-run.py --sid=0 &
pid0=$!
./build/ALL/gem5.opt -re --outdir=outputs/simpoint1-run configs/tutorial/chapter2/9/simpoint-run.py --sid=1&
pid1=$!
./build/ALL/gem5.opt -re --outdir=outputs/simpoint2-run configs/tutorial/chapter2/9/simpoint-run.py --sid=2 &
pid2=$!

# Array of PIDs and SIDs
pids=($pid0 $pid1 $pid2)
sids=(0 1 2)

# Loop to wait for each process and echo a message when it finishes
for i in "${!pids[@]}"; do
    wait ${pids[$i]} && echo "gem5 with sid ${sids[$i]} finished"
done

# Wait for all background jobs to finish
wait
