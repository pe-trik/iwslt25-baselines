#!/bin/bash

export PYTHONPATH="${REPO_ROOT_PATH}"
export LD_LIBRARY_PATH="${REPO_ROOT_PATH}/iwslt25_env/lib/python3.10/site-packages/nvidia/cudnn/lib"

segment_length=$1
step_length=$2

output_dir=$3/segment-length_${segment_length}_step-length_${step_length}

if [[ -f $output_dir/scores.tsv ]]
then
    echo $output_dir/scores.tsv exists - exiting
    exit 0
fi

mkdir -p $output_dir

# Creates necessary config YAML dynamically
cat > simulstream_wrapper_for_simuleval_config.yaml <<EOF
type: "simulstream.server.speech_processors.simuleval_wrapper.SimulEvalWrapper"
simuleval_agent: "agent.SeamlessM4TAgentWithFixedSegmenter"
latency_unit: word
speech_chunk_size: 1.0  # seconds
detokenizer_type: "simuleval"

source_segment_size: 250
step_length: ${step_length}
device: "cuda"
seamless_m4t_tgt_lang: "ita"
segment_length: ${segment_length}

# need to include default arguments
seamless_m4t_model: "facebook/seamless-m4t-v2-large"
eval_latency_unit: "word"
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
