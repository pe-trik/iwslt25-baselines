for max_unvoiced_length in 0.1
do
    for voice_threshold in 0.1 
    do
        for step_length in 0.5 0.75 1.0 1.25 1.5 1.75 2.0
        do
            bash run_simuleval.sh $max_unvoiced_length $voice_threshold $step_length final
        done
    done
done