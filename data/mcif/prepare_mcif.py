#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import re
import os
import argparse


def load_segments_from_xml(xml_path: str):
    """
    Parse the XML and return a dict:
        { task_num (int): { 'docid': str, 'tgt_segs': [str], 'src_segs': [str] } }

    Tasks are keyed by the integer X in iid="TRANS_X".
    Each segment list is split on blank lines within <reference> / <transcript>.
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    trans_pattern = re.compile(r'^TRANS_(\d+)$')
    docs = {}

    for sample in root.iter('sample'):
        iid = sample.get('iid', '')
        m = trans_pattern.match(iid)
        if not m:
            continue

        task_num = int(m.group(1))

        audio_path = sample.findtext('audio_path', '').strip()
        docid = os.path.splitext(audio_path)[0]  # strip extension

        reference = sample.findtext('reference') or ''
        transcript_el = sample.find('metadata/transcript')
        transcript = transcript_el.text if transcript_el is not None and transcript_el.text else ''

        def to_segments(text):
            # Split on blank lines to get segments
            segs = re.split(r'\n{2,}', text.strip())
            return [s.strip() for s in segs if s.strip()]

        docs[task_num] = {
            'docid': docid,
            'tgt_segs': to_segments(reference),
            'src_segs': to_segments(transcript),
        }

    return docs


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("xml", type=str)
    parser.add_argument("wav_dir", type=str)
    parser.add_argument("save_dir", type=str)
    args = parser.parse_args()

    docs = load_segments_from_xml(args.xml)

    lang_id = args.xml.split('.')[-3]
    save_dir = os.path.join(args.save_dir, lang_id)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    docs = sorted(docs.items(), key=lambda x: x[0])

    with open(os.path.join(save_dir, "src.txt"), "w") as src_f, \
         open(os.path.join(save_dir, "tgt.txt"), "w") as tgt_f, \
         open(os.path.join(save_dir, "tgt_segments.txt"), "w") as tgt_seg_f, \
         open(os.path.join(save_dir, "transcript.txt"), "w") as transcript_f, \
         open(os.path.join(save_dir, "transcript_segments.txt"), "w") as transcript_seg_f, \
         open(os.path.join(wav_dir, "wav_list.txt") as wav_list_f:

        for task_num, doc in docs:
            docid = doc['docid']
            tgt_segs = doc['tgt_segs']
            src_segs = doc['src_segs']

            doc_wav_path = os.path.join(args.wav_dir, f"{docid}.wav")
            assert os.path.exists(doc_wav_path), f"Audio file {doc_wav_path} not found"

            src_f.write(f"{doc_wav_path}\n")

            wav_list_f.write(f"{docid}.wav")

            tgt_f.write(" ".join(tgt_segs).replace("\n", " ") + "\n")
            for seg in tgt_segs:
                tgt_seg_f.write(f"{seg.strip()}\n")

            transcript_f.write(" ".join(src_segs).replace("\n", " ") + "\n")
            for seg in src_segs:
                transcript_seg_f.write(f"{seg.strip()}\n")

    print(f"Wrote outputs for {len(docs)} TRANS tasks to {save_dir}/ and wav_list.txt to {wav_dir} for SimulStream use")
