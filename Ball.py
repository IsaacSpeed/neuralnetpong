import pygame.draw


class Ball:
    background_color = (0, 0, 0)
    foreground_color = (255, 255, 255)
    max_velocity = 1

    def __init__(self, vx, vy, radius, surface):
        self.x = surface.get_width() // 2
        self.y = surface.get_height() // 2
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.surface = surface
        self.x_accumulator = 0
        self.y_accumulator = 0

    def check_collision(self, other):
        if other.paddle.rect.left - self.radius < self.x < other.paddle.rect.right + self.radius and\
                other.paddle.rect.top - self.radius < self.y + self.vy < other.paddle.rect.bottom + self.radius:
            other.collide()
            if self.y > 50:
                self.y -= 10
            return True
        else:
            return False

    def is_past_top_of_screen(self):
        return self.y + self.radius < 0

    def is_past_bottom_of_screen(self):
        return self.y - self.radius > self.surface.get_height()

    def respawn(self, vx, vy):
        self.vx = vx
        self.vy = vy
        self.x = self.surface.get_width() // 2
        self.y = self.surface.get_height() // 2
        self.y_accumulator = 0
        self.x_accumulator = 0

        if self.vy > Ball.max_velocity:
            self.vy = Ball.max_velocity
        elif self.vy < -1 * Ball.max_velocity:
            self.vy = -1 * Ball.max_velocity
        if self.vx > Ball.max_velocity:
            self.vx = Ball.max_velocity
        elif self.vx < -1 * Ball.max_velocity:
            self.vx = -1 * Ball.max_velocity

    def move(self, players):
        self.undraw()

        for player in players:
            if self.check_collision(player):
                self.vy *= -1
                self.y_accumulator *= -1

        if self.x - self.radius + self.x_accumulator < 0:
            self.vx *= -1
            self.x_accumulator = 0
        elif self.x + self.radius + self.x_accumulator > self.surface.get_width():
            self.vx *= -1
            self.x_accumulator = 0

        if abs(round(self.x_accumulator)) >= 1:
            self.x_accumulator = 0
        if abs(round(self.y_accumulator)) >= 1:
            self.y_accumulator = 0

        self.x_accumulator += self.vx
        self.y_accumulator += self.vy

        self.x += round(self.x_accumulator)
        self.y += round(self.y_accumulator)
        self.draw()

    def draw(self):
        pygame.draw.circle(self.surface, Ball.foreground_color, (self.x, self.y), self.radius, 0)

    def undraw(self):
        pygame.draw.circle(self.surface, Ball.background_color, (self.x, self.y), self.radius, 0)

