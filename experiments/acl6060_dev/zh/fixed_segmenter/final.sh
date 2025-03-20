#!/bin/bash

for segment_length in 8.0
do
    for step_length in 0.5 0.75 1.0 1.25 1.5 1.75 2.0
    do
        bash run_simuleval.sh $segment_length $step_length final
    done
done