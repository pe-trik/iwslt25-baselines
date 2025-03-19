# SeamlessM4T with VAD Segmenter

## Run Experiments

Set enviroment variables:
```
export REPO_ROOT_PATH=
export PYTHON_ENV_DIR=
```

We follow the hyperparameters from En->De SeamlessM4T with VAD Segmenter system.

To run the translation, execute the following script:
```
bash final.sh
```

Afterwards, run the resegmentation:
```
REPO_ROOT_PATH=... bash eval.sh
```

## Final Results

|  BLEU  | StreamLAAL | StreamLAAL_CA |
|:------:|:----------:|:-------------:|
| 15.16  | 1777       | 3463          |
| 15.36  | 2647       | 4093          |
| 15.79  | 3041       | 4286          |
| 16.13  | 2713       | 3919          |
| 16.04  | 2963       | 4115          |
| 15.98  | 3316       | 4444          |
| 16.06  | 3339       | 4579          |
