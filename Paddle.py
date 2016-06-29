import pygame
from pygame import Rect


# A paddle class
class Paddle:
    background_color = (0, 0, 0)
    foreground_color = (255, 255, 255)

    def __init__(self, x, y, width, height, surface):
        self.rect = Rect(x, y, width, height)
        self.surface = surface

    def move(self, dx):
        self.undraw()
        self.rect.move_ip(dx, 0)
        self.draw()

    def draw(self):
        pygame.draw.rect(self.surface, Paddle.foreground_color, self.rect, 0)

    def undraw(self):
        pygame.draw.rect(self.surface, Paddle.background_color, self.rect, 0)
