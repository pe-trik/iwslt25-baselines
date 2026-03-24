#!/bin/bash

export PYTHONPATH="${REPO_ROOT_PATH}"
export LD_LIBRARY_PATH="${REPO_ROOT_PATH}/iwslt25_env/lib/python3.10/site-packages/nvidia/cudnn/lib"

segment_length=$1
step_length=$2
translation_la_policy=$3
transcript_context=${4}
translation_max_input_length_soft=${5}

output_dir=${6}/segment-length_${segment_length}_step-length_${step_length}_translation-la-policy_${translation_la_policy}_transcript-context_${transcript_context}_translation-max-input-length-soft_${translation_max_input_length_soft}

if [[ -f $output_dir/scores.tsv ]]
then
    echo $output_dir/scores.tsv exists - exiting
    exit 0
fi

mkdir -p $output_dir

# Creates necessary config YAML dynamically
# If the agent.py or underlying class is updated, the default arguments may need to be updated
cat > simulstream_wrapper_for_simuleval_config.yaml <<EOF
type: "simulstream.server.speech_processors.simuleval_wrapper.SimulEvalWrapper"
simuleval_agent: "agent.CascadeAgentWitFixedLengthSegmenter"
latency_unit: word
speech_chunk_size: 1.0  # seconds
detokenizer_type: "simuleval"

source_segment_size: 100
step_length: ${step_length}
whisper_model: "large-v2"
device: "cuda"
translation_language: "it"
segment_length: ${segment_length}
translation_la_policy: ${translation_la_policy}
transcript_context: ${transcript_context}
translation_max_input_length_soft: ${translation_max_input_length_soft}

# need to include a bunch of previously default arguments
whisper_language: "en"
translation_model: "facebook/m2m100_418M"
translation_max_input_length_hard: 40
whisper_task: "transcribe"
EOF

simulstream_inference --speech-processor-config simulstream_wrapper_for_simuleval_config.yaml \
    --wav-list-file ${REPO_ROOT_PATH}/data/MCIF_AUDIO/wav_list.txt \
    --tgt-lang it --src-lang en --metrics-log-file ${output_dir}/metrics.jsonl

simulstream_score_quality --scorer sacrebleu \
    --eval-config simulstream_wrapper_for_simuleval_config.yaml \
    --log-file ${output_dir}/metrics.jsonl \
    --references ${REPO_ROOT_PATH}/data/it/tgt.it

simulstream_stats --eval-config simulstream_wrapper_for_simuleval_config.yaml \
    --log-file ${output_dir}/metrics.jsonl
