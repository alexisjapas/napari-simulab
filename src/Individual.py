import numpy as np
from random import randint, seed, choice


class Individual():
    def __init__(self,
                 lab,
                 genes,
                 y, x,
                 max_energy,
                 energy,
                 cost_moving,
                 cost_resting,
                 cost_eating,
                 reward_eating,
                 cost_reproducting) -> None:
        super().__init__()
        self.lab = lab
        self.color = (randint(1, 255), randint(1, 255), randint(1, 255))
        self.genes = genes
        self.y = y
        self.x = x
        self.max_energy = 100
        self.energy = 100
        self.cost_moving = cost_moving
        self.cost_resting = cost_resting
        self.cost_eating = cost_eating
        self.reward_eating = reward_eating
        self.cost_reproducting = cost_reproducting
        self.decisions = ['move_up', 'move_down', 'move_right', 'move_left', 'rest', 'eat', 'reproduce']


    def decide(self):
        if randint(0, 5) == 0:
            seed(self.genes)
        self.decision = self.decisions[randint(0, len(self.decisions) - 1)]
        seed()


    def move(self, map):
        # Mouvement decision
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
        if self.x + mov_pred_x >= map.shape[1] or self.x + mov_pred_x < 0:
            mov_pred_x = 0

        # Other individuals boundings
        if np.sum(map[self.y + mov_pred_y, self.x, :]) != 0:
            mov_pred_y = 0
        if np.sum(map[self.y, self.x + mov_pred_x, :]) != 0:
            mov_pred_x = 0

        # Proceed
        self.y += mov_pred_y
        self.x += mov_pred_x

        return mov_pred_y != 0 or mov_pred_x != 0

    def rest(self):
        return 0


    def eat(self):
        return 0


    def reproduce(self, map):
        # Check available positions and secure map boundings
        available_pos = []
        if self.y+1 < map.shape[0] and np.sum(map[self.y + 1, self.x, :]) == 0:
            available_pos.append((self.y + 1, self.x))
        if self.y-1 >= 0 and np.sum(map[self.y - 1, self.x, :]) == 0:
            available_pos.append((self.y - 1, self.x))
        if self.x+1 < map.shape[1] and np.sum(map[self.y, self.x + 1, :]) == 0:
            available_pos.append((self.y, self.x + 1))
        if self.x-1 >= 0 and np.sum(map[self.y, self.x - 1, :]) == 0:
            available_pos.append((self.y, self.x - 1))

        # Reproduction
        if available_pos:
            pos = choice(available_pos)
            self.energy /= 2
            noob = Individual(
                    lab=self.lab,
                    genes=self.genes,
                    y=pos[0],
                    x=pos[1],
                    max_energy=self.max_energy,
                    energy=self.energy,
                    cost_moving=self.cost_moving,
                    cost_resting=self.cost_resting,
                    cost_eating=self.cost_eating,
                    reward_eating=self.reward_eating,
                    cost_reproducting=self.cost_reproducting)
            self.lab.individuals.append(noob)

        return True if available_pos else False


    def act(self, map):
        # Decision
        self.decide()

        update_map = 0
        if self.decision.startswith("move"):  # MOVING
            update_map = self.move(map)
            self.energy -= self.cost_moving
        elif self.decision == "rest":  # RESTING
            update_map = self.rest()
            self.energy -= self.cost_resting
        elif self.decision == "eat":  # EATING
            update_map = self.eat()
            self.energy -= self.cost_eating
            if self.energy > 0:
                self.energy += self.reward_eating
        elif self.decision == "reproduce":  # REPRODUCING
            if self.energy > 80:
                update_map = self.reproduce(map)

        # Consequencies of life x.x
        if self.energy <= 0:
            update_map = 1


        return update_map
