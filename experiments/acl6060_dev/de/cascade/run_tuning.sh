# for segment_length in 8 12 16 20 24 28 30
# do
#     for transcript_context in 0
#     do
#         for step_length in 0.50 #0.75 1.00 1.25 1.50 1.75 2.00
#         do
#             for translation_la_policy in 1 #3 4 5 6 7 8
#             do 
#                 for translation_max_input_length_soft in 0 #5 10 15 20 25 30
#                 do
#                     bash run_simuleval.sh $segment_length $step_length $translation_la_policy $transcript_context $translation_max_input_length_soft tuning
#                 done
#             done
#         done
#     done
# done

# for segment_length in 24
# do
#     for transcript_context in 0 5 10 15 20 25 30
#     do
#         for step_length in 0.50 #0.75 1.00 1.25 1.50 1.75 2.00
#         do
#             for translation_la_policy in 1 #3 4 5 6 7 8
#             do 
#                 for translation_max_input_length_soft in 0 #5 10 15 20 25 30
#                 do
#                     bash run_simuleval.sh $segment_length $step_length $translation_la_policy $transcript_context $translation_max_input_length_soft tuning
#                 done
#             done
#         done
#     done
# done

for segment_length in 24
do
    for transcript_context in 30
    do
        for step_length in 0.50 #0.75 1.00 1.25 1.50 1.75 2.00
        do
            for translation_la_policy in 1 #3 4 5 6 7 8
            do 
                for translation_max_input_length_soft in 0 5 10 15 20 25 30
                do
                    bash run_simuleval.sh $segment_length $step_length $translation_la_policy $transcript_context $translation_max_input_length_soft tuning
                done
            done
        done
    done
done