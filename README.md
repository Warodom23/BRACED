# BRACED
Bridge-aware reinforced query decomposition for multi-hop biomedical question answering over PrimeKG

Code and results for the paper published in *Machine Learning and Knowledge Extraction*.

## What this is

A planner is trained with GRPO to decompose a two-hop biomedical question into sub-queries. A deterministic typed traversal over PrimeKG converts those sub-queries into an entity set, and that set is the answer — no generative step follows the traversal.

## Requirements

```bash
pip install -r requirements.txt
```

Tested on Python 3.10, PyTorch 2.x, one 48 GB GPU.

## Data

Neither dataset is redistributed here.

- **PrimeKG** — https://doi.org/10.7910/DVN/IXA7BM
- **BioHopR** — see the paper's reference [2]

`data/split_*.txt` contain question indices only. Run
`scripts/prepare_primekg.py` to build the normalised graph.

## Reproducing the main result

```bash
python scripts/train.py --backbone Qwen/Qwen2.5-7B-Instruct
python scripts/evaluate.py --checkpoint outputs/best --k 25
```

Expected: micro-F1 0.3783, macro-F1 0.6197 on the 764-question test split
under unordered truncation.

## Trained adapters

QLoRA adapters for all five backbones are on HuggingFace:
[LINK]

## Results in the paper

| Paper | File |
|---|---|
| Table 3 | `results/main_results.json` |
| Table 4 | `results/per_question/` |
| Figure 4 | `results/topk_sweep.csv` |
| Table 9 | `results/backbone_swap.json` |

## A note on reproducibility

Each configuration was trained once. Training terminates at whichever of two budgets is reached first — 1,500 optimiser updates or 8,000 sampled questions — so the number of updates a backbone receives depends on how often its rollouts differ in reward.

## Citation

```bibtex
@article{phungjununt2026braced,
  title   = {Bridge-Aware Reinforced Compositional Exploration and
             Decomposition for Biomedical Multi-Hop Answering},
  author  = {Phungjununt, Warodom and Srisomboon, Kanabadee and
             Lee, Wilaiporn and Prayote, Akara and Pipanmekaporn, Luepol},
  journal = {Machine Learning and Knowledge Extraction},
  year    = {2026}
}
```

## License

Apache-2.0. Qwen2.5 and Qwen3 are Apache-2.0; Llama-3.1 is under the Llama 3.1 Community License.
