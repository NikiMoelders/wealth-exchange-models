import numpy as np

# ============================================================
#  Simulation
# ============================================================

def MH_simulate(N, m, sims, count = 0.01, beta = 1, U = None, updates = False, uniform = True):
    """
    Simulates a Yakovenko-style wealth exchange model with the option of applying a potential based Metropolis-Hastings algorithm.
    Parameters
    ----------
    N : Number of agents.
    m : Initial wealth per agent.
    sims : Number of simulation steps.
    count (default 0.01): Fraction of simulations between entropy measurements.
    beta (default 1) : parameter chosen for P_acc = min(1, e^(-beta dU))
    U (optional) : potential Function U(wealth). The default (None) sets dU = 0, so every affordable trade is accepted (the DY model)
    updates (False) : print updates every 10% of simulations
    uniform (True) : initial wealth identically m, else ~exp(1/m)

    Returns
    ---------
    wealth : Final wealth distribution.
    entropy : Entropy values recorded during the simulation.
    """

    M = N*m #Total Wealth

    ### -------------------- INITIAL DISTRIBUTION --------------------------------------------------------

    if uniform:
        wealth = np.ones(N) * m
    else:
        wealth = np.random.exponential(scale=m, size=N) #New addition, note scale = mean

    entropy = []
    prints = max(1, int(sims * count))
    update = max(1, sims // 10)
    width = m / 100 # entropy bin width, scales with initial wealth

    for sim in range(sims):

    ### -------------------- AGENT CHOICE --------------------------------------------------------

        i, j = np.random.randint(N, size=2)
        while i == j: # distinct agents, much faster than np.random.choice(..., replace=False)
            j = np.random.randint(N)
        dm = np.random.uniform(0, m) #consistent with mean initial wealth
        accept = False
        m_j_old = wealth[j]
    
    ### -------------------- NO DEBT --------------------------------------------------------

        if m_j_old >= dm:

    ### -------------------- METROPOLIS PROBABILITY + POTENTIAL --------------------------------------------------------

            m_i_old = wealth[i]
            m_i_new = m_i_old + dm 
            m_j_new = m_j_old - dm
            if U is None:
                dU = 0
            else: 
                dU = U(m_i_new) + U(m_j_new) - U(m_i_old) - U(m_j_old) 

        # Metropolis probability is acceptance = min(1, e^(-beta dU))

            if dU <= 0:
                accept = True

            else:
                accept = np.log(np.random.rand()) < - beta * dU #easier computation

    ### -------------------- WEALTH EXCHANGE --------------------------------------------------------

        if accept:
            wealth[i] = m_i_new 
            wealth[j] = m_j_new

    ### -------------------- ENTROPY --------------------------------------------------------

        if sim % prints == 0:
            w_max = wealth.max()
            bin_edges = np.arange(0, w_max + width, width) # bins of width m/100
            vec, _ = np.histogram(wealth, bins = bin_edges)
            vec = vec[vec != 0] #problems with log 0 and less computation
            Pb = vec/N
            entropy.append(-np.sum(Pb*np.log(Pb)))

    ### -------------------- UPDATES --------------------------------------------------------

        if updates:
            if sim % update == 0:
                current = entropy[-1] if entropy else np.nan
                print(f"{(sim/ sims) *100}% completed, max wealth:{100*(wealth.max() / M):.3f}%, entropy:{current:.3f}")

    return wealth, entropy
