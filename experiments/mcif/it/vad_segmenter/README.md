# SeamlessM4T with VAD Segmenter

## Run Experiments

Set environment variables:
```
export REPO_ROOT_PATH=
export PYTHON_ENV_DIR=
```

Following command runs an offline translation with different pause lengths (0.1-0.9s) and voice activity threshold (0.1-0.6):
```
bash tune.sh
```

We get following results:
| Pause \ VA Threshold | 0.1   | 0.2   | 0.3   | 0.4   | 0.5   | 0.6   |
|:---------------------:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| 0.1   | 33.05 | 32.07 | 31.46 | 31.27 | 31.41 | 30.36 |
| 0.3   | 33.95 | 34.78 | 34.93 | 35.16 | 35.32 | **35.63** |
| 0.5   | 30.67 | 32.90 | 34.28 | 35.02 | 35.27 | 35.14 |
| 0.7   | 26.49 | 29.39 | 30.31 | 31.17 | 31.69 | 31.68 |
| 0.9   | 24.29 | 25.81 | 27.45 | 27.92 | 28.52 | 29.18 |

The best results are obtained with pause=0.3 and VA threshold=0.6. We run the final runs using this setting:
```
bash final.sh
```

Run evaluation script:
```
bash eval.sh
```

## Final Results

| BLEU  | StreamLAAL | StreamLAAL_CA |
|:-----:|:----------:|:-------------:|
| 30.63 | 2069       | 3164         |
| 34.18 | 2467       | 3499         |
| 35.22 | 2959       | 3937         |
| 36.07 | 3362       | 4457         |
| 36.17 | 3447       | 4536         |
| 36.47 | 3833       | 4900         |
| 36.26 | 4130       | 5232         |