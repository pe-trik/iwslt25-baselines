#!/bin/bash

export PYTHONPATH=${REPO_ROOT_PATH}
export LD_LIBRARY_PATH="${PYTHON_ENV_DIR}/lib/python3.10/site-packages/nvidia/cudnn/lib"

segment_length=$1
step_length=$2
output_dir=$3/segment-length_${segment_length}_step-length_${step_length}

mkdir -p $output_dir

simuleval \
    --agent agent.py \
    --source-segment-size 250 \
    --source ${REPO_ROOT_PATH}/data/cs_en_dev/cs_en/src.txt \
    --target ${REPO_ROOT_PATH}/data/cs_en_dev/cs_en/tgt.txt \
    --step-length $step_length \
    --output $output_dir \
    --device cuda \
    --seamless-m4t-tgt-lang eng \
    --segment-length $segment_length 
