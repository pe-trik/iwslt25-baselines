# SeamlessM4T with Fixed Segmenter

## Run Experiments

Set enviroment variables:
```
export REPO_ROOT_PATH=
export PYTHON_ENV_DIR=
```

Following command runs an offline translation with different segment sizes (2-20 seconds).
```
bash tune.sh
```

We get following results:

| Length | BLEU   |
|--------|--------|
| 2.0    | 9.844  |
| 4.0    | 19.679 |
| 6.0    | 22.087 |
| **8.0**    | **22.761** |
| 10.0   | 21.873 |
| 12.0   | 20.412 |
| 14.0   | 18.835 |
| 16.0   | 15.813 |
| 18.0   | 15.784 |
| 20.0   | 12.994 |

Run the final runs in simultaneous mode with segment length of 8 seconds:
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
| 16.42 | 1870       | 3478          |
| 17.27 | 2284       | 3685          |
| 18.94 | 2777       | 4247          |
| 18.99 | 2988       | 4495          |
| 19.11 | 3246       | 4885          |
| 19.47 | 3421       | 5311          |
| 19.62 | 3666       | 5566          |