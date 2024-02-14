import matplotlib.pyplot as plt
import numpy as np
from lattice_module import Lattice
import random
from msd_module import get_msd

mc_steps = 100000
moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # movement of ions up down left right
# (1,0)=down,(0,1)=right,(-1,0)=up,(0,-1)=left
for s in [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]:
    lattice = Lattice(20, s, 1)
    lat_2d = lattice.get_lattice()
    for i in range(mc_steps):
        ions = lattice.get_ions(lat_2d)
        np.random.shuffle(ions)

        for ion in ions:

            step = random.choice(moves)

            potential_pos = [(ion.mapped_position[0] + step[0]) % lattice.size,
                             (ion.mapped_position[1] + step[1]) % lattice.size]

            if lat_2d[potential_pos[0], potential_pos[1]].value == 0:

                lat_2d[ion.mapped_position[0], ion.mapped_position[1]], lat_2d[potential_pos[0], potential_pos[1]] = \
                    lat_2d[potential_pos[0], potential_pos[1]], lat_2d[ion.mapped_position[0], ion.mapped_position[1]]
                ion.position = [ion.position[0] + step[0], ion.position[1] + step[1]]
                ion.mapped_position = potential_pos
                if (i + 1) % 100 == 0:
                    ion.position_list.append(ion.position)

            else:
                if (i + 1) % 100 == 0:
                    ion.position_list.append(ion.position)

                continue
    ions = lattice.get_ions(lat_2d)

    msd = get_msd(ions, 500)

    np.save(f'vacancy_{s * 100}.npy', msd)
    print(s)
