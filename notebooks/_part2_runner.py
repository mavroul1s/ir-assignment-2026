"""Standalone runner for the Part 2 (Zipf) analysis.

Identical methodology to the notebook; isolated as a .py file for
quick smoke-testing during development.
"""
import re
import urllib.request
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / 'data'
FIG_DIR = ROOT / 'results' / 'figures'
TBL_DIR = ROOT / 'results' / 'tables'
for d in (DATA_DIR, FIG_DIR, TBL_DIR):
    d.mkdir(parents=True, exist_ok=True)

BOOK_PATH = DATA_DIR / 'pride_and_prejudice.txt'
BOOK_URL = 'https://www.gutenberg.org/ebooks/1342.txt.utf-8'

START_MARKER = '*** START OF THE PROJECT GUTENBERG EBOOK'
END_MARKER = '*** END OF THE PROJECT GUTENBERG EBOOK'
TOKEN_REGEX = re.compile(r"[a-z]+(?:'[a-z]+)?")


def load_text() -> str:
    if BOOK_PATH.exists():
        text = BOOK_PATH.read_text(encoding='utf-8')
        print(f'Cached: {len(text):,} chars')
        return text
    print(f'Downloading {BOOK_URL}...')
    req = urllib.request.Request(BOOK_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as r:
        text = r.read().decode('utf-8')
    BOOK_PATH.write_text(text, encoding='utf-8')
    print(f'Saved {len(text):,} chars to {BOOK_PATH}')
    return text


def strip_gutenberg(raw: str) -> str:
    s = raw.find(START_MARKER)
    e = raw.find(END_MARKER)
    if s == -1 or e == -1:
        return raw
    s = raw.find('\n', s) + 1
    return raw[s:e]


def tokenise(s: str) -> list[str]:
    s = s.replace('\u2019', "'").replace('\u2018', "'")
    return TOKEN_REGEX.findall(s.lower())


def main() -> None:
    text = load_text()
    body = strip_gutenberg(text)
    print(f'Body length: {len(body):,} chars')

    tokens = tokenise(body)
    vocab = set(tokens)
    print(f'Tokens: {len(tokens):,}   Vocabulary: {len(vocab):,}')

    freq = Counter(tokens)
    ranked = freq.most_common()
    df = pd.DataFrame(ranked, columns=['term', 'cf'])
    df['rank'] = np.arange(1, len(df) + 1)
    df['cf_times_rank'] = df['cf'] * df['rank']
    print('\nTop 20 terms:')
    print(df.head(20).to_string(index=False))

    ranks = df['rank'].to_numpy()
    cfs = df['cf'].to_numpy()

    c_a = float(cfs[0])
    c_b_mean = float(np.mean(cfs * ranks))
    c_b_median = float(np.median(cfs * ranks))
    TOP_N_FIT = min(1000, len(df))
    log_r = np.log(ranks[:TOP_N_FIT])
    log_cf = np.log(cfs[:TOP_N_FIT])
    slope, intercept = np.polyfit(log_r, log_cf, 1)
    c_c = float(np.exp(intercept))
    exponent = float(-slope)

    print('\nConstant estimators:')
    print(f'  (a) cf_1                 : {c_a:,.2f}')
    print(f'  (b) mean(cf_i * i)       : {c_b_mean:,.2f}')
    print(f'  (b) median(cf_i * i)     : {c_b_median:,.2f}')
    print(f'  (c) log-log fit (top {TOP_N_FIT}) : {c_c:,.2f}    exponent = {exponent:.3f}')

    # Figure 1: top-50 bars
    TOP = 50
    top_df = df.head(TOP)
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.bar(range(1, TOP + 1), top_df['cf'], color='#3a6ea5', edgecolor='black', linewidth=0.4)
    ax.set_xticks(range(1, TOP + 1))
    ax.set_xticklabels(top_df['term'], rotation=60, ha='right', fontsize=8)
    ax.set_xlabel('Term (rank order)', fontsize=11)
    ax.set_ylabel('Collection frequency', fontsize=11)
    ax.set_title(f'Top {TOP} most frequent terms in Pride and Prejudice', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    ax.set_axisbelow(True)
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'zipf_top50_bar.pdf', bbox_inches='tight')
    plt.savefig(FIG_DIR / 'zipf_top50_bar.png', dpi=160, bbox_inches='tight')
    plt.close()

    # Figure 2: log-log
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.loglog(ranks, cfs, 'o', markersize=2.5, alpha=0.5, color='#3a6ea5',
              label='Empirical (cf$_i$)')
    ax.loglog(ranks, c_c / ranks, '-', color='#c0392b', linewidth=1.5,
              label=f'Zipf fit: c/i,  c={c_c:,.0f}')
    ax.set_xlabel('Rank i (log scale)', fontsize=11)
    ax.set_ylabel('Collection frequency cf$_i$ (log scale)', fontsize=11)
    ax.set_title('Zipf plot — Pride and Prejudice', fontsize=12)
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, which='both', alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / 'zipf_loglog.pdf', bbox_inches='tight')
    plt.savefig(FIG_DIR / 'zipf_loglog.png', dpi=160, bbox_inches='tight')
    plt.close()

    df.head(50).to_csv(TBL_DIR / 'zipf_top50.csv', index=False)
    pd.DataFrame([
        {'estimator': '(a) cf_1', 'constant_c': c_a},
        {'estimator': '(b) mean(cf_i * i)', 'constant_c': c_b_mean},
        {'estimator': '(b) median(cf_i * i)', 'constant_c': c_b_median},
        {'estimator': f'(c) log-log fit (top {TOP_N_FIT})',
         'constant_c': c_c, 'exponent': exponent},
    ]).to_csv(TBL_DIR / 'zipf_constants.csv', index=False)

    print(f'\nFigures saved to {FIG_DIR}')
    print(f'Tables saved to {TBL_DIR}')


if __name__ == '__main__':
    main()
