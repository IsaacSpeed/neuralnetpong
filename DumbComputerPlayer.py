from Paddle import Paddle


class DumbComputerPlayer:
    def __init__(self, x, y, ball, surface):
        self.paddle = Paddle(x, y, 50, 10, surface)
        self.ball = ball
        self.score = 0

    def play(self):
        if self.paddle.rect.centerx < self.ball.x:
            self.paddle.move(1)
        elif self.paddle.rect.centerx > self.ball.x:
            self.paddle.move(-1)