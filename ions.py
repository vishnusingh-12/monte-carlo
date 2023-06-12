class Ion:
    def __init__(self, pos, index=-1, value=0):
        self.value = value  # value of lattice site (0 - vacancy, 1 - ion)
        self.index = index
        self.final_pos = pos  # position of ion in space [y,x] list
        self.initial_pos = pos  # initial position of ion
        self.mapped_pos = pos  # position of ion in NxN lattice
