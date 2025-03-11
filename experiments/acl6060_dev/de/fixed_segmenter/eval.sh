#!/bin/bash

for log_path in final/segment-length_8.0_step-length_*/instances.log; do
    python3 ${REPO_ROOT_PATH}/tools/stream_laal.py --simuleval-instances $log_path  \
            --reference ${REPO_ROOT_PATH}/data/acl6060_dev/de/tgt_segments.txt \
            --audio-yaml ${REPO_ROOT_PATH}/data/acl6060.yaml \
            --sacrebleu-tokenizer 13a \
            --latency-unit word > $(dirname $log_path)/scores.resegmented.tsv
done