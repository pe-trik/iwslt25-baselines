#!/usr/bin/env python3

from collections import defaultdict
import json
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('json', type=str)
    parser.add_argument('tgt_path', type=str)

    args = parser.parse_args()
    devset = json.load(open(args.json, 'r', encoding='utf-8'))

    if not os.path.exists(args.tgt_path):
        os.makedirs(args.tgt_path)

    # remove empty lines
    devset = [line for line in devset if len(line['english']) > 0]

    devset_merged = defaultdict(list)
    for line in devset:
        devset_merged[line['audio']].append(line)

    devset_merged = sorted(devset_merged.items(), key=lambda x: x[0])
    
    with open(os.path.join(args.tgt_path, 'segments.yaml'), 'w', encoding='utf-8') as yaml:
        with open(os.path.join(args.tgt_path, 'tgt_segments.txt'), 'w', encoding='utf-8') as tgt:
            for idx, (audio, lines) in enumerate(devset_merged):
                for line in lines:
                    duration = line['end'] - line['start']
                    audio = audio.replace('audio/', '')
                    yaml.write(f"- {{ duration: {duration}, offset: {line['start']}, speaker_id: speaker{idx}, wav: {audio} }}\n")
                    tgt.write(line['english'].strip() + '\n')
            

    wav_path = os.path.dirname(args.json)
    wav_path = os.path.realpath(wav_path)
    with open(os.path.join(args.tgt_path, 'src.txt'), 'w', encoding='utf-8') as src_f:
        with open(os.path.join(args.tgt_path, 'tgt.txt'), 'w', encoding='utf-8') as tgt_f:
            for idx, (audio, lines) in enumerate(devset_merged):
                src_f.write(os.path.join(wav_path, audio) + '\n')
                tgt = ' '.join([line['english'].strip() for line in lines])
                tgt_f.write(tgt + '\n')

if __name__ == '__main__':
    main()