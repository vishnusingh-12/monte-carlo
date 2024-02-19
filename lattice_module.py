import random

import numpy as np
from ions import Ion


class Lattice:
    def __init__(self, size, vacancy, epsilon):
        # size is the dimensions of the square lattice
        # vacancy is the percentage of vacancies present in lattice (0.0-1.0)
        # epsilon is the interaction term between the ions
        self.size = size
        self.vacancy = vacancy
        self.epsilon = epsilon
        self.energy_lattice = self.get_energy_lattice()

    def delta_e(self, initial_pos, final_pos, lattice):
        """
        Calculates the change in energy of an ion when it tries to jump from one site to a vacant site.
        This change in energy will further be required in the Metropolis algorithm to select or reject
        the move
        :param initial_pos: position of the ion before jump
        :param final_pos: potential position of the ion after jump
        :param lattice: lattice 2d array, to make a copy of values and calculate energy without changing original lattice
        :return: returns the change in energy of the particle from the initial to final position (del_e)
        """

        # making a lattice array which has only values (1 and 0)
        lat = self.get_lattice_val_ind(lattice, 'value')

        # list of values of initial neighbours 1 or 0
        values_of_initial_neighbours = np.array([lat[i, j] for (i, j) in self.get_neighbours(initial_pos)])

        # initial energy of the ion according to ising model and adding energy penalty from energy lattice
        initial_energy = sum(self.epsilon * values_of_initial_neighbours) + self.epsilon * self.energy_lattice[
            initial_pos[0], initial_pos[1]]

        # ion making a jump to final position to calculate final energy
        lat[initial_pos[0], initial_pos[1]], lat[final_pos[0], final_pos[1]] = lat[final_pos[0], final_pos[1]], lat[
            initial_pos[0], initial_pos[1]]

        # list of values of final neighbours
        values_of_final_neighbours = np.array([lat[i, j] for (i, j) in self.get_neighbours(final_pos)])

        # final energy of the ion according to the ising model and adding energy penalty from energy lattice
        final_energy = sum(self.epsilon * values_of_final_neighbours) + self.epsilon * self.energy_lattice[
            final_pos[0], final_pos[1]]

        # calculating delta_e
        delta_e = final_energy - initial_energy

        # returning delta_E
        return delta_e

    def get_lattice(self):
        """
        Generates a 2d array of Ions. Each element is an object of Ion class. Ions and vacancies are randomly placed.
        :return: Returns the generated 2d array of Ions.(lattice)
        """
        # getting number of vacant sites
        vacant = round(self.size * self.size * self.vacancy)

        # getting number of occupied sites
        occupied = self.size * self.size - vacant

        # making an array of 0 (unoccupied) and 1(occupied)
        lattice = np.array([0] * int(vacant) + [1] * int(occupied))

        # shuffling positions of 1's and 0's
        np.random.shuffle(lattice)

        # reshaping to a 2D matrix
        lattice = lattice.reshape((self.size, self.size))

        # making a matrix of ions (class Ion)
        ion_lattice = np.ndarray((self.size, self.size), dtype=Ion)

        # placing Ions with value=1 at places where 1 is present and Ions with value=0 where 0 is present
        for i in range(self.size):
            for j in range(self.size):
                if lattice[i, j] == 1:
                    ion_lattice[i, j] = Ion([i, j], 1, index=self.size * i + j + 1)
                else:
                    ion_lattice[i, j] = Ion([i, j], 0)

        # returning the lattice
        return ion_lattice

    def print_lattice(self, lattice, parameter='value'):

        """
        Prints the lattice values or index matrix
        :param lattice: 2d array of Ions whose values or indices  have to be printed
        :param parameter: string that tells whether to print values or index of the given lattice
        :return: does not return but prints the matrix
        """
        # if parameter is index , index matrix is printed
        if parameter.lower() == 'index':
            for i in range(self.size):
                for j in range(self.size):
                    print(lattice[i, j].index, end=' ')
                print()

        # if parameter is value , value matrix is printed
        if parameter.lower() == 'value':
            for i in range(self.size):
                for j in range(self.size):
                    print(lattice[i, j].value, end=' ')
                print()

    def get_lattice_val_ind(self, lattice, parameter):
        """
        Similar to print_lattice function, this functions returns a numpy matrix of values or indices
        to be used for calculations
        :param lattice: 2d numpy array lattice of Ions lattice whose values or indices matrix has to be created
        :param parameter: string that tells whether value or index matrix has to be created
        :return: returns the 2d numpy array of values or indices
        """
        # creating a numpy matrix of zeroes of size of the lattice
        lat = np.zeros((self.size, self.size))

        # if parameter is index returns numpy array of indices
        if parameter.lower() == 'index':
            for i in range(self.size):
                for j in range(self.size):
                    lat[i, j] = lattice[i, j].index
            return lat

        # if parameter is value then return numpy array of values
        if parameter.lower() == 'value':
            for i in range(self.size):
                for j in range(self.size):
                    lat[i, j] = lattice[i, j].value
            return lat

    def get_ions(self, lattice):
        """
        Creates and returns a list of all the ions present in a lattice
        :param lattice: The 2d numpy array of ions from where ions has ti be collected
        :return: returns the list of collected ions
        """
        # defining an empty list
        ions = []

        # appends in the ions list if the value of Ion is 1 i.e. if ion is present append , if vacancy is present don't.
        for i in range(self.size):
            for j in range(self.size):
                if lattice[i, j].value == 1:
                    ions.append(lattice[i, j])

        # returns the list of ions in the lattice
        return np.array(ions)

    def get_neighbours(self, pos):
        """
        Makes a list of 4 neighboring positions to a given position based on Periodic Boundary Conditions(PBC)
        :param pos: the position corresponding to which neighbors are required.
        :return: returns list of tuples where each tuple has position of neighbors
        """
        # [up,down,left,right]
        return [((pos[0] - 1) % self.size, pos[1]),
                ((pos[0] + 1) % self.size, pos[1]),
                (pos[0], (pos[1] - 1) % self.size),
                (pos[0], (pos[1] + 1) % self.size)
                ]

    def get_energy_lattice(self):
        """
        The Function creates an energy lattice with each element as the energy penalty at that lattice site.
        :return: Returns the energy lattice (numpy matrix)
        """

        # calculating number of vacancies. The number of vacancies will decide the number of energy penalties.
        num_of_vacancies = round(self.size * self.size * self.vacancy)

        # creating a lattice with all elements zero
        energy_lattice = np.zeros((self.size, self.size))

        # iterating the number of times equal to number of vacancies
        for i in range(num_of_vacancies):

            # randomly picking a site
            site_to_update = (random.randint(0, self.size - 1), random.randint(0, self.size - 1))

            # increasing the value of that site by 1. When we use these values, epsilon has to be multiplied
            energy_lattice[site_to_update[0], site_to_update[1]] = energy_lattice[
                                                                       site_to_update[0], site_to_update[1]] + 1
        # returning the updated lattice

        return energy_lattice
