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
| 0.1   | 24.25 | **25.55** | 25.53 | 25.05 | 25.01 | 24.39 |
| 0.3   | 22.02 | 22.05 | 22.58 | 23.24 | 22.76 | 22.32 |
| 0.5   | 19.34 | 20.17 | 21.65 | 21.86 | 22.46 | 22.76 |
| 0.7   | 19.14 | 20.16 | 19.73 | 20.21 | 20.36 | 20.98 |
| 0.9   | 18.55 | 18.43 | 18.94 | 19.00 | 19.40 | 19.57 |

The best results are obtained with pause=0.1 and VA threshold=0.2. We run the final runs using this setting:
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
| 18.31 | 1821       | 4747         |
| 19.27 | 2280       | 5340         |
| 21.56 | 2734       | 5301         |
| 22.52 | 3087       | 5743         |
| 21.80 | 3021       | 5691         |
| 22.96 | 3433       | 6352         |
| 22.45 | 3618       | 5718         |