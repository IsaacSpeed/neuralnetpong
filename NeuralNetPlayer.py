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
        self.fitness_score = 1
        self.network = NeuralNetwork(2, [4, 4, 1])
        self.x_accumulator = 0.0

    @classmethod
    def empty(cls):
        player = cls(0, 0, None, None)
        return player

    @classmethod
    def from_other(cls, other):
        player = cls(other.paddle.surface.get_width() // 2, other.paddle.rect.y, other.ball, other.paddle.surface)
        player.network = NeuralNetwork.from_other_network(other.network)
        return player

    @classmethod
    def crossover(cls, first, second):
        child = cls(first.paddle.surface.get_width() // 2, first.paddle.rect.y, first.ball, first.paddle.surface)
        child.network = NeuralNetwork.crossover(first.network, second.network)
        return child

    def collide(self):
        self.fitness_score += 3

    def get_fitness_score(self):
        return self.fitness_score

    def mutate(self):
        self.network.mutate()

    def play(self):
        target_x = self.ball.x
        self_x = self.paddle.rect.x

        outputs = self.network.feed_forward([self_x, target_x])

        if self.x_accumulator > 1:
            self.x_accumulator = 1
        elif self.x_accumulator < -1:
            self.x_accumulator = -1

        self.x_accumulator += outputs[0] * 3

        if self.paddle.rect.left > self.paddle.surface.get_width():
            self.paddle.move(-1)
        elif self.paddle.rect.right < 0:
            self.paddle.move(1)
        else:
            self.paddle.move(self.x_accumulator)
