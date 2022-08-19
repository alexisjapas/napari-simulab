from Individual import Individual


class Predator(Individual):
    def __init__(self, genes, y, x) -> None:
        super().__init__(genes, y, x)

    def act(self, map):
        self.y += 0
        self.x += 1

        super().act(map)