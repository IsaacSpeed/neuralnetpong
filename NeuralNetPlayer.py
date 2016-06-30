from Paddle import Paddle
from NeuralNetwork import NeuralNetwork
import math


class NeuralNetPlayer:
    def __init__(self, x, y, ball, surface):
        if surface != None:
            self.paddle = Paddle(x, y, math.floor(surface.get_width() * 0.2),
                                 math.floor(surface.get_height() * 0.05), surface)
        else:
            self.paddle = None
        self.ball = ball
        self.score = 0
        self.fitness_score = 0
        self.network = NeuralNetwork(1, [3, 3, 2])
        self.last_output = []

    @classmethod
    def empty(cls):
        player = cls(0, 0, None, None)
        return player

    @classmethod
    def from_other(cls, other):
        player = cls(other.paddle.surface.get_width() // 2, other.y, other.ball, other.paddle.surface)
        player.network = NeuralNetwork.from_other_network(other.network)
        return player

    @classmethod
    def crossover(cls, first, second):
        child = cls(first.paddle.surface.get_width() // 2, first.y, first.ball, first.paddle.surface)
        child.network = NeuralNetwork.crossover(first.network, second.network)
        return child

    def collide(self):
        self.fitness_score += 10

    def get_fitness_score(self):
        return self.fitness_score + self.score * 50

    def mutate(self):
        self.network.mutate()

    def play(self, debug):
        target_x = self.ball.x
        self_x = self.paddle.rect.x
        outputs = self.network.feed_forward([self_x - target_x])
        movement = 0

        # first output is should I move?
        if outputs[0] == 1:
            movement = -1

            # second is, which direction?
            if outputs[1] == 1:
                movement = 1

        self.paddle.move(movement)
        self.network.mutate()

        if debug == True:
            if self.last_output != outputs:
                if self.paddle.rect.x < 100: print("      ", end="")
                print(outputs)
            self.last_output = outputs
