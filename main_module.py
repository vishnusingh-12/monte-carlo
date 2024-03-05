# important conversion r=1/T^*
# importing dependencies
import numpy as np
from lattice_module import Lattice
import random
from msd_module import get_msd
from scipy.constants import Boltzmann
import time
import winsound
from plots_module import plot_energy_heatmap

# for estimation of simulation run time
start_time = time.time()

# number of Monte Carlo Steps
mc_steps = 100000

# Temperature
temperature = 1300

# ratio of epsilon/KbT
temperature_star = 2.0

# Energy interaction between ions
epsilon = (temperature * Boltzmann) / temperature_star

# inverse temperature
beta = 1 / (Boltzmann * temperature)

# lattice size
N = 40

# vacancy
vacancy = 0.15

# movement of ions up down left right
# (1,0)=down,(0,1)=right,(-1,0)=up,(0,-1)=left
moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Creating Lattice Class Object of 40x40, vacancy, epsilon= interaction term
lattice = Lattice(N, vacancy, epsilon)

# plotting energy lattice
plot_energy_heatmap(lattice)

# getting matrix of ions using Lattice class function
lat_2d = lattice.get_lattice()

# Simulation starts here
for i in range(mc_steps):

    # for each MC step a list of all ions is fetched from the lattice matrix
    ions = lattice.get_ions(lat_2d)

    # The list is shuffled so that ions are picked at random
    np.random.shuffle(ions)

    for ion in ions:

        # for each ion a random step is selected from moves defined above
        step = random.choice(moves)

        # the potential position of the ion in the lattice is calculated if the move is accepted according to PBC
        potential_pos = [(ion.mapped_position[0] + step[0]) % lattice.size,
                         (ion.mapped_position[1] + step[1]) % lattice.size]

        # if an ion is found at potential position
        if lat_2d[potential_pos[0], potential_pos[1]].value == 1:

            # reject move

            # checks whether to store the ion position or not. I am storing ion position after every 100 steps
            if (i + 1) % 100 == 0:
                # stores current position of the ion in space into a list
                ion.position_list.append(ion.position)

            # continue without updating ion as collision has occurred
            continue

        # if ion not found at potential position
        else:

            # calculate delta_e between new position and initial position
            delta_e = lattice.delta_e(ion.mapped_position, potential_pos, lat_2d)

            # if delta e is less than 0
            if delta_e < 0:

                # always accept the move

                # swap the ion and the vacancy
                lat_2d[ion.mapped_position[0], ion.mapped_position[1]], lat_2d[potential_pos[0], potential_pos[1]] = \
                    lat_2d[potential_pos[0], potential_pos[1]], lat_2d[ion.mapped_position[0], ion.mapped_position[1]]

                # update the ion position in actual space
                ion.position = [ion.position[0] + step[0], ion.position[1] + step[1]]

                # update the ion position on the matrix
                ion.mapped_position = potential_pos

                # checks whether to store the ion position or not. I am storing ion position after every 100 steps
                if (i + 1) % 100 == 0:
                    # stores current position of the ion in space into a list
                    ion.position_list.append(ion.position)

            # if delta e is greater than 0
            else:

                # generate a random number between 0 and 1 and compare exp(-beta*delta_e)

                # if random number is less than or equal to exp(-beta*delta_e)
                if random.random() <= np.exp(-beta * delta_e):
                    # accept the move

                    # swap the ion and the vacancy
                    lat_2d[ion.mapped_position[0], ion.mapped_position[1]], lat_2d[potential_pos[0], potential_pos[1]] = \
                        lat_2d[potential_pos[0], potential_pos[1]], lat_2d[
                            ion.mapped_position[0], ion.mapped_position[1]]

                    # update the ion position in actual space
                    ion.position = [ion.position[0] + step[0], ion.position[1] + step[1]]

                    # update the ion position on the matrix
                    ion.mapped_position = potential_pos

                    # checks whether to store the ion position or not. I am storing ion position after every 100 steps
                    if (i + 1) % 100 == 0:
                        # stores current position of the ion in space into a list
                        ion.position_list.append(ion.position)

                # if random number is greater than exp(-beta*epsilon)
                else:

                    # reject move

                    # checks whether to store the ion position or not. I am storing ion position after every 100 steps
                    if (i + 1) % 100 == 0:
                        # stores current position of the ion in space into a list
                        ion.position_list.append(ion.position)

                    # continue without updating ion as collision has occurred
                    continue

# again getting ions list after simulation run
ions = lattice.get_ions(lat_2d)

# calculating msd , parameters passed are ions list and half of number of positions captured
msd = get_msd(ions, mc_steps // 200)  # original msd calculation

# saving msd to file
np.save(f'40x40_T=1300_r=0.5/vacancy_{round(vacancy * 100)}_metro_ep_0.5.npy', msd)

# for estimation of simulation run time
end_time = time.time()

# prints total time of simulation run in seconds
print(end_time - start_time)

# tells me when the simulation run is complete
winsound.Beep(1000, 500)
