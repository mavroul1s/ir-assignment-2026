# Information Retrieval Assignment — ECE328, University of Thessaly

**Author:** Nikos Mavros (AEM 03741)
**Course:** ECE328 — Information Retrieval (Spring 2026)
**Submission:** single PDF report, generated from `report/main.tex`.

This repository contains the code, results, and report for the ECE328
Information Retrieval coursework.

## Layout

```
ir-assignment-2026/
├── notebooks/                     # Jupyter notebooks, one per part
│   ├── 01_part1_pagerank_hits.ipynb   (Part 1: PageRank, HITS, eigenvalues)
│   ├── 02_part2_zipf.ipynb            (Part 2: Zipf's law)
│   └── 03_part3_bpr.ipynb             (Part 3: BPR recommendation)
├── data/                          # Datasets (gitignored)
├── results/
│   ├── figures/                   # PDF/PNG figures used in the report
│   └── tables/                    # CSV tables of numerical results
├── report/                        # LaTeX sources for the final paper
│   ├── main.tex
│   └── refs.bib
├── requirements.txt
└── README.md (this file)
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook
```

Then open the notebook for the part you want to run.

## Datasets

The notebooks download their inputs on first run.

- **Part 2:** *Pride and Prejudice* from Project Gutenberg (eBook #1342, Plain Text UTF-8).
- **Part 3:** Last.FM dataset (HetRec 2011, GroupLens) and MovieLens 1M (GroupLens). Place the unpacked folders at `data/lastfm/` and `data/ml-1m/` respectively, or let the notebook prompt you.

## Reproducibility

- All Part-3 experiments are repeated 10 times with mean ± standard deviation reported, per the assignment specification.
- Random seeds are set inside each notebook so re-runs produce identical figures.
- The `results/` folder is committed so the report can be re-built without re-running anything.

## Building the report

```bash
cd report/
latexmk -pdf main.tex
```

This produces `main.pdf`, the file submitted to `draf@uth.gr`.
