#!/bin/bash
export MWERSEGMENTER_ROOT=${REPO_ROOT_PATH}/tools/mwerSegmenter

for log_path in final/segment*/instances.log; do
    if [ -f $(dirname $log_path)/scores.tsv ] && [ ! -f $(dirname $log_path)/scores.resegmented.tsv ] ; then
        echo "Evaluating $log_path"
    else
        echo "Skipping $log_path"
        continue
    fi
    python3 ${REPO_ROOT_PATH}/tools/stream_laal.py --simuleval-instances $log_path  \
            --reference ${REPO_ROOT_PATH}/data/acl6060_dev/de/tgt_segments.txt \
            --audio-yaml ${REPO_ROOT_PATH}/data/acl6060.yaml \
            --sacrebleu-tokenizer 13a \
            --latency-unit word > $(dirname $log_path)/scores.resegmented.tsv
done