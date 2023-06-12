import numpy as np
from ions import Ion


class Lattice:
    def __init__(self, n, coverage, epsilon=None, j=None):
        # epsilon is energy penalty,j is interaction term between ions
        self.N = n
        self.coverage = coverage

    def get_lattice(self):
        """ Returns a matrix of NxN ions and vacancies.
            Each ion in the matrix is defined as an object of Ion class"""

        occupied = round((self.N * self.N) * self.coverage)  # number of lattice points to be occupied
        unoccupied = (self.N * self.N) - occupied  # number of vacant lattice points
        lattice = np.array([0] * int(unoccupied) + [1] * int(occupied))  # making an array of 0 (unoccupied) and 1(occ)
        np.random.shuffle(lattice)  # shuffling positions of 1's and 0's
        lattice = lattice.reshape((self.N, self.N))  # reshaping 2 a matrix
        np.save('init_lat.npy', lattice)  # saving lattice(matrix) to a text file
        lattice_ions = np.ndarray((self.N, self.N), dtype=Ion)  # making a matrix of ions (class Ion)
        for i in range(self.N):
            for j in range(self.N):
                if lattice[i][j] == 1:  # for every 1, putting an ion with value 1 (ion)
                    lattice_ions[i][j] = Ion([i, j], index=self.N * i + j, value=1)
                else:  # for every 0, putting an ion with value 0 (vacancy)
                    lattice_ions[i][j] = Ion([i, j])

        return lattice_ions  # returns a NxN matrix of ions and vacancies

    def get_init_positions(self, lattice):
        """Returns a matrix of initial positions of all the ions in the lattice .
           Each row is a list of two coordinates [y,x] of the initial position
           of the ion"""
        init_pos = []
        for i in range(self.N):
            for j in range(self.N):
                if lattice[i][j].value == 1:
                    init_pos.append(lattice[i, j].initial_pos)
        pos = np.array(init_pos)
        return pos

    def get_final_positions(self, lattice):
        """Returns a matrix of final positions of all the ions in the lattice .
           Each row is a list of two coordinates [y,x] of the final position
           of the ion"""
        init_pos = []
        for i in range(self.N):
            for j in range(self.N):
                if lattice[i][j].value == 1:
                    init_pos.append(lattice[i, j].final_pos)
        pos = np.array(init_pos)
        return pos

    def show_init_lattice(self):
        """Gives an overview of the initial lattice based on 1's(ion) and 0's(vacancy) """
        lattice = np.load('init_lat.npy')
        print(lattice)

    def get_ion_list(self, lattice):
        """Returns a list of all the ions from the lattice.
           Very useful while updating every ion according to a selected move  """
        ion_list = []
        for i in range(self.N):
            for j in range(self.N):
                if lattice[i][j].value == 1:
                    ion_list.append(lattice[i][j])
        return ion_list

    def print_lattice(self, lattice, parameter):
        """Prints the lattice based on the value of 'parameter'.
           If parameter=index, its gives a matrix of ion indices.
           Indices of vacancies are given by -1.
           We only need to track ions and not vacancies.
           If parameter = value, it gives a matrix of 1's(ions) and 0's (vacancies)
           """
        if parameter.lower() == 'index':
            for i in range(self.N):
                for j in range(self.N):
                    print(lattice[i, j].index, end=' ')
                print()
        if parameter.lower() == 'value':
            for i in range(self.N):
                for j in range(self.N):
                    print(lattice[i, j].value, end=' ')
                print()
