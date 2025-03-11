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

| BLEU    | LAAL    | LAAL_CA |
|---------|---------|---------|
| 16.42   | 908     | 2622    |
| 17.27   | 1527    | 3036    |
| 18.94   | 2637    | 4159    |
| 18.99   | 2432    | 4036    |
| 19.11   | 2516    | 4294    |
| 19.47   | 2712    | 4753    |
| 19.62   | 3627    | 5568    |