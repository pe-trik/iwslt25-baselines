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
| 2.0    | 13.315  |
| 4.0    | 25.141 |
| 6.0    | 26.363 |
| **8.0**    | **28.245** |
| 10.0   | 27.552 |
| 12.0   | 26.187 |
| 14.0   | 22.586 |
| 16.0   | 20.596 |
| 18.0   | 19.042 |
| 20.0   | 16.085 |

Run the final runs in simultaneous mode with segment length of 8 seconds:
```
bash final.sh
```

Run evaluation scripts:
```
bash eval.sh
bash omnisteval.sh
```

## Final Results

| BLEU  | StreamLAAL | StreamLAAL_CA | LongYAAL |
|:-----:|:----------:|:-------------:|:--------:|
| 24.29 | 2078       | 3442          | 2046     |
| 27.00 | 2474       | 3563          | 2568     |
| 26.97 | 2889       | 3912          | 3006     |
| 27.30 | 3236       | 4343          | 3407     |
| 27.54 | 3508       | 4664          | 3670     |
| 27.78 | 3741       | 4846          | 3840     |
| 29.12 | 3912       | 5034          | 4065     |


## SimulStream Usage Script

In addition to the results seen here, we also provide an example of a script that can be run with SimulStream in this directory. It should be a drop-in replacement for the `run_simuleval.sh` script and may be used instead.
