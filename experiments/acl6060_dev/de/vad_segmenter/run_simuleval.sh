#!/bin/bash

export PYTHONPATH=${REPO_ROOT_PATH}
export LD_LIBRARY_PATH="${PYTHON_ENV_DIR}/lib/python3.10/site-packages/nvidia/cudnn/lib"

max_unvoiced_length=$1
voice_threshold=$2
step_length=$3

output_dir=${4}/pause_${max_unvoiced_length}_threshold_${voice_threshold}_step-length_${step_length}

mkdir -p $output_dir

simuleval \
    --agent agent.py \
    --source-segment-size 250 \
    --source ${REPO_ROOT_PATH}/acl6060_dev/de/src.txt \
    --target ${REPO_ROOT_PATH}/data/acl6060_dev/de/tgt.txt\
    --step-length $step_length \
    --output $output_dir \
    --device cuda \
    --seamless-m4t-tgt-lang deu \
    --voice-threshold $voice_threshold \
    --max-unvoiced-length $max_unvoiced_length
    