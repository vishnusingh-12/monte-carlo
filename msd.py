import numpy as np


def get_msd(ions, steps):
    ions_positions = np.array([ion.position_list for ion in ions])
    msd = []

    for i in range(steps):
        displacements = ions_positions[:, i:i + steps] - ions_positions[:, :steps]
        dr2 = np.sum(displacements ** 2, axis=(1, 2))
        displacement_sum = np.sum(dr2)
        msd.append(displacement_sum / (steps * len(ions)))

    return msd
