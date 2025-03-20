#!/bin/bash

export PYTHONPATH="${REPO_ROOT_PATH}"
export LD_LIBRARY_PATH="${REPO_ROOT_PATH}/iwslt25_env/lib/python3.10/site-packages/nvidia/cudnn/lib"

max_unvoiced_length=$1
voice_threshold=$2
step_length=$3
output_dir=final/pause_${max_unvoiced_length}_threshold_${voice_threshold}_step-length_${step_length}

if [[ -f $output_dir/scores.tsv ]]
then
    echo $output_dir/scores.tsv exists - exiting
    exit 0
fi

mkdir -p $output_dir

simuleval \
    --agent agent.py \
    --source-segment-size 250 \
    --source ${REPO_ROOT_PATH}/demos/data/acl6060_dev/ja/src.txt \
    --target ${REPO_ROOT_PATH}/demos/data/acl6060_dev/ja/tgt.txt \
    --step-length $step_length \
    --output $output_dir \
    --device cuda \
    --seamless-m4t-tgt-lang jpn \
    --voice-threshold $voice_threshold \
    --max-unvoiced-length $max_unvoiced_length \
    --eval-latency-unit char \
    --sacrebleu-tokenizer ja-mecab
    