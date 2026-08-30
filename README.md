# BRACED

Bridge-Aware Reinforced Compositional Exploration and Decomposition for
Biomedical Multi-Hop Answering.

Code and results supporting a manuscript under review at *Machine Learning
and Knowledge Extraction*.

## What this is

A planner is trained with Group Relative Policy Optimization to decompose a
two-hop biomedical question into sub-queries. A deterministic typed traversal
over PrimeKG converts those sub-queries into an entity set, and that set is the
answer — no generative step follows the traversal.

On the BioHopR test split of 764 questions this reaches micro-F1 0.3783 and
macro-F1 0.6197 at K = 25 under unordered truncation.

## Layout

| Path | Contents |
|---|---|
| `src/training.ipynb` | GRPO training and the retrieval operator |
| `src/baselines.ipynb` | the five compared systems |
| `src/evaluate.py` | entity-set F1 and per-question records |
| `src/bridge_hit.py` | bridge-hit rate |
| `src/verify.py` | consistency checks across runs |
| `results/main_results/` | every system at three evaluation tiers |
| `results/per_question/` | per-question F1, precision and recall |
| `results/ablations/` | bridge reward ablation |
| `results/predictions/` | predicted and gold answer sets, all 764 questions |
| `results/training/` | training history and checkpoint selection |
| `data/README.md` | how the split was constructed |

See `results/README.md` for the tier system and the mapping from file prefixes
to the systems named in the paper.

## Reproducing the reported figure

`results/main_results/B11_rldqd_retrieval.json` holds micro-F1 0.3783 and
macro-F1 0.6197 — the values reported in Table 3. `src/evaluate.py` recomputes
them from a trained checkpoint.

## Status

Backbone substitution results, the Top-K sweep and trained adapter weights are
being prepared and will be added.

## Data

Neither dataset is redistributed here. See `data/README.md`.

## Citation

```bibtex
@article{phungjununt2026braced,
  title   = {Bridge-Aware Reinforced Compositional Exploration and
             Decomposition for Biomedical Multi-Hop Answering},
  author  = {Phungjununt, Warodom and Srisomboon, Kanabadee and
             Lee, Wilaiporn and Prayote, Akara and Pipanmekaporn, Luepol},
  journal = {Machine Learning and Knowledge Extraction},
  year    = {2026},
  note    = {Under review}
}
```

## License

Apache-2.0. Qwen2.5 and Qwen3 are Apache-2.0; Llama-3.1 is under the
Llama 3.1 Community License.
