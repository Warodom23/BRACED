# Results

## Evaluation tiers

Each system is scored at three points in the pipeline:

| Suffix | Tier | Meaning |
|---|---|---|
| `_retrieval` | retrieval | the retrieved entity set, taken directly |
| *(none)* | grounded | LLM output filtered against the retrieved set |
| `_raw` | raw | LLM output, unfiltered |

**Table 3 of the paper reports the retrieval tier.** The paired statistical tests
are computed on the grounded tier, where per-question records are available for
every system; the ranking of systems is identical under both.

## System identifiers

| Prefix | System in the paper | Retrieval-tier micro-F1 |
|---|---|---|
| `B7_true_naive` | Single-hop KG retrieval | 0.0050 |
| `B9_react_kg` | ReAct + KG | 0.1588 |
| `B10_sft_only` | SFT-only | 0.3432 |
| `B8_cot_kg_v2` | CoT + KG | 0.3515 |
| `B7b_qsubq` | Type-aware two-hop, no planner | 0.3563 |
| `B11_rldqd` | **BRACED** | **0.3783** |

## per_question/

Each file holds 764 records with `f1`, `p`, `r`, `n_pred` and `n_gold`, in the
order of the test split. These are the records the paired bootstrap and the
Wilcoxon signed-rank test in Section 5.2 are computed from.

## ablations/

`bridgehit_full` uses w_b = 0.4 and w_t = 0.6; `bridgehit_nobridge` sets w_b = 0
and w_t = 1.0, with the planner retrained under each setting. Both are scored
with the same entity-matching implementation, which accounts for the small offset
from Table 3.

## predictions/

`final_preds.json` holds the question, the predicted entity set and the gold
entity set for all 764 test questions.

## training/

`history.json` records the selected checkpoint. Training terminated at update
1,440 after consuming the 8,000-question sampling budget; the checkpoint at
update 1,300 was selected on development macro-F1.
