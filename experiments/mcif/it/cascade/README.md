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
|      20      | -  |   -   |    -     |
|      24      | 36.76  |   3266   |    4913     |
|      28      | 36.93  |   3063   |    4721     |
|      30      | 36.13  |   3160   |    4968     |

The best result is when using the context of 28 seconds.

Whisper ASR also supports prompting. Prompting allows us to use previous context to lower the WER. We tune the context length (in words):

| ASR Context |  BLEU  | StreamLAAL | StreamLAAL_CA |
|:-----------:|:------:|:----------:|:-------------:|
|      0      | 20.65  |   10332   |    19975    |
|      5      | 20.41  |   10791   |    20396    |
|     10      | 20.35  |   10696   |    20412    |
|     15      | 20.62  |   10628   |    18572    |
|     20      | 20.67  |   10450   |    21724    |
|     25      | 20.68  |   10425   |    19801    |
|     30      | 20.72  |   10393   |    19808    |

Following the previous tuning, we also sweep the minimum segment length (in number of words) for the MT model:

| Number of words |  BLEU  | StreamLAAL | StreamLAAL_CA |
|:---------------:|:------:|:----------:|:-------------:|
|       0         | -----  |   -----    |    -----    |
|       5         | -----  |   -----    |    -----    |
|      10         | -----  |   -----    |    -----    |
|      15         | -----  |   -----    |    -----    |
|      20         | -----  |   -----    |    -----    |
|      25         | -----  |   -----    |    -----    |
|      30         | -----  |   -----    |    -----    |

## Final Results

## Cascade Workflow Diagram

![Final Results](./final/tradeoff.png)

| ASR Step Length (seconds) | MT LA-2 Step (words) |  BLEU | StreamLAAL | StreamLAAL_CA |
|:-------------------------:|:--------------------:|:-----:|:----------:|:-------------:|
| 0.1                       | 1                    | 18.07 | 4822       | 12610         |
| 0.1                       | 2                    | 19.47 | 4958       | 16403         |
| 0.1                       | 3                    | 19.69 | 5291       | 18823         |
| 0.1                       | 4                    | 20.82 | 6897       | 25403         |
| 0.2                       | 1                    | 21.75 | 3229       | 7348          |
| 0.2                       | 2                    | 23.50 | 3810       | 18717         |
| 0.2                       | 3                    | 24.18 | 4606       | 11152         |
| 0.2                       | 4                    | 24.10 | 5428       | 14534         |
| 0.3                       | 1                    | 23.94 | 2948       | 5584          |
| 0.3                       | 2                    | 25.19 | 3762       | 7648          |
| 0.3                       | 3                    | 26.17 | 4332       | 8739          |
| 0.3                       | 4                    | 26.24 | 4931       | 9977          |
| 0.4                       | 1                    | 24.70 | 3204       | 4896          |
| 0.4                       | 2                    | 25.69 | 3892       | 6105          |
| 0.4                       | 4                    | 26.32 | 5080       | 9769          |
| 0.5                       | 1                    | 25.88 | 3140       | 5722          |
| 0.5                       | 2                    | 26.48 | 3773       | 6162          |
| 0.5                       | 3                    | 26.67 | 4392       | 7758          |
| 0.5                       | 4                    | 27.04 | 4989       | 8987          |
| 0.6                       | 1                    | 25.47 | 3637       | 5110          |
| 0.6                       | 2                    | 26.34 | 4112       | 5922          |
| 0.6                       | 3                    | 26.97 | 4852       | 7667          |
| 0.6                       | 4                    | 26.89 | 5445       | 8779          |
| 0.7                       | 1                    | 25.83 | 3777       | 5749          |
| 0.7                       | 2                    | 26.29 | 4281       | 6354          |
| 0.7                       | 3                    | 27.09 | 4839       | 7359          |
| 0.7                       | 4                    | 27.15 | 5540       | 8534          |
| 0.8                       | 1                    | 26.64 | 4119       | 6063          |
| 0.8                       | 2                    | 26.77 | 4596       | 7204          |
| 0.8                       | 4                    | 26.94 | 5780       | 8422          |