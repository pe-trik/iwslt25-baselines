for segment_length in 24
do
    for transcript_context in 30
    do
        for step_length in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
        do
            for translation_la_policy in 1 2 3 4 
            do 
                for translation_max_input_length_soft in 0 #5 10 15 20 25 30
                do
                    bash run_simuleval.sh $segment_length $step_length $translation_la_policy $transcript_context $translation_max_input_length_soft final
                done
            done
        done
    done
done