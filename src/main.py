#!/usr/bin/env python3
import os
import random
import sys

import pygame
from pygame.locals import *


class Snake(object):
    """..."""
    def __init__(
            self, x: int = 0, y: int = 0, w: int = 20, h: int = 20) -> None:
        """..."""
        self.__x, self.__y, self.__w, self.__h = x, y, w, h
        self.__direction = 'down'
        self.__coordinates = [(x, y + h * 2), (x, y + h), (x, y)]
        self.__head_coordinate = self.__coordinates[0]
        self.__tail_coordinate = self.__coordinates[-1]
        self.__head_tail_color = (0, 0, 0)
        self.__last_used_color = (0, 0, 0)
        self.__color_by_coordinate = {
            self.__coordinates[0]: (255, 0, 0),
            self.__coordinates[1]: (220, 210, 130),
            self.__coordinates[2]: (0, 0, 0)}

    @property
    def coordinates(self) -> list:
        """X and Y coordinates

        Coordinates that define where the character will be drawn on
        the screen
        """
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, coordinates: list) -> None:
        # ...
        self.__coordinates = coordinates
        self.__tail_coordinate = coordinates[-1]
        self.__head_coordinate = coordinates[0]

    @property
    def head_coordinate(self) -> tuple:
        """X and Y head coordinates

        The coordinates of the snake's head
        """
        return self.__head_coordinate

    @head_coordinate.setter
    def head_coordinate(self, coordinate: tuple) -> None:
        # ...
        self.__head_coordinate = coordinate

    @property
    def tail_coordinate(self) -> tuple:
        """..."""
        return self.__tail_coordinate

    @property
    def h(self) -> int:
        """..."""
        return self.__h

    @property
    def w(self) -> int:
        """..."""
        return self.__w

    @property
    def x(self) -> int:
        """..."""
        return self.__x

    @property
    def y(self) -> int:
        """..."""
        return self.__y

    def color_by_coordinate(self, coordinate: tuple) -> tuple:
        """..."""
        colors = {
            'white-1': (220, 210, 130),
            'black-1': (0, 0, 0),
            'black-2': (0, 0, 0),
            'white-2': (220, 210, 130),
            'red-1': (255, 0, 0),
            'red-2': (255, 0, 0),
            'red-3': (255, 0, 0)}

        choose_color = {
            'red-2': 'red-3',
            'red-3': 'white-1',
            'white-1': 'black-1',
            'black-1': 'black-2',
            'black-2': 'white-2',
            'white-2': 'red-1',
            'red-1': 'red-2', }

        color = 'white-2'
        for c in self.__coordinates:
            self.__color_by_coordinate[c] = colors[choose_color[color]]
            color = choose_color[color]

        if (coordinate == self.__head_coordinate or
                coordinate == self.__tail_coordinate):
            return self.__head_tail_color
        return self.__color_by_coordinate[coordinate]

    def grow(self, coordinate: tuple) -> None:
        """Increases the size of the snake

        Adds a length item on snake front (on head) where the mouse was

        :param coordinate: x and y mouse coordinate tuple
        """
        self.__coordinates.insert(0, coordinate)

    def walk_in_coordinate_direction(self, direction: str) -> None:
        """..."""
        x, y = self.__head_coordinate
        if direction == 'down':
            if self.__direction != 'up':
                y += self.__h
                self.__direction = 'down'
        elif direction == 'up':
            if self.__direction != 'down':
                y -= self.__h
                self.__direction = 'up'
        elif direction == 'left':
            if self.__direction != 'right':
                x -= self.__w
                self.__direction = 'left'
        elif direction == 'right':
            if self.__direction != 'left':
                x += self.__w
                self.__direction = 'right'

        self.__coordinates.pop()
        self.__coordinates.insert(0, (x, y))
        self.__head_coordinate = (x, y)
        self.__tail_coordinate = self.__coordinates[-1]


class Mouse(object):
    """..."""
    def __init__(
            self, x: int = 0, y: int = 0, w: int = 20, h: int = 20) -> None:
        """..."""
        self.__x, self.__y, self.__w, self.__h = x, y, w, h
        self.__coordinates = [(self.__x, self.__y)]

    @property
    def coordinates(self) -> list:
        """X and Y coordinates

        Coordinates that define where the character will be drawn on
        the screen
        """
        return self.__coordinates

    @property
    def h(self) -> int:
        """..."""
        return self.__h

    @property
    def w(self) -> int:
        """..."""
        return self.__w

    @property
    def x(self) -> int:
        """..."""
        return self.__x

    @property
    def y(self) -> int:
        """..."""
        return self.__y

    def raffle_new_coordinates(self, area: tuple) -> None:
        """Updates the x and y coordinates

        Coordinates where the mouse will be drawn
        """
        self.__coordinates = [(
            random.randrange(self.__w, area[0] - self.__w, self.__w),
            random.randrange(self.__h, area[1] - self.__h, self.__h))]
        self.__x, self.__y = self.__coordinates[0]


class SnakeGame(object):
    """..."""
    def __init__(
            self, x: int = 0, y: int = 0, w: int = 600, h: int = 400) -> None:
        """..."""
        self.__x, self.__y, self.__w, self.__h = x, y, w, h
        self.__game_path = os.path.dirname(os.path.abspath(__file__))

        pygame.init()
        pygame.font.SysFont('arial', 30, True, True)
        pygame.display.set_caption('Snake - Micrurus corallinus')
        pygame.mixer.music.load(
            os.path.join(
                self.__game_path,
                'resources',
                # https://freemusicarchive.org/music/Peter_Gresser/
                'Peter Gresser - Skipping in the No Standing Zone.mp3'))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        self.__screen = pygame.display.set_mode((self.__w, self.__h))

        self.__snake = Snake(x=self.__w // 2 - 20, y=20, w=20, h=20)
        self.__snake_eating_mouse_sound = pygame.mixer.Sound(
            # https://themushroomkingdom.net/media/smw/wav
            os.path.join(self.__game_path, 'resources', 'smw_kick.wav'))

        self.__mouse = Mouse(
            x=random.randrange(20, self.__w - 20, 20),
            y=random.randrange(20, self.__h - 20, 20),
            w=20, h=20)

        self.__clock = pygame.time.Clock()
        self.__clock_tick = 5
        self.__running = True
        self.__direction = 'down'

    def run(self) -> int:
        """..."""
        while self.__running:
            self.__clock.tick(self.__clock_tick)
            self.__screen.fill((110, 160, 120))

            self.__handle_keyboard_keys_event()
            self.__handle_characters_state()

            self.__draw()
            pygame.display.update()
        return 0

    def __draw(self) -> None:
        # ...
        # pygame.draw.circle(screen, (0, 0, 100), (300, 260), 40)
        # pygame.draw.line(screen, (0, 0, 100), (390, 0), (390, 600), 5)

        for mouse_x_y in self.__mouse.coordinates:
            pygame.draw.rect(
                self.__screen, (100, 100, 110),
                (mouse_x_y[0], mouse_x_y[1], self.__mouse.w, self.__mouse.h))

        for snake_x_y in self.__snake.coordinates:
            pygame.draw.rect(
                self.__screen, self.__snake.color_by_coordinate(snake_x_y),
                (snake_x_y[0], snake_x_y[1], self.__snake.w, self.__snake.h))

    def __handle_characters_state(self) -> None:
        # ...
        # message = f'Pontos: {points}'
        # text = font.render(message, True, (0, 0, 0))
        # screen.blit(text, (450, 40))
        self.__snake.walk_in_coordinate_direction(self.__direction)
        self.__snake_appears_on_inverse_screen_side()
        self.__snake_collides_itself()
        self.__snake_eat_the_mouse()

    def __handle_keyboard_keys_event(self):
        # ...
        # pressed = pygame.key.get_pressed()
        # if pressed[pygame.K_UP]:
        #     if snake_y > 0:
        #         snake_y -= 20
        # if pressed[pygame.K_DOWN]:
        #     if snake_y < height - 50:
        #         snake_y += 20
        # if pressed[pygame.K_LEFT]:
        #     if snake_x > 0:
        #         snake_x -= 20
        # if pressed[pygame.K_RIGHT]:
        #     if snake_x < width - 50:
        #         snake_x += 20

        keys = {K_LEFT: 'left', K_RIGHT: 'right', K_UP: 'up', K_DOWN: 'down'}
        opposite_direction = {
            'down': 'up', 'up': 'down', 'left': 'right', 'right': 'left'}

        for event in pygame.event.get():
            if event.type == QUIT:
                self.__running = False
                break

            if event.type == KEYDOWN:
                if event.key in keys:
                    if keys[event.key] == self.__direction:
                        self.__speed_up_snake()

                    if keys[event.key] != opposite_direction[self.__direction]:
                        self.__direction = keys[event.key]

    def __snake_eat_the_mouse(self) -> None:
        # ...
        if self.__snake.head_coordinate == self.__mouse.coordinates[0]:
            self.__snake.grow(self.__mouse.coordinates[0])
            self.__mouse.raffle_new_coordinates((self.__w, self.__h))
            self.__snake_eating_mouse_sound.play()

    def __snake_appears_on_inverse_screen_side(self) -> None:
        # ...
        if self.__snake.head_coordinate[0] > self.__w:
            self.__snake.coordinates.pop(0)
            new_head_coordinate = (0, self.__snake.head_coordinate[1])
            self.__snake.coordinates.insert(0, new_head_coordinate)
            self.__snake.head_coordinate = new_head_coordinate

        elif self.__snake.head_coordinate[0] < 0:
            self.__snake.coordinates.pop(0)
            new_head_coordinate = (self.__w, self.__snake.head_coordinate[1])
            self.__snake.coordinates.insert(0, new_head_coordinate)
            self.__snake.head_coordinate = new_head_coordinate

        elif self.__snake.head_coordinate[1] > self.__h:
            self.__snake.coordinates.pop(0)
            new_head_coordinate = (self.__snake.head_coordinate[0], 0)
            self.__snake.coordinates.insert(0, new_head_coordinate)
            self.__snake.head_coordinate = new_head_coordinate

        elif self.__snake.head_coordinate[1] < 0:
            self.__snake.coordinates.pop(0)
            new_head_coordinate = (self.__snake.head_coordinate[0], self.__h)
            self.__snake.coordinates.insert(0, new_head_coordinate)
            self.__snake.head_coordinate = new_head_coordinate

    def __snake_collides_itself(self) -> None:
        # ...
        if self.__snake.head_coordinate in self.__snake.coordinates[2:]:
            self.__running = False

    def __speed_up_snake(self):
        # ...
        if self.__direction == 'right':
            if (self.__snake.head_coordinate[0] <=
                    self.__mouse.x - self.__mouse.w * 2 or
                    self.__snake.head_coordinate[0] > self.__mouse.x):
                self.__snake.walk_in_coordinate_direction(self.__direction)

        elif self.__direction == 'left':
            if (self.__mouse.x <=
                    self.__snake.head_coordinate[0] - self.__mouse.w * 2 or
                    self.__mouse.x > self.__snake.head_coordinate[0]):
                self.__snake.walk_in_coordinate_direction(self.__direction)

        elif self.__direction == 'down':
            if (self.__snake.head_coordinate[1] <=
                    self.__mouse.y - self.__mouse.h * 2 or
                    self.__snake.head_coordinate[1] > self.__mouse.y):
                self.__snake.walk_in_coordinate_direction(self.__direction)

        elif self.__direction == 'up':
            if (self.__mouse.y <=
                    self.__snake.head_coordinate[1] - self.__mouse.h * 2 or
                    self.__mouse.y > self.__snake.head_coordinate[1]):
                self.__snake.walk_in_coordinate_direction(self.__direction)


if __name__ == '__main__':
    # s = Snake()
    # print(s.coordinates)
    #
    # m = Mouse(x=40)
    # print(m.coordinates)

    snake_game = SnakeGame()
    sys.exit(snake_game.run())
