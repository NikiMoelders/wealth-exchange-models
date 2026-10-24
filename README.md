# Wealth Exchange Models

Preliminary code and analysis from my summer research internship in financial mathematics at University College Dublin, which was joint work with Dr. Andrea Monaco and Dr. Adamaria Perrotta.

The project asks which wealth exchange mechanisms take the stationary wealth distribution from the exponential (Boltzmann–Gibbs) form of kinetic exchange models to a Pareto tail. It led to the preprint:

> Monaco, A., Perrotta, A. & Moelders, N. (2026). *Scale Homogeneity and Pareto Tails in Wealth Accumulation*. [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7640561)

> [!IMPORTANT]
> This repository contains **exploratory code developed during the summer**, before the paper. It is **not** the code used to generate the numerical results or figures in the preprint, and it will not reproduce them. The code behind the paper's results is available on request (nmoelders@ethz.ch).

Comments and suggestions are welcome.

## Notebooks

The notebooks are grouped by model family and numbered in reading order. Notebooks 01 and 02 reproduce existing models from the literature; 03 to 06 are the mechanisms explored in this project. I would recommend following this order.

```text
notebooks/
├── baseline_models/
│   ├── 01_DY.ipynb
│   └── 02_MGP.ipynb
├── potentials/
│   ├── 03_wealth_weighted_exchange.ipynb
│   └── 04_dissimilarity_kernels.ipynb
└── metropolis_hastings/
    ├── 05_log_potential.ipynb
    └── 06_unified_log_potential.ipynb
```

| Notebook | Model |
| --- | --- |
| `01_DY` | Drăgulescu & Yakovenko (2000) monetary exchange model, plus a yard-sale variant |
| `02_MGP` | Multi-aggregate extension of the DY model (Monaco, Ghio & Perrotta, 2024) |
| `03_wealth_weighted_exchange` | Counterparty chosen in proportion to its wealth |
| `04_dissimilarity_kernels` | Interaction probability $P_{ab} \propto e^{-\Phi(a,b)}$ based on wealth dissimilarity (homophily) |
| `05_log_potential` | Metropolis–Hastings acceptance with $U(w) = \pm\log w$ |
| `06_unified_log_potential` | Unified potential $U(w) = A\log(1 + w/w_0)$: exponential bulk with a Pareto tail |

## Package

`wealth_dist/` holds the code shared by the notebooks:

- `potential.py`: interaction kernels and the pairing-based exchange simulation (`simulate`)
- `metropolis.py`: Metropolis–Hastings exchange simulation (`MH_simulate`)
- `plotting.py`: histograms, entropy, CCDFs and Pareto fit plots
- `stats_analysis.py`: maximum-likelihood (Hill) Pareto tail fits with Kolmogorov–Smirnov tests

## Setup

Requires Python 3.11+. From the repository root, install the package and its dependencies (`numpy`, `scipy`, `matplotlib`, `jupyter`) so the notebooks can import `wealth_dist`:

```bash
pip install -e .
```

## References

- Drăgulescu, A. & Yakovenko, V. M. (2000). Statistical mechanics of money. *The European Physical Journal B*, 17(4), 723–729. https://doi.org/10.1007/s100510070114
- Monaco, A., Ghio, M. & Perrotta, A. (2024). Wealth dynamics in a multi-aggregate closed monetary system. *Physica A*, 646, 129851. https://doi.org/10.1016/j.physa.2024.129851
