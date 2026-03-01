# Data

## MCIF Dev Set
Download and unzip the relevant MCIF components.

```
git clone https://huggingface.co/datasets/FBK-MT/MCIF
cd MCIF
gunzip MCIF.long.*.ref.xml.gz
```

MCIF does not natively include the needed YAML for StreamLAAL regrading, so we have to run a resegmenter that finds timestamps for original segments. Follow instructions here: https://github.com/pe-trik/audio-resegmenter.

Alternatively, download the final YAML file directly:

```
wget https://web.engr.oregonstate.edu/~agostinv/audio-mcif-translation.yaml
```

### Prepare Files for SimulEval
SimulEval requires src.txt and tgt.txt files where each recording and translation is listed on a separate lines.

```
for lang in de zh it
do
    python prepare_mcif.py `pwd -P`MCIF/MCIF.long.${lang}.ref.xml `pwd -P`MCIF/MCIF_DATA/LONG_AUDIO/ .
done
```

## ACL 60/60 Dev Set

### Download
Download and unzip the ACL 60/60 Dev Set:
```
wget https://aclanthology.org/attachments/2023.iwslt-1.2.dataset.zip
unzip 2023.iwslt-1.2.dataset.zip
```
### Prepare YAML File for Evaluation
The dev set does not include YAML file, so we have to run a resegmenter that finds timestamps for original segments. Follow instructions here: https://github.com/pe-trik/audio-resegmenter.

Alternatively, download the final YAML file directly:
```
wget https://raw.githubusercontent.com/pe-trik/audio-resegmenter/refs/heads/master/examples/acl6060-dev/acl6060.yaml
```

### Prepare Files for SimuEval
SimulEval requires src.txt and tgt.txt files where each recording and translation is listed on a separate lines.

```
for lang in de zh ja
do
    python prepare_acl6060_dev.py `pwd -P`/2/acl_6060/dev/text/xml/ACL.6060.dev.en-xx.${lang}.xml `pwd -P`/2/acl_6060/dev/full_wavs .
done
```
## Czech-to-English IWSLT Dev Set

Download data from: https://drive.google.com/file/d/1-XicsrBQubkGK-kyBIxKO-7JAx94o_KV/view?usp=sharing

Run data preparation:
```
python prepare_cs_en_dev.py iwslt2024_cs_en_dev/iwslt2024_cs_devset.json cs_en

```
