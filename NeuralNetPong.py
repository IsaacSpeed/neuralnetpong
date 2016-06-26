import pygame
from pygame.locals import *
from Paddle import Paddle
from Ball import Ball
from DumbComputerPlayer import DumbComputerPlayer


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("NeuralNetPong")

    main_surface = pygame.Surface(screen.get_size())
    main_surface = main_surface.convert()
    main_surface.fill((0, 0, 0))

    screen.blit(main_surface, (0, 0))
    pygame.display.flip()

    ball = Ball(-0.25, -0.25, 5, main_surface)
    top_player = DumbComputerPlayer(150, 10, ball, main_surface)
    bottom_player = DumbComputerPlayer(150, 450, ball, main_surface)

    speed_multiplier = 1

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
        ball.move([bottom_player.paddle, top_player.paddle])

        if ball.is_past_bottom_of_screen():
            top_player.score += 1
            ball.respawn(ball.vx * speed_multiplier, ball.vy * speed_multiplier * -1)
            print("" + str(ball.vx) + "   " + str(ball.vy))
        elif ball.is_past_top_of_screen():
            bottom_player.score += 1
            ball.respawn(ball.vx * speed_multiplier, ball.vy * speed_multiplier * -1)

        top_player.play()
        # bottom_player.play()
        screen.blit(main_surface, (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    main()
