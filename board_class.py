import pygame
import math
import sys
from maps import *


class Board:
    def __init__(self, map_number, screen, player_coordinates):

        self.board_screen = screen

        self.board, x, y = get_map(map_number)
        self.board_len_y, self.board_len_x = len(self.board), len(self.board[0])

        self.left = player_coordinates[0] + x
        self.top = player_coordinates[1] + y

        self.cell_size = 32
        self.wall_sprites = pygame.sprite.Group()
        self.board_sprites = pygame.sprite.Group()

    # настройка внешнего вида
    def set_view(self, left, top):
        self.left = left
        self.top = top

    def get_map_coords(self):
        return self.left, self.top

    def create_board(self):
        x, y = self.left, self.top
        for y_map in range(self.board_len_y):
            for x_map in range(self.board_len_x):
                block = self.board[y_map][x_map]
                if block == 1:
                    Wall(self.wall_sprites, x + x_map * 32, y + y_map * 32)
                elif block == 0:
                    Floor(self.board_sprites, x + x_map * 32, y + y_map * 32)

    def update_board(self, delta_x, delta_y):
        self.set_view(self.left + delta_x, self.top + delta_y)
        # print(self.left, self.top)
        for cube in self.wall_sprites:
            cube.change_coords(delta_x, delta_y)
        for cube in self.board_sprites:
            cube.change_coords(delta_x, delta_y)

    def draw_board(self):
        self.wall_sprites.draw(self.board_screen)
        self.board_sprites.draw(self.board_screen)


class Wall(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.x, self.y = x, y
        self.image = pygame.image.load('walls/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def change_coords(self, delta_x, delta_y):
        self.x, self.y = self.x + delta_x, self.y + delta_y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


class Floor(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.x, self.y = x, y
        self.image = pygame.image.load('walls/floor.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def change_coords(self, delta_x, delta_y):
        self.x, self.y = self.x + delta_x, self.y + delta_y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
