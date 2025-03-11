#!/bin/bash

for segment_length in 2.0 4.0 6.0 8.0 10.0 12.0 14.0 16.0 18.0 20.0
do
    for step_length in inf # offline translation
    do
        bash run_simuleval.sh $segment_length $step_length tuning
    done
done