import numpy as np
import random
from lattice_module import Lattice
from plots_module import plot_energy_heatmap
from plots_module import plot_msd, plot_diffusivity
from msd_module import get_diffusivity

# lattice = Lattice(40, 0.5, 2)
# plot_energy_heatmap(lattice)

#
# x = [i for i in range(1, 50001, 100)]
# diff = []
# for i in [10, 15, 20, 25, 30, 35, 40, 45, 50, 70, 90]:
#     diff.append(get_diffusivity(x, np.load(f'40x40_T=1300_r=2.0/vacancy_{i}_metro_ep_2.0.npy')))
# np.save('diffusivity_data/40X40_T=1300_diffusivity_metro_2.0(10-50 at 5,70,90).npy', diff)

# plot_msd(100000, ['metro_ratio_1.5_data/vacancy_10_metro_ep_1.5.npy',
#                   'metro_ratio_1.5_data/vacancy_30_metro_ep_1.5.npy',
#                   'metro_ratio_1.5_data/vacancy_50_metro_ep_1.5.npy',
#                   'metro_ratio_1.5_data/vacancy_60_metro_ep_1.5.npy',
#                   'metro_ratio_1.5_data/vacancy_70_metro_ep_1.5.npy',
#                   'metro_ratio_1.5_data/vacancy_80_metro_ep_1.5.npy'])
# plot_msd(100000, ['40x40_T=1300_r=0.5/vacancy_10_metro_ep_0.5.npy',
#                   '40x40_T=1300_r=1.0/vacancy_10_metro_ep_1.0.npy',
#                   '40x40_T=1300_r=1.5/vacancy_10_metro_ep_1.5.npy',
#                   '40x40_T=1300_r=2.0/vacancy_10_metro_ep_2.0.npy'])
plot_diffusivity()
