# Cascade with Whisper ASR and M2M100 MT

## Run Experiments

Set environment variables:
```
export REPO_ROOT_PATH=
export PYTHON_ENV_DIR=
```

First, we tune the segment length for Whisper ASR (with ASR step_length=0.5s and translation_la_policy=1 fixed):

| Segment Length |  BLEU  | StreamLAAL | StreamLAAL_CA |
|:--------------:|:------:|:----------:|:-------------:|
|       8      | 21.45  |   3169   |    4274     |
|      12      | 32.62  |   3582   |    4759     |
|      16      | 33.75  |   3654   |    5032     |
|      20      | 36.22  |   3462   |    4860     |
|      24      | 36.76  |   3266   |    4913     |
|      28      | **36.98**  |   3057   |    4698     |
|      30      | 36.13  |   3160   |    4968     |

The best result is when using the context of 28 seconds.

Whisper ASR also supports prompting. Prompting allows us to use previous context to lower the WER. We tune the context length (in words) for segment length 28:

| ASR Context |  BLEU  | StreamLAAL | StreamLAAL_CA |
|:-----------:|:------:|:----------:|:-------------:|
|      0      | **36.80**  |   3085   |    4612    |
|      5      | 36.55  |   3052   |    4696    |
|     10      | 36.37  |   3115   |    4788    |
|     15      | 36.19  |   3259   |    4985    |
|     20      | 36.06  |   3118   |    4724    |
|     25      | 36.56  |   3185   |    4900    |
|     30      | 36.21  |   3076   |    4625    |

Following the previous tuning, we also sweep the minimum segment length (in number of words) for the MT model:

| Number of words |  BLEU  | StreamLAAL | StreamLAAL_CA |
|:---------------:|:------:|:----------:|:-------------:|
|       0         | 36.80  |   3085    |    4612    |
|       5         | **36.96**  |   3068    |    4615    |
|      10         | 36.62  |   3121    |    4707    |
|      15         | 36.36  |   3196    |    4778    |
|      20         | 36.15  |   3399    |    5072    |
|      25         | 35.06  |   3612    |    5312    |
|      30         | 33.70  |   3860    |    5610    |


## Final Results

## Cascade Workflow Diagram

![Final Results](./final/tradeoff.png)

| ASR Step Length (seconds) | MT LA-2 Step (words) |  BLEU | StreamLAAL | StreamLAAL_CA | LongYAAL |
|:-------------------------:|:--------------------:|:-----:|:----------:|:-------------:|:--------:|
| 0.1                       | 1                    | 34.39 | 2367       | 4508          | 2449 | 
| 0.1                       | 2                    | 37.43 | 3108       | 6376          |  3202 |
| 0.1                       | 3                    | 38.05 | 3895       | 8241          | 3866 |
| 0.1                       | 4                    | 38.23 | 4437       | 10402         | 4273 |
| 0.2                       | 1                    | 34.39 | 2367       | 4480          | 2449 |
| 0.2                       | 2                    | 37.39 | 3145       | 6504          | 3239 |
| 0.2                       | 3                    | 38.05 | 3895       | 8258          | 3866 |
| 0.2                       | 4                    | 38.34 | 4437       | 10423         | 4273 |
| 0.3                       | 1                    | 36.96 | 3068       | 4584          | 3095 |
| 0.3                       | 2                    | **38.85** | 3786       | 5766          | 3737 |
| 0.3                       | 3                    | 39.36 | 4463       | 6956          | 4349 |
| 0.3                       | 4                    | 39.63 | 5096       | 8497          | 4741 |
| 0.4                       | 1                    | 36.71 | 3079       | 4564          | 3129 |
| 0.4                       | 2                    | 38.85 | 3785       | 5744          | 3736 |
| 0.4                       | 3                    | 39.50 | 4438       | 6936          | 4301 |
| 0.4                       | 4                    | 39.63 | 5096       | 8489          | 4741 |
| 0.5                       | 1                    | 36.96 | 3068       | 4543          | 3095 |
| 0.5                       | 2                    | 38.85 | 3787       | 5710          | 3737 |
| 0.5                       | 3                    | 39.29 | 4466       | 6938          | 4312 | 
| 0.5                       | 4                    | 39.63 | 5096       | 8488          | 4741 |
| 0.6                       | 1                    | 37.70 | 3837       | 5224          | 3791 |
| 0.6                       | 2                    | 39.03 | 4388       | 5986          | 4261 |
| 0.6                       | 3                    | 39.73 | 5030       | 6965          | 4763 |
| 0.6                       | 4                    | 39.61 | 5574       | 8118          | 5136 |
| 0.7                       | 1                    | 37.70 | 3837       | 5212          | 3791 |
| 0.7                       | 2                    | 39.03 | 4388       | 6016          | 4261 |
| 0.7                       | 3                    | 39.73 | 5030       | 6970          | 4763 |
| 0.7                       | 4                    | 39.61 | 5574       | 8124          | 5136 |
| 0.8                       | 1                    | 38.63 | 4936       | 6258          | 4692 |
| 0.8                       | 2                    | 39.20 | 5267       | 6657          | 5014 |
| 0.8                       | 3                    | 39.56 | 5722       | 7284          | 5371 |
| 0.8                       | 4                    | 39.76 | 6360       | 8491          | 5732 |


## SimulStream Usage Script

In addition to the results seen here, we also provide an example of a script that can be run with SimulStream in this directory. It should be a drop-in replacement for the `run_simuleval.sh` script and may be used instead.
