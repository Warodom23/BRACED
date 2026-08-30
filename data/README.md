# Data

Neither dataset is redistributed here.

## Sources

- **PrimeKG** — https://doi.org/10.7910/DVN/IXA7BM
- **BioHopR** — see reference [2] of the manuscript

## Question split

BioHopR provides no official split. Ours was created by stratified sampling on
the first-hop relation type, with `test_size = 0.1` and `random_state = 42`,
from the 7,633 two-hop questions in the benchmark.

| Split | Questions |
|---|---|
| train | 6,669 |
| dev | 200 |
| test | 764 |

The split is representative of the full benchmark: total variation distance is
0.0007 on target type and 0.0015 on the bridge–target type pair, and a
chi-square goodness-of-fit test gives p = 1.00 for both.

Test-set composition by gold answer-set size: 275 questions with at most 5
answers, 192 with 6–15, 167 with 16–50, and 130 with more than 50.

## Graph preprocessing

PrimeKG's 129,375 node identifiers reduce to 128,549 canonical entities after
name normalisation. 824 duplicate-name groups covering 1,650 identifiers are
merged, with the canonical member chosen by degree; 805 of those groups span
more than one node type.
