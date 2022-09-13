from random import randint, seed


class Individual():
    def __init__(self, genes, y, x, max_energy, energy, cost_moving, cost_resting, cost_eating, seed) -> None:
        super().__init__()
        self.genes = genes
        self.y = y
        self.x = x
        self.max_energy = 100
        self.energy = 100
        self.cost_moving = cost_moving
        self.cost_resting = cost_resting
        self.cost_eating = cost_eating
        self.decision = ['move_up', 'move_down', 'move_right', 'move_left', 'rest', 'eat', 'reproduce']
        self.seed = seed


    def decide(self):
        if randint(0, 2) == 0:
            seed(self.seed)
        decision = self.decision[randint(0, len(self.decision) - 1)]
        seed()
        return decision


    def act(self, map):
        # Decision
        decision = self.decide()
        update_map = 0

        if decision.startswith("move"):  # MOVING
            # Mouvement boudings
            mov_pred_y = 0
            mov_pred_x = 0
            if decision == 'move_up':
                mov_pred_y += 1
            elif decision == 'move_down':
                mov_pred_y -= 1
            elif decision == 'move_right':
                mov_pred_x += 1
            elif decision == 'move_left':
                mov_pred_x -= 1
            # Map boundings
            if self.y + mov_pred_y >= map.shape[0] or self.y + mov_pred_y < 0:
                mov_pred_y = 0
                update_map = 1
            if self.x + mov_pred_x >= map.shape[1] or self.x + mov_pred_x < 0:
                mov_pred_x = 0
                update_map = 1
            # Other individuals boundings
            if map[self.y + mov_pred_y, self.x] != 0:
                mov_pred_y = 0
                update_map = 1
            if map[self.y, self.x + mov_pred_x] != 0:
                mov_pred_x = 0
                update_map = 1
            # Proceed
            self.y += mov_pred_y
            self.x += mov_pred_x
            self.energy -= self.cost_moving

        elif decision == "rest":  # RESTING
            self.energy -= self.cost_resting

        elif decision == "eat":  # EATING
            self.energy = min(self.energy - self.cost_eating, self.max_energy)

        elif decision == "reproduce":  # REPRODUCING
            pass

        # Consequencies of life
        if self.energy <= 0:
            update_map = 1


        return update_map
