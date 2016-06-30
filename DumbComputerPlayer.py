from Paddle import Paddle
import math


class DumbComputerPlayer:
    def __init__(self, x, y, ball, surface):
        self.paddle = Paddle(x, y, math.floor(surface.get_width() * 0.2),
                             math.floor(surface.get_height() * 0.05), surface)
        self.ball = ball
        self.score = 0

    def play(self):
        if self.paddle.rect.centerx < self.ball.x:
            self.paddle.move(1)
        elif self.paddle.rect.centerx > self.ball.x:
            self.paddle.move(-1)

    def collide(self):
        return
