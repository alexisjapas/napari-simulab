from random import randint, seed


class Individual():
    def __init__(self, genes, y, x, max_energy, energy, cost_moving, cost_resting, cost_eating, reward_eating, seed) -> None:
        super().__init__()
        self.genes = genes
        self.y = y
        self.x = x
        self.max_energy = 100
        self.energy = 100
        self.cost_moving = cost_moving
        self.cost_resting = cost_resting
        self.cost_eating = cost_eating
        self.reward_eating = reward_eating
        self.decision = ['move_up', 'move_down', 'move_right', 'move_left', 'rest', 'eat', 'reproduce']
        self.seed = seed


    def decide(self):
        if randint(0, 2) == 0:
            seed(self.seed)
        decision = self.decision[randint(0, len(self.decision) - 1)]
        seed()
        return decision


    def move(self):
        # Mouvement boudings
        mov_pred_y = 0
        mov_pred_x = 0
        if self.decision == 'move_up':
            mov_pred_y += 1
        elif self.decision == 'move_down':
            mov_pred_y -= 1
        elif self.decision == 'move_right':
            mov_pred_x += 1
        elif self.decision == 'move_left':
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


    def rest(self):
        self.energy -= self.cost_resting


    def eat(self):
        self.energy -= self.cost_eating
        if self.energy > 0:
            self.energy += self.reward_eating


    def act(self, map):
        # Decision
        self.decision = self.decide()
        update_map = 0

        if self.decision.startswith("move"):  # MOVING
            self.move()
        elif self.decision == "rest":  # RESTING
            self.rest()
        elif self.decision == "eat":  # EATING
            self.eat()
        elif decision == "reproduce":  # REPRODUCING
            self.reproduce()

        # Consequencies of life x.x
        if self.energy <= 0:
            update_map = 1


        return update_map
