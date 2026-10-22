# Wealth Exchange Models

Preliminary code and analysis from my summer research project in financial mathematics at University College Dublin, joint work with Dr. Andrea Monaco and Dr. Adamaria Perrotta.

The project asks which wealth exchange mechanisms take the stationary wealth distribution from the exponential (Boltzmann–Gibbs) form of kinetic exchange models to a Pareto tail. It led to the preprint:

> Monaco, A., Perrotta, A. & Moelders, N. (2026). *Scale Homogeneity and Pareto Tails in Wealth Accumulation*. [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7640561)

This repository contains the exploratory simulations that came before the paper. The numerical results in the paper were produced separately; that code is available on request (njmoelders@gmail.com).

## Notebooks

The notebooks are numbered in reading order. Notebooks 01 and 02 reproduce existing models from the literature; 03 to 06 are the mechanisms explored in this project.

| Notebook | Model |
| --- | --- |
| `baseline_models/01_DY.ipynb` | Drăgulescu & Yakovenko (2000) monetary exchange model, plus a yard-sale variant |
| `baseline_models/02_MGP.ipynb` | Multi-aggregate extension of the DY model (Monaco, Ghio & Perrotta, 2024) |
| `potentials/03_wealth_weighted_exchange.ipynb` | Counterparty chosen in proportion to its wealth |
| `potentials/04_dissimilarity_kernels.ipynb` | Interaction probability $P_{ab} \propto e^{-\Phi(a,b)}$ based on wealth dissimilarity (homophily) |
| `metropolis_hastings/05_log_potential.ipynb` | Metropolis–Hastings acceptance with $U(w) = \pm\log w$ |
| `metropolis_hastings/06_unified_log_potential.ipynb` | Unified potential $U(w) = A\log(1 + w/w_0)$: exponential bulk with a Pareto tail |

## Package

`wealth_dist/` holds the code shared by the notebooks:

- `potential.py`: interaction kernels and the pairing-based exchange simulation (`simulate`)
- `metropolis.py`: Metropolis–Hastings exchange simulation (`MH_simulate`)
- `plotting.py`: histograms, entropy, CCDFs and Pareto fit plots
- `stats_analysis.py`: Pareto tail fits with Kolmogorov–Smirnov tests

## Setup

Requires Python 3.11+.

```bash
pip install -r requirements.txt
pip install -e .
```

## References

- Drăgulescu, A. & Yakovenko, V. M. (2000). Statistical mechanics of money. *The European Physical Journal B*, 17(4), 723–729. https://doi.org/10.1007/s100510070114
- Monaco, A., Ghio, M. & Perrotta, A. (2024). Wealth dynamics in a multi-aggregate closed monetary system. *Physica A*, 646, 129851. https://doi.org/10.1016/j.physa.2024.129851
