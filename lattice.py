import numpy as np
from ions import Ion


class Lattice:
    def __init__(self, size, vacancy):
        self.size = size
        self.vacancy = vacancy

    def get_lattice(self):
        vacant = round(self.size * self.size * self.vacancy)
        occupied = self.size * self.size - vacant
        lattice = np.array([0] * int(vacant) + [1] * int(occupied))  # making an array of 0 (unoccupied) and 1(occ)
        np.random.shuffle(lattice)  # shuffling positions of 1's and 0's
        lattice = lattice.reshape((self.size, self.size))
        ion_lattice = np.ndarray((self.size, self.size), dtype=Ion)  # making a matrix of ions (class Ion)
        for i in range(self.size):
            for j in range(self.size):
                if lattice[i, j] == 1:
                    ion_lattice[i, j] = Ion([i, j], 1, index=self.size * i + j + 1)
                else:
                    ion_lattice[i, j] = Ion([i, j], 0)
        return ion_lattice

    def print_lattice(self, lattice, parameter):
        if parameter.lower() == 'index':
            for i in range(self.size):
                for j in range(self.size):
                    print(lattice[i, j].index, end=' ')
                print()
        if parameter.lower() == 'value':
            for i in range(self.size):
                for j in range(self.size):
                    print(lattice[i, j].value, end=' ')
                print()

    def get_ions(self, lattice):
        ions = []
        for i in range(self.size):
            for j in range(self.size):
                if lattice[i, j].value == 1:
                    ions.append(lattice[i, j])
        return np.array(ions)
