from Paddle import Paddle
from NeuralNetwork import NeuralNetwork


class NeuralNetPlayer:
    def __init__(self, x, y, ball, surface):
        self.paddle = Paddle(x, y, 50, 10, surface)
        self.ball = ball
        self.score = 0
        self.network = NeuralNetwork(1, [3, 3, 2])
        self.last_output = []

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
