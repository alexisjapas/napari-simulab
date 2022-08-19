from abc import ABC, abstractmethod


class Individual(ABC):
    def __init__(self, genes, y, x) -> None:
        super().__init__()
        self.genes = genes
        self.y = y
        self.x = x

    def act(self, map):
        if self.y >= map.shape[0]:
            self.y = map.shape[0] - 1
        if self.x >= map.shape[1]:
            self.x = map.shape[1] - 1
