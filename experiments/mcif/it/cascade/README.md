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

Pending, should be updated with these soon.
