for max_unvoiced_length in 0.1
do
    for voice_threshold in 0.2
    do
        for step_length in 0.50 0.75 1.00 1.25 1.50 1.75 2.00
        do
            sbatch run_simuleval.sh $max_unvoiced_length $voice_threshold $step_length final
        done
    done
done