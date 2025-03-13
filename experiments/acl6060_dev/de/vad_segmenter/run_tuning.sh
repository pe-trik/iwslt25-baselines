for max_unvoiced_length in 0.5 #0.1 0.3 0.5 0.7 0.9
do
    for voice_threshold in 0.1 #0.2 0.3 0.4 0.5 0.6
    do
        for step_length in inf # 0.5 0.75 1.0 1.25 1.5 1.75 2.0
        do
            sbatch run_simuleval.sh $max_unvoiced_length $voice_threshold $step_length tuning
        done
    done
done