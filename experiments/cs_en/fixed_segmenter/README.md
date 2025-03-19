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

|  BLEU  | StreamLAAL | StreamLAAL_CA |
|:------:|:----------:|:-------------:|
| 13.22  |    1751    |     3145      |
| 15.04  |    1866    |     3009      |
| 15.50  |    2292    |     3391      |
| 15.96  |    2742    |     3935      |
| 16.41  |    2740    |     3922      |
| 16.50  |    3189    |     4479      |
| 16.58  |    3408    |     4653      |