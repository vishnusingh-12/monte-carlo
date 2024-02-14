import matplotlib.pyplot as plt
import numpy as np
from lattice_module import Lattice
import random
from msd_module import get_msd

mc_steps = 10000
moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # movement of ions up down left right
# (1,0)=down,(0,1)=right,(-1,0)=up,(0,-1)=left
lattice = Lattice(20, 0.3, 1)
lat_2d = lattice.get_lattice()
for i in range(mc_steps):
    ions = lattice.get_ions(lat_2d)
    np.random.shuffle(ions)
    # random_ion = random.randint(0, len(ions) - 1)
    # ions = ions[random_ion:] + ions[:random_ion]
    for ion in ions:
        # print('before lattice')
        # lattice.print_lattice(lat_2d, 'index')
        # print('selecting ion ', ion.index)
        # print('before pos ', ion.position)
        # print('before mapped pos ', ion.mapped_position)

        step = random.choice(moves)
        # print('move ', step)
        potential_pos = [(ion.mapped_position[0] + step[0]) % lattice.size,
                         (ion.mapped_position[1] + step[1]) % lattice.size]
        # print('potential position', potential_pos)
        if lat_2d[potential_pos[0], potential_pos[1]].value == 0:
            # print('move accepted')
            lat_2d[ion.mapped_position[0], ion.mapped_position[1]], lat_2d[potential_pos[0], potential_pos[1]] = \
                lat_2d[potential_pos[0], potential_pos[1]], lat_2d[ion.mapped_position[0], ion.mapped_position[1]]
            ion.position = [ion.position[0] + step[0], ion.position[1] + step[1]]
            ion.mapped_position = potential_pos
            ion.position_list.append(ion.position)
            # print('after pos ', ion.position)
            # print('after mapped pos ', ion.mapped_position)
            # print('after lattice')
            # lattice.print_lattice(lat_2d, 'index')
            # print(ion.position_list)
        else:
            # print('move rejected')
            ion.position_list.append(ion.position)
            # print('after pos ', ion.position)
            # print('after mapped pos ', ion.mapped_position)
            # print('after lattice')
            # lattice.print_lattice(lat_2d, 'index')
            # print(ion.position_list)
            continue
ionss = lattice.get_ions(lat_2d)
x = [i[1] for i in ionss[0].position_list]
y = [i[0] for i in ionss[0].position_list]
x1 = [i[1] for i in ionss[1].position_list]
y1 = [i[0] for i in ionss[1].position_list]
x2 = [i[1] for i in ionss[2].position_list]
y2 = [i[0] for i in ionss[2].position_list]
x3 = [i[1] for i in ionss[-1].position_list]
y3 = [i[0] for i in ionss[-1].position_list]
# x4= [i[1] for i in ions[5].position_list]
# y4 = [i[0] for i in ions[5].position_list]
plt.plot(x, y)
plt.plot(x1, y1)
plt.plot(x2, y2)
plt.plot(x3, y3)
# plt.plot(x4, y4)
plt.show()
# msd = get_msd(ions, mc_steps // 2)

# print(msd)

# print(msd_new == msd)
