import numpy as np
from scipy.stats import linregress


def get_msd(ions, steps):
    """
    Returns msd at different Monte Carlo steps
    :param ions: list of ions. Each element of the list is an ion
    :param steps: half of the number of positions captured for each ion
    :return: list of msd for different steps
    """

    # making an array of all the ion position list. The ion position list is already a list of lists.
    # so this becomes a 3d numpy array
    ions_positions = np.array([ion.position_list for ion in ions], dtype=np.float64)
    msd = []
    # msd calculation algorithm
    for i in range(steps):
        displacements = ions_positions[:, i:i + steps] - ions_positions[:, :steps]
        dr2 = np.sum(displacements ** 2, axis=(1, 2), dtype=np.float64)
        displacement_sum = np.sum(dr2, dtype=np.float64)
        msd.append(displacement_sum / (steps * len(ions)))

    # returning msd
    return msd


def get_msd_old(ions, steps):
    """
        Old and non pythonic way of msd calculation (kept just for reference)
    :param ions: ions list
    :param steps: half of the number of positions captured for each ion
    :return: list of msd for different steps

    """
    msd = []
    for i in range(steps):
        sm = 0
        for j in ions:
            for k in range(steps):
                dx = j.position_list[i + k][0] - j.position_list[k][0]
                dy = j.position_list[i + k][1] - j.position_list[k][1]
                dr2 = dx ** 2 + dy ** 2
                sm = sm + dr2
        msd.append(sm / (steps * len(ions)))
    return msd


def get_diffusivity(x, msd):
    diffusivity = linregress(x, msd).slope / 4
    return diffusivity
