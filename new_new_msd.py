import numpy as np


def get_msd(ions, steps):
    num_ions = len(ions)
    positions = np.array([ion.position_list for ion in ions])

    msd = np.zeros(steps)
    for k in range(steps):
        dx = positions[:, k:, 0] - positions[:, :steps - k, 0]
        dy = positions[:, k:, 1] - positions[:, :steps - k, 1]
        squared_displacements = dx ** 2 + dy ** 2
        msd[k] = np.mean(squared_displacements)

    msd /= (steps * num_ions)
    return msd
