import numpy as np
from scipy import stats


def pareto_tail_fit(wealth, pct):
    """
    Fits a Pareto distribution to the upper tail of a wealth distribution by maximum likelihood.

    With the location fixed at 0, the maximum-likelihood scale is the smallest tail value (xmin),
    and the shape estimate is the Hill estimator, alpha = n / sum(log(w / xmin)). This is preferred
    to a least-squares line on the log-log CCDF, which gives biased exponents.

    Parameters
    ----------
    wealth: array-like
        Wealth values.
    pct: float
        Percentile threshold for the tail. For example, pct=95 fits the top 5%.

    Returns
    ---------
    dict
        Pareto fit statistics for the selected tail.
    """

    xmin = np.percentile(wealth, pct)
    tail = wealth[wealth >= xmin]

    shape, loc, scale = stats.pareto.fit(tail, floc=0)
    ks_stat, p_value = stats.kstest(
        tail,
        "pareto",
        args=(shape, loc, scale)
    )

    return {
        "pct": pct,
        "tail_pct": 100 - pct,
        "xmin": xmin,
        "n_tail": len(tail),
        "alpha": shape,
        "loc": loc,
        "scale": scale,
        "ks_stat": ks_stat,
        "p_value": p_value,
    }

def pareto_tail_fits(wealth, pcts=(90, 95, 97.5, 99), prints=True):
    """
    Fits Pareto distributions to multiple upper-tail thresholds.
    """

    fitting = []

    for pct in pcts:
        result = pareto_tail_fit(wealth, pct)
        fitting.append(result)

        if prints:
            print(f"\nTop {result['tail_pct']}% tail")
            print(f"xmin = {result['xmin']}")
            print(f"n_tail = {result['n_tail']}")
            print(f"alpha = {result['alpha']}")
            print(f"KS = {result['ks_stat']}")
            print(f"p-value = {result['p_value']}")

    return fitting