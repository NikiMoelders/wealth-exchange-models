import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# ============================================================
#  Histogram + Entropy
# ============================================================

def make_hist(wealth, bins=None, title="Simulation", ax=None):
    if ax is None:
        ax = plt.gca()
        
    if bins is None:
        bins0 = max(1, int(len(wealth) / 100))
    else:
        bins0 = bins
    
    ax.hist(wealth, bins=bins0, density=True)
    ax.set_xlabel('Wealth')
    ax.set_ylabel('Probability Density')
    ax.set_title(title)

def plot_entropy(ent, ax=None):
    if ax is None:
        ax = plt.gca()
        
    n = len(ent) 
    ax.plot(np.arange(0, 100, 100/n), ent)
    ax.set_xlabel("Percentage of Simulations")
    ax.set_ylabel("Entropy")
    ax.set_title("Entropy Over Time")

def plot_simulation_results(vector, bins=None, title="Simulation", figsize=(12, 5), ax=None):
    """
    Plots the distribution of wealth and entropy over time of a simulation

    Parameters
    ----------
    vector: the output of the simulate function
    bins: number of bins in the histogram
    title: title of the simulation eg. kernel type
    figsize: figsize of the plots
    ax: optional pair of matplotlib axes, e.g. ax=[ax1, ax2]

    Returns
    ---------
    two plots, left side is wealth histogram and right is entropy over time
    """

    if ax is None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
        show = True
    else:
        ax1, ax2 = ax
        show = False

    wealth = vector[0]
    ent = vector[1]

    make_hist(wealth, bins=bins, title=title, ax=ax1)
    plot_entropy(ent, ax=ax2)

    if show:
        plt.tight_layout()
        plt.show()

def gibbs_plot(wealth, m=100, pct=None, bins=None, ax=None, DY=False):
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))
        show = True
    else:
        show = False

    title = "Entire Population"

    if pct is not None:
        wealth = wealth[wealth <= np.percentile(wealth, pct)]
        title = f"Bottom {pct}% of the Population"
    
    make_hist(wealth, bins=bins, title=title, ax=ax)

    if DY:
        xvals = np.linspace(0, wealth.max(), 500)
        ax.plot(xvals, np.exp(-xvals / m) / m, label="Theoretical Exponential (DY)") # PDF, matching the density histogram
        ax.legend()

    if show:
        plt.tight_layout()
        plt.show()

# ============================================================
#  CCDF + Regression (For Power Law Tails)
# ============================================================

def prepare_ccdf(wealth, pct = None):
    x = np.sort(wealth)
    N = len(wealth)
    ccdf = 1 - np.arange(0, N) / N #greater or equal
    if pct is not None:
        cutoff = np.percentile(wealth, pct)
    else:
        cutoff = 0 
    mask = (x >= cutoff) & (ccdf > 0)
    return x[mask], ccdf[mask]

def regression(x, ccdf, loglog = True):

    if loglog:
        x_reg = np.log(x)

    else:
        x_reg = x

    y_reg = np.log(ccdf)
    fit = linregress(x_reg, y_reg)

    m = fit.slope
    c = fit.intercept
    r2 = fit.rvalue**2

    y_fit = np.exp(m * x_reg + c)

    return x, y_fit, r2

def plot_ccdf(wealth, pct = None, reg = False, ylog = True, xlog = True, ax=None):

    """
    Plots the CCDF of Wealth on a log log or log scale

    Parameters
    ----------
    wealth: array of wealth values
    pct (None): the percentile for which the ccdf starts, eg. 95 means the top 5% are plotted
    reg (False): plots a linear regression fit to the data on the appropriate scale
    ylog (True): plot the y-axis on a log scale
    xlog (True): plot the x-axis on a log scale
    ax (None): used for further functions

    Returns
    ---------
    A plot of the CCDF of Wealth
    """

    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))
        show = True
    else:
        show = False

    x, ccdf = prepare_ccdf(wealth, pct = pct)

    ax.plot(x, ccdf, '.')
    ax.set_ylabel("CCDF")
    ax.set_xlabel("Wealth")

    if ylog:
        ax.set_yscale('log')

    if xlog:
        ax.set_xscale('log')

    if xlog and ylog:
        loglog = True
    else:
        loglog = False

    if reg:
        x, y_fit, r2 = regression(x, ccdf, loglog = loglog)
        ax.plot(x, y_fit, label = f"R²={r2:.3f}")
        ax.legend()
        display_pct = 0 if pct is None else pct
        ax.set_title(f"CCDF of the Top {100 - display_pct}%")
    else:
        if pct is not None:
            ax.set_title(f"CCDF of the Top {100 - pct}%")
        else:
            ax.set_title("CCDF of the Population")
            
    if show:
        plt.tight_layout()
        plt.show()


def plot_pareto_ccdf_grid(wealth, fitting, title=None):
    """
    Plots the CCDF of the whole population and of the top 10%, 5% and 1% on log-log axes,
    overlaying the fitted Pareto tails from pareto_tail_fits (default pcts=(90, 95, 97.5, 99)).

    Parameters
    ----------
    wealth: array of wealth values
    fitting: output of stats_analysis.pareto_tail_fits(wealth)
    title (None): optional figure title
    """

    fig, axs = plt.subplots(2, 2, figsize=(10, 8))

    plot_ccdf(wealth, pct=None, ax=axs[0, 0])

    for ax, fit in zip([axs[0, 1], axs[1, 0], axs[1, 1]], [fitting[0], fitting[1], fitting[3]]):
        plot_ccdf(wealth, pct=fit["pct"], ax=ax)
        xvals = np.linspace(fit["xmin"], wealth.max(), 200)
        tail_frac = fit["tail_pct"] / 100
        ax.plot(
            xvals,
            tail_frac * (xvals / fit["xmin"]) ** (-fit["alpha"]),
            label=f'KS: {fit["ks_stat"]:.2f} (p = {fit["p_value"]:.2f})',
        )
        ax.legend()

    if title is not None:
        fig.suptitle(title)

    plt.tight_layout()
    plt.show()
