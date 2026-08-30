# CoT baseline, first run

API failures during this run caused the decomposition step to fall back to the
unmodified question, making the configuration structurally identical to
`B7b_qsubq` — the type-aware two-hop pipeline with no decomposition. The scores
confirm this: 0.3563 against 0.3563 at the retrieval tier, and agreement to four
decimal places at the other two tiers.

The second run, in `../B8_cot_kg_v2*`, is the one reported in the paper. It is
the lower of the two values, but it is the only one that measures what the
baseline is intended to measure.
