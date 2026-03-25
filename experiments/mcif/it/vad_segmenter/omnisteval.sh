#!/bin/bash

export MWERSEGMENTER_ROOT=${REPO_ROOT_PATH}/tools/mwerSegmenter

for log_path in final/pause*/instances.log; do
	omnisteval longform \
	  --speech_segmentation ${REPO_ROOT_PATH}/data/mcif_translation.yaml \
	  --ref_sentences_file ${REPO_ROOT_PATH}/data/mcif/it/tgt_segments.txt \
	  --hypothesis_file $log_path \
	  --lang it \
	  --bleu_tokenizer 13a \
      --word_level \
	  --output_folder $(dirname "$log_path")
done
