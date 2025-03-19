# SeamlessM4T with Fixed Segmenter

## Run Experiments

Set enviroment variables:
```
export REPO_ROOT_PATH=
export PYTHON_ENV_DIR=
```

We follow the hyperparameters from En->De SeamlessM4T with Fixed Segmenter system.

To run the translation, execute the following script:
```
bash final.sh
```

Afterwards, run the resegmentation:
```
REPO_ROOT_PATH=... bash eval.sh
```

## Final Results

| BLEU  | StreamLAAL | StreamLAAL_CA |
|:-----:|:----------:|:-------------:|
| 13.22 | 1665       | 3096          |
| 15.04 | 1766       | 2935          |
| 15.50 | 2260       | 3366          |
| 15.96 | 2725       | 3923          |
| 16.41 | 2674       | 3886          |
| 16.50 | 3172       | 4471          |
| 16.58 | 3390       | 4647          |