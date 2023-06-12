import numpy as np
from lattice import Lattice
import random

moves = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # movement of ions up down left right
# (1,0)=down,(0,1)=right,(-1,0)=up,(0,-1)=left
lat = Lattice(20, 0.7)  # creating lattice object
init_lattice = lat.get_lattice()  # getting lattice matrix (matrix of ions and vacancies)
final_lattice = init_lattice.copy()  # storing a copy of lattice as initial lattice
for k in range(10000):  # Monte carlo steps
    ions = lat.get_ion_list(final_lattice)  # getting ions list to update them for each step
    for ion in ions:
        step = moves[random.randint(0, 3)]  # selecting a random move for ion movement
        temp_pos = [(ion.mapped_pos[0] + step[0]) % lat.N, (ion.mapped_pos[1] + step[1]) % lat.N]
        '''temp position is the position which ion is likely to take 
            inside the NxN matrix if the move is accepted or collision does not occur
            according to periodic boundary conditions'''
        if final_lattice[temp_pos[0], temp_pos[1]].value == 1:  # checking for ion on temp_pos
            continue  # if collision occurs, move to next ion
        else:
            '''If collision does not occur , interchange the ion with vacancy, change its mapped position on the
               NxN lattice, change its final position in space(which can be out of the NxN lattice) '''
            ion.final_pos = [ion.final_pos[0] + step[0], ion.final_pos[1] + step[1]]
            final_lattice[ion.mapped_pos[0], ion.mapped_pos[1]], final_lattice[temp_pos[0], temp_pos[1]] = \
                final_lattice[temp_pos[0], temp_pos[1]], final_lattice[ion.mapped_pos[0], ion.mapped_pos[1]]
