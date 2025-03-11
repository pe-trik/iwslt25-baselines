#!/usr/bin/env python3

"""
This script is used to preprocess the ACL 60/60 dev set.
"""

from collections import defaultdict
import os
import xml.etree.ElementTree as ET


def load_segments_from_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    docs = defaultdict(dict)
    for d in root.findall('.//doc'):
        docid = d.attrib['docid']
        for s in d.findall('.//seg'):
            segid = s.attrib['id']
            text = s.text
            docs[docid][segid] = text

    return docs


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("xml", type=str)
    parser.add_argument("wav_dir", type=str)
    parser.add_argument("save_dir", type=str)
    args = parser.parse_args()

    docs = load_segments_from_xml(args.xml)

    lang_id = args.xml.split('.')[-2]
    save_dir = os.path.join(args.save_dir, lang_id)

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    docs = sorted(docs.items(), key=lambda x: x[0])

    with open(os.path.join(args.save_dir, lang_id, f"src.txt"), "w") as src_f:
        with open(os.path.join(args.save_dir, lang_id, f"tgt.txt"), "w") as tgt_f:
            with open(os.path.join(args.save_dir, lang_id, f"tgt_segments.txt"), "w") as tgt_segments_f:
                for docid, segs in docs:
                    doc_wav_path = os.path.join(args.wav_dir, f"{docid}.wav")
                    assert os.path.exists(doc_wav_path), f"Audio file {doc_wav_path} not found"
                    src_f.write(f"{doc_wav_path}\n")
                    seg_text = " ".join(segs.values()).replace("\n", " ")
                    tgt_f.write(f"{seg_text}\n")
                    for seg_text in segs.values():
                        tgt_segments_f.write(f"{seg_text.strip()}\n")

