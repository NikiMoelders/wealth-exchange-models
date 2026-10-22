import numpy as np
from numpy import random

# ============================================================
#  Kernels
# ============================================================

def square_kernel(ma, mb, sigma=100): #sigma protects prob 0 for small ma/large mb
    return ((ma - mb) / (sigma)) ** 2

def abs_kernel(ma, mb):
    return np.abs(ma - mb)

def log_kernel(ma, mb, eps=1e-12): #protect log0
    return -np.log((ma + eps) * (mb + eps))


# ============================================================
#  Probability Function
# ============================================================

def make_prob(kernel):
    """
    Creates a probability distribution function given an interaction kernel

    Parameters
    ----------
    kernel(m_a, m_b): a function which measures economic distance or dissimilarity

    Returns
    ---------
    prob(wealth, i): a function, which given an array of wealth values and an agent i,
                    outputs a probability distribution for the choice of j given the kernel chosen above
    """

    def prob(wealth, i):
        m_a = wealth[i]
        P_ab = np.exp(-kernel(m_a, wealth))
        P_ab[i] = 0 
        total = P_ab.sum()
        if total == 0:
            raise ValueError("Kernel produced zero total probability")
        return P_ab / total
    return prob

# ============================================================
#  Simulation
# ============================================================

def simulate(N, m, sims, count = 0.01, prob=None, updates = False):
    """
    Simulates a Yakovenko-style wealth exchange model with the option to add in a probability

    Parameters
    ----------
    N : Number of agents.
    m : Initial wealth per agent.
    sims : Number of simulation steps.
    count (default 0.01): Fraction of simulations between entropy measurements.
    prob (optional): Function prob(wealth, i) returning a probability vector for choosing agent j.
                    This has strict requirements, the output must be a valid probability distribution
                    i.e. sums to 1 and probability of choosing i must be zero.
                    The default is a uniform distribution, as outlined in the original Drăgulescu & Yakovenko (2000) paper.
    updates (False) : print updates every 10% of simulations
    Returns
    ---------
    wealth : Final wealth distribution.
    entropy : Entropy values recorded during the simulation.
    """

    M = N*m #Total Wealth
    wealth = np.ones(N) * m
    entropy = []
    index = np.arange(N)
    prints = max(1, int(sims * count))
    update = max(1, sims // 10)
    width = m / 100 # entropy bin width, scales with initial wealth

    for sim in range(sims):

    ### -------------------- AGENT CHOICE --------------------------------------------------------
        if prob is None:
            i, j = np.random.randint(N, size=2)
            while i == j: # distinct agents
                j = np.random.randint(N)

        else: 
            i = np.random.choice(N)
            p = prob(wealth, i)
            if p[i] != 0:
                raise ValueError("Probability 0 is not assigned to i")
            if not np.isclose(p.sum(), 1):
                raise ValueError("Probabilities do not sum to 1")
            if np.any(p < 0):
                raise ValueError("Probabilities must be non-negative")
            j = np.random.choice(index, p = p)

    ### -------------------- WINNER CHOICE --------------------------------------------------------

        loser = np.random.choice([i,j])  #"Coin Flip"
        winner = j if loser == i else i
        dm = np.random.uniform(0, m) 

    ### -------------------- WEALTH EXCHANGE --------------------------------------------------------

        if wealth[loser] >= dm:
            wealth[loser] -= dm
            wealth[winner] += dm

    ### -------------------- ENTROPY --------------------------------------------------------

        if sim % prints == 0:
            w_max = wealth.max()
            bin_edges = np.arange(0, w_max + width, width) # bins of width m/100
            vec, _ = np.histogram(wealth, bins = bin_edges)
            vec = vec[vec != 0] #problems with log 0 and less computation
            Pb = vec/N
            entropy.append(-np.sum(Pb*np.log(Pb)))

        if updates and sim % update == 0:
            current = entropy[-1] if entropy else np.nan
            print(f"{(sim/ sims) *100}% completed, max wealth:{100*(wealth.max() / M):.3f}%, entropy:{current:.3f}")

    return wealth, entropy
