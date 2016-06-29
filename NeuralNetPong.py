import pygame
from pygame.locals import *
from Ball import Ball
from DumbComputerPlayer import DumbComputerPlayer
from NeuralNetPlayer import NeuralNetPlayer


def main():
    sqrt_number_of_screens = 5
    speed_multiplier = 1.0
    screens = []
    players = []
    balls = []

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("NeuralNetPong")

    main_surface = pygame.Surface(screen.get_size())
    main_surface = main_surface.convert()
    main_surface.fill((0, 0, 0))

    for i in range(0, sqrt_number_of_screens):
        array_of_screens = []
        array_of_players = []
        array_of_balls = []
        for j in range(0, sqrt_number_of_screens):
            surface = pygame.Surface((main_surface.get_width() // sqrt_number_of_screens, main_surface.get_height()
                                      // sqrt_number_of_screens))
            pygame.draw.rect(surface, (150, 150, 150), Rect(0, 0, surface.get_width(), surface.get_height()), 1)

            ball = Ball(0.25, 0.25, 5, surface)
            top_player = NeuralNetPlayer(surface.get_width() // 2, 15, ball, surface)
            bottom_player = NeuralNetPlayer(surface.get_width() // 2, surface.get_height() - 15, ball, surface)

            array_of_screens.append(surface)
            array_of_balls.append(ball)
            array_of_players.append([top_player, bottom_player])
        screens.append(array_of_screens)
        balls.append(array_of_balls)
        players.append(array_of_players)

    screen.blit(main_surface, (0, 0))
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        for i in range(0, sqrt_number_of_screens):
            for j in range(0, sqrt_number_of_screens):
                surface = screens[i][j]
                ball = balls[i][j]
                top_player = players[i][j][0]
                bottom_player = players[i][j][1]

                ball.move([bottom_player.paddle, top_player.paddle])

                if ball.is_past_bottom_of_screen():
                    top_player.score += 1
                    ball.respawn(ball.vx * speed_multiplier, ball.vy * speed_multiplier * -1)
                elif ball.is_past_top_of_screen():
                    bottom_player.score += 1
                    ball.respawn(ball.vx * speed_multiplier, ball.vy * speed_multiplier * -1)

                top_player.play(False)
                bottom_player.play(False)

                main_surface.blit(surface, (surface.get_width() * j, surface.get_height() * i))

        screen.blit(main_surface, (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    main()
