#!/usr/bin/env python3
import logging
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
        self.__texture_name_coordinates = {
            self.__coordinates[0]: 'head-down',
            self.__coordinates[1]: 'red-3-down',
            self.__coordinates[2]: 'tail-down'}

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

    @property
    def texture_name_coordinates(self) -> dict:
        return self.__texture_name_coordinates

    @texture_name_coordinates.setter
    def texture_name_coordinates(self, texture_name_coordinates: dict):
        self.__texture_name_coordinates = texture_name_coordinates

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

    def grow(self, coordinate: tuple) -> None:
        """Increases the size of the snake

        Adds a length item on snake front (on head) where the mouse was

        :param coordinate: x and y mouse coordinate tuple
        """
        pre_tail_name = self.__texture_name_coordinates[self.__coordinates[-2]]

        x, y = coordinate
        if self.__direction == 'up':
            y -= self.__h
        elif self.__direction == 'down':
            y += self.__h
        elif self.__direction == 'left':
            x -= self.__w
        elif self.__direction == 'right':
            x += self.__w

        if 'red-1' in pre_tail_name:
            pre_tail_name = f'black-1-{self.__direction}'
        elif 'red-2' in pre_tail_name:
            pre_tail_name = f'red-1-{self.__direction}'
        elif 'red-3' in pre_tail_name:
            pre_tail_name = f'red-2-{self.__direction}'
        elif 'black-1' in pre_tail_name:
            pre_tail_name = f'black-2-{self.__direction}'
        elif 'black-2' in pre_tail_name:
            pre_tail_name = f'red-3-{self.__direction}'

        self.__texture_name_coordinates[self.__coordinates[-1]] = pre_tail_name

        self.__coordinates.append((x, y))
        self.__texture_name_coordinates[(x, y)] = f'tail-{self.__direction}'

    def reset(self) -> None:
        """..."""
        self.__direction = 'down'
        self.__coordinates = [
            (self.__x, self.__y + self.__h * 2),
            (self.__x, self.__y + self.__h),
            (self.__x, self.__y)]
        self.__texture_name_coordinates = {
            self.__coordinates[0]: 'head-down',
            self.__coordinates[1]: 'red-3-down',
            self.__coordinates[2]: 'tail-down'}

    def walk_in_coordinate_direction(self, direction: str) -> None:
        """..."""
        x, y = self.__coordinates[0]
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

        self.__coordinates.insert(0, (x, y))
        self.__coordinates.pop()
        # self.__coordinates = self.__coordinates[:-1]

        textures = [tex for tex in self.__texture_name_coordinates.values()]
        texture_name_coordinates = {}
        for coordinate, texture in zip(self.__coordinates, textures):
            texture_name_coordinates[coordinate] = texture

        there_was_a_thread_cut = False
        for xy in self.__coordinates:
            if xy not in texture_name_coordinates:
                texture_name_coordinates[xy] = f'red-1-{self.__direction}'
                logging.warning('Thread cut')
                there_was_a_thread_cut = True

        if there_was_a_thread_cut:
            for xy in self.__coordinates:
                if 'tail' in texture_name_coordinates[xy]:
                    texture_name_coordinates[xy] = f'red-1-{self.__direction}'

                texture_name_coordinates[self.__coordinates[-1]] = (
                    f'tail-{self.__direction}')

        self.__texture_name_coordinates = texture_name_coordinates

    def texture_name_coordinates_thread_cut(
            self, texture_name_coordinates: dict) -> dict:
        pass


class SnakeSprites(pygame.sprite.Sprite):
    def __init__(self, game_path, layer):
        super().__init__()
        self.__sprites_path = os.path.join(game_path, 'resources', 'sprites')
        self.__sprites = {}

        for filename in os.listdir(self.__sprites_path):
            sprite = pygame.image.load(
                os.path.join(self.__sprites_path, filename))
            self.__sprites[filename[:-4]] = sprite

        self.image = self.__sprites['head-down']
        self.rect = self.image.get_rect()
        self._layer = layer

    def set_texture(self, texture_name: str) -> None:
        """..."""
        for i in ['red-1', 'red-2', 'red-3']:
            texture_name = texture_name.replace(i, 'red')
        self.image = self.__sprites[texture_name]

    def set_coordinate(self, coordinate: tuple):
        """..."""
        self.rect.topleft = coordinate


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

    def raffle_new_coordinates(self, area: tuple, snake: Snake) -> None:
        """Updates the x and y coordinates

        Coordinates where the mouse will be drawn
        """
        coordinate = None
        count = 0
        while count < area[0] * area[1] - len(snake.coordinates):
            count += 1
            coordinate = (
                random.randrange(self.__w, area[0] - self.__w, self.__w),
                random.randrange(self.__h, area[1] - self.__h, self.__h))
            if coordinate not in snake.coordinates:
                break

        self.__coordinates = [coordinate]
        self.__x, self.__y = self.__coordinates[0]


class MouseSprites(pygame.sprite.Sprite):
    def __init__(self, game_path, layer):
        super().__init__()
        self.__sprites_path = os.path.join(game_path, 'resources', 'sprites')
        self.__sprites = {}

        for filename in os.listdir(self.__sprites_path):
            sprite = pygame.image.load(
                os.path.join(self.__sprites_path, filename))
            self.__sprites[filename[:-4]] = sprite

        self.image = self.__sprites['mouse-1']
        self.rect = self.image.get_rect()
        self._layer = layer

    def set_new_sprite(self) -> None:
        """..."""
        self.image = self.__sprites[f'mouse-{random.randint(1, 4)}']

    def set_coordinate(self, coordinate: tuple):
        """..."""
        self.rect.topleft = coordinate


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

        self.__window_icon = pygame.image.load(os.path.join(
            self.__game_path, 'resources', 'coral-snake-game.png'))
        pygame.display.set_icon(self.__window_icon)

        self.__font_url = os.path.join(
            self.__game_path, 'resources', 'amaticsc-bold.ttf')
        self.__score_font = pygame.font.Font(self.__font_url, 25)
        # self.__score_font = pygame.font.SysFont('arial', 15, False, False)

        self.__screen = pygame.display.set_mode((self.__w, self.__h))
        self.__background = pygame.image.load(
            os.path.join(self.__game_path, 'resources', 'background.jpg'))

        # self.__sprite_group = pygame.sprite.Group()
        self.__sprite_group = pygame.sprite.LayeredUpdates()

        self.__mouse = Mouse(
            x=random.randrange(20, self.__w - 20, 20),
            y=random.randrange(20, self.__h - 20, 20),
            w=20, h=20)

        self.__mouse_sprites = MouseSprites(self.__game_path, 0)
        self.__sprite_group.add(self.__mouse_sprites)

        self.__snake = Snake(x=self.__w // 2 - 20, y=20, w=20, h=20)
        self.__snake_eating_mouse_sound = pygame.mixer.Sound(
            # https://themushroomkingdom.net/media/smw/wav
            os.path.join(self.__game_path, 'resources', 'smw_kick.wav'))
        self.__snake_sprites = SnakeSprites(self.__game_path, 1)
        self.__sprite_group.add(self.__snake_sprites)

        self.__running = True
        self.__end_game = False
        self.__pause_game = False

        self.__clock = pygame.time.Clock()
        self.__clock_tick = 5

        self.__direction = 'down'
        self.__direction_coordinates = {}
        self.__direction_bend_coordinates = {}

        self.__can_walk = False
        self.__scores = 0

    def run(self) -> int:
        """..."""
        while self.__running:
            self.__clock.tick(self.__clock_tick)
            # self.__screen.fill((110, 160, 120))

            self.__handle_keyboard_keys_event()

            if self.__end_game:
                self.__draw_end_screen()

            elif not self.__pause_game:
                self.__handle_characters_state()
                self.__draw()
            pygame.display.flip()
        return 0

    def __draw(self) -> None:
        # ...
        # pygame.draw.circle(screen, (0, 0, 100), (300, 260), 40)
        # pygame.draw.line(screen, (0, 0, 100), (390, 0), (390, 600), 5)
        self.__screen.blit(self.__background, (0, 0))

        if self.__mouse.coordinates[0] == self.__snake.coordinates[0]:
            self.__mouse_sprites.set_coordinate((1000, 1000))
        else:
            self.__mouse_sprites.set_coordinate(self.__mouse.coordinates[0])

        for coordinate in self.__snake.coordinates:
            self.__snake_sprites.set_coordinate(coordinate)
            texture_name = self.__texture_name_by_coordinate(coordinate)
            if texture_name:
                self.__snake_sprites.set_texture(texture_name)

            self.__sprite_group.draw(self.__screen)

        self.__screen.blit(
            self.__score_font.render(
                str(self.__scores), True, (255, 255, 255)),
            (5, -5))
        self.__sprite_group.update()
        self.__can_walk = True

    def __draw_end_screen(self) -> None:
        # ...
        self.__screen.blit(self.__background, (0, 0))

        font = pygame.font.Font(self.__font_url, 100)
        self.__screen.blit(
            font.render('End Game!', True, (255, 255, 255)),
            (self.__w // 2 - 130, 50))

        txt = f'Scores: {self.__scores}'
        font = pygame.font.Font(self.__font_url, 40)
        self.__screen.blit(
            font.render(txt, True, (255, 255, 255)), (50, 180))

        txt = "Press key 'ENTER' to play again"
        font = pygame.font.Font(self.__font_url, 50)
        self.__screen.blit(
            font.render(txt, True, (255, 255, 255)), (50, 250))

    def __handle_characters_state(self) -> None:
        # ...
        self.__snake_eat_the_mouse()
        self.__snake_appears_on_inverse_screen_side()
        self.__snake_collides_itself()
        self.__snake.walk_in_coordinate_direction(self.__direction)
        self.__register_coordinate_direction()

    def __handle_keyboard_keys_event(self) -> None:
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
                if event.key == K_SPACE:
                    if self.__running and self.__end_game:
                        if self.__pause_game:
                            self.__pause_game = False
                        else:
                            self.__pause_game = True

                elif event.key == K_ESCAPE:
                    self.__running = False

                elif event.key == K_RETURN:
                    if self.__end_game:
                        self.__end_game = False
                        self.__restart_game()

                if event.key in keys:
                    if keys[event.key] == self.__direction:
                        self.__speed_up_snake()

                    if keys[event.key] != opposite_direction[self.__direction]:
                        if self.__can_walk:
                            if keys[event.key] != self.__direction:
                                self.__register_bend_coordinate_direction(
                                    self.__direction, keys[event.key])

                            self.__direction = keys[event.key]
                            self.__can_walk = False

    def __register_bend_coordinate_direction(
            self, old_direction: str, new_direction: str) -> None:
        # ...
        self.__direction_bend_coordinates[self.__snake.coordinates[0]] = (
            f'bend-{old_direction}-to-{new_direction}')

    def __register_coordinate_direction(self) -> None:
        # ...
        if self.__snake.coordinates[0] in self.__direction_bend_coordinates:
            self.__direction_bend_coordinates.pop(self.__snake.coordinates[0])

        self.__direction_coordinates[self.__snake.coordinates[0]] = (
            self.__direction)

    def __restart_game(self) -> None:
        self.__screen.fill(pygame.Color('black'))
        self.__snake.reset()
        self.__scores = 0

    def __snake_eat_the_mouse(self) -> None:
        # ...
        if self.__snake.coordinates[0] == self.__mouse.coordinates[0]:
            self.__mouse.raffle_new_coordinates(
                (self.__w, self.__h), self.__snake)
            self.__mouse_sprites.set_new_sprite()
            self.__snake.grow(self.__mouse.coordinates[0])
            self.__snake_eating_mouse_sound.play()
            self.__scores += 1
            self.__scores_info = f'Scores: {self.__scores}'

    def __snake_appears_on_inverse_screen_side(self) -> None:
        # ...
        if self.__snake.coordinates[0][0] > self.__w:
            new_head_coordinate = (0, self.__snake.coordinates[0][1])
            self.__snake.coordinates[0] = new_head_coordinate

        elif self.__snake.coordinates[0][0] < 0:
            new_head_coordinate = (self.__w, self.__snake.coordinates[0][1])
            self.__snake.coordinates[0] = new_head_coordinate

        elif self.__snake.coordinates[0][1] > self.__h:
            new_head_coordinate = (self.__snake.coordinates[0][0], 0)
            self.__snake.coordinates[0] = new_head_coordinate

        elif self.__snake.coordinates[0][1] < 0:
            new_head_coordinate = (self.__snake.coordinates[0][0], self.__h)
            self.__snake.coordinates[0] = new_head_coordinate

    def __snake_collides_itself(self) -> None:
        # ...
        if self.__snake.coordinates[0] in self.__snake.coordinates[2:]:
            self.__end_game = True
            # self.__running = False

    def __speed_up_snake(self) -> None:
        # ...
        can_walk = False
        if self.__direction == 'right':
            if (self.__snake.coordinates[0][0] <=
                    self.__mouse.x - self.__mouse.w * 2 or
                    self.__snake.coordinates[0][0] > self.__mouse.x):
                can_walk = True

        elif self.__direction == 'left':
            if (self.__mouse.x <=
                    self.__snake.coordinates[0][0] - self.__mouse.w * 2 or
                    self.__mouse.x > self.__snake.coordinates[0][0]):
                can_walk = True

        elif self.__direction == 'down':
            if (self.__snake.coordinates[0][1] <=
                    self.__mouse.y - self.__mouse.h * 2 or
                    self.__snake.coordinates[0][1] > self.__mouse.y):
                can_walk = True

        elif self.__direction == 'up':
            if (self.__mouse.y <=
                    self.__snake.coordinates[0][1] - self.__mouse.h * 2 or
                    self.__mouse.y > self.__snake.coordinates[0][1]):
                can_walk = True

        if can_walk:
            self.__snake.walk_in_coordinate_direction(self.__direction)
            self.__register_coordinate_direction()

    def __texture_name_by_coordinate(self, coordinate: tuple) -> str:
        # ...
        texture_name = self.__snake.texture_name_coordinates[coordinate]

        if coordinate in self.__direction_bend_coordinates:
            direction = self.__direction_bend_coordinates[coordinate]
            if 'head' not in texture_name:  # 'tail' not in texture_name and
                if direction not in texture_name:
                    for d in ['left', 'right', 'up', 'down']:
                        if d in texture_name:
                            texture_name = texture_name.replace(d, direction)
                            break

        elif coordinate in self.__direction_coordinates:
            direction = self.__direction_coordinates[coordinate]

            if direction not in texture_name:
                for d in ['left', 'right', 'up', 'down']:
                    if d in texture_name:
                        texture_name = texture_name.replace(d, direction)
                        break
        return texture_name


if __name__ == '__main__':
    snake_game = SnakeGame()
    sys.exit(snake_game.run())
