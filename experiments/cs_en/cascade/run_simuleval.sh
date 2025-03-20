#!/bin/bash
#SBATCH -p gpu-troja,gpu-ms --mem=20G --gres=gpu:1  --cpus-per-task=4 --constraint="gpuram48G|gpuram40G|gpuram16G,gpu_cc8.0|gpu_cc8.6|gpu_cc8.9"


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

simuleval \
    --agent agent.py \
    --source-segment-size 100 \
    --source ${REPO_ROOT_PATH}/data/cs_en_dev/cs_en/src.txt \
    --target ${REPO_ROOT_PATH}/data/cs_en_dev/cs_en/tgt.txt \
    --step-length $step_length \
    --whisper-model large-v2 \
    --output $output_dir \
    --device cuda \
    --whisper-language cs \
    --translation-language en \
    --segment-length $segment_length \
    --translation-la-policy $translation_la_policy \
    --transcript-context $transcript_context \
    --translation-max-input-length-soft $translation_max_input_length_soft
    