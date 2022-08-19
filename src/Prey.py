from Individual import Individual


class Prey(Individual):
    def __init__(self, genes, y, x) -> None:
        super().__init__(genes, y, x)

    def act(self, map):
        self.y += 1
        self.x += 0

        super().act(map)