import pygame
from pygame.locals import *
from Ball import Ball
from DumbComputerPlayer import DumbComputerPlayer
from NeuralNetPlayer import NeuralNetPlayer
from GeneticAlgorithm import GeneticAlgorithm
from Paddle import Paddle
import math
import time


def main():
    speed_multiplier = 1.0
    screens = []
    players = []
    balls = []

    genetic_algorithm = GeneticAlgorithm(50, 16)

    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("NeuralNetPong")

    main_surface = pygame.Surface(screen.get_size())
    main_surface = main_surface.convert()
    main_surface.fill((0, 0, 0))

    max_index = math.floor(math.sqrt(len(genetic_algorithm.population)))
    for i in range(0, max_index):
        array_of_screens = []
        array_of_players = []
        array_of_balls = []
        for j in range(0, max_index):
            surface = pygame.Surface((main_surface.get_width() // max_index, main_surface.get_height() // max_index))
            pygame.draw.rect(surface, (150, 150, 150), Rect(0, 0, surface.get_width(), surface.get_height()), 1)

            ball = Ball(0.25, 0.25, 5, surface)
            top_player = DumbComputerPlayer(surface.get_width() // 2, 5, ball, surface)

            player_index = i * max_index + j
            bottom_player = genetic_algorithm.population[player_index]
            bottom_player.ball = ball
            bottom_player.paddle = Paddle(surface.get_width() // 2, surface.get_height() - 15,
                                          math.floor(surface.get_width() * 0.2),
                                          math.floor(surface.get_height() * 0.05), surface)
            bottom_player.x = surface.get_width() // 2
            bottom_player.y = surface.get_height() // 2

            array_of_screens.append(surface)
            array_of_balls.append(ball)
            array_of_players.append([top_player, bottom_player])
        screens.append(array_of_screens)
        balls.append(array_of_balls)
        players.append(array_of_players)

    screen.blit(main_surface, (0, 0))
    pygame.display.flip()

    start_time = time.clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

        current_time = time.clock()
        if current_time - start_time > 3:
            should_continue = genetic_algorithm.next_generation()

            print("Respawning! Now generation {:}".format(genetic_algorithm.generation_counter))

            for i in range(0, max_index):
                array_of_players = []
                for j in range(0, max_index):
                    players[i][j][0].paddle.undraw()
                    players[i][j][1].paddle.undraw()
                    surface = screens[i][j]
                    ball = balls[i][j]
                    ball.undraw()

                    ball.respawn(ball.vx, ball.vy)
                    top_player = DumbComputerPlayer(surface.get_width() // 2, 5, ball, surface)

                    player_index = i * max_index + j
                    bottom_player = genetic_algorithm.population[player_index]
                    bottom_player.ball = ball
                    bottom_player.paddle = Paddle(surface.get_width() // 2, surface.get_height() - 15,
                                                  math.floor(surface.get_width() * 0.2),
                                                  math.floor(surface.get_height() * 0.05), surface)
                    bottom_player.x = surface.get_width() // 2
                    bottom_player.y = surface.get_height() // 2

                    array_of_players.append([top_player, bottom_player])
                players[i] = array_of_players

            if not should_continue:
                running = False

            start_time = time.clock()

        for i in range(0, max_index):
            for j in range(0, max_index):
                surface = screens[i][j]
                ball = balls[i][j]
                top_player = players[i][j][0]
                bottom_player = players[i][j][1]

                ball.move([bottom_player, top_player])

                if ball.is_past_bottom_of_screen():
                    top_player.score += 1
                    ball.respawn(ball.vx * speed_multiplier, ball.vy * speed_multiplier * -1)
                elif ball.is_past_top_of_screen():
                    bottom_player.score += 1
                    ball.respawn(ball.vx * speed_multiplier, ball.vy * speed_multiplier * -1)

                top_player.play()
                bottom_player.play(False)

                main_surface.blit(surface, (surface.get_width() * j, surface.get_height() * i))

        screen.blit(main_surface, (0, 0))
        pygame.display.flip()


if __name__ == '__main__':
    main()
