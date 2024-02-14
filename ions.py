class Ion:
    def __init__(self, pos, value, index=-1):
        self.position = pos
        self.mapped_position = pos
        self.value = value
        self.index = index
        self.position_list = [pos]
