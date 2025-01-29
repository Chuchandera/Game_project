import pygame


# def opposite(a):
#     if a == 'a':
#         return 'd'
#     elif a == 'd':
#         return 'a'
#     elif a == 'w':
#         return 's'
#     elif a == 's':
#         return 'w'


class Player(pygame.sprite.Sprite):
    image = pygame.image.load('player/left_player_1.png')
    key_a_pressed, key_d_pressed, key_w_pressed, key_s_pressed = False, False, False, False

    def __init__(self, group):
        super().__init__(group)

        self.speed = 3
        self.what_anim = 0

        self.last_key = ''
        self.opposite_key = ''

        self.image = Player.image
        self.rect = self.image.get_rect()
        self.x_player = width // 2 - self.image.get_width() // 2
        self.y_player = height // 2 - self.image.get_height() // 2

        self.x_map = -96
        self.y_map = -96
        self.left_pose = [
            pygame.image.load('player/left_player_1.png').convert_alpha(),
            pygame.image.load('player/left_player_2.png').convert_alpha(),
            pygame.image.load('player/left_player_3.png').convert_alpha(),
            pygame.image.load('player/left_player_4.png').convert_alpha(),
            pygame.image.load('player/left_player_5.png').convert_alpha(),
            pygame.image.load('player/left_player_6.png').convert_alpha(),
            pygame.image.load('player/left_player_7.png').convert_alpha(),
            pygame.image.load('player/left_player_8.png').convert_alpha()
        ]

        self.right_pose = [
            pygame.image.load('player/right_player_1.png').convert_alpha(),
            pygame.image.load('player/right_player_2.png').convert_alpha(),
            pygame.image.load('player/right_player_3.png').convert_alpha(),
            pygame.image.load('player/right_player_4.png').convert_alpha(),
            pygame.image.load('player/right_player_5.png').convert_alpha(),
            pygame.image.load('player/right_player_6.png').convert_alpha(),
            pygame.image.load('player/right_player_7.png').convert_alpha(),
            pygame.image.load('player/right_player_8.png').convert_alpha()
        ]
        self.side = self.left_pose
        self.frame_counter = 0

    def get_map_coords(self):
        return self.x_map, self.y_map

    def update(self, *args, **kwargs):
        self.image = self.side[self.what_anim]
        self.rect.topleft = (self.x_player, self.y_player)

        if pygame.sprite.spritecollideany(self, wall_sprites):
            self.speed = 0


        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_map += self.speed
            self.side = self.left_pose
            self.last_key = 'a'
            # self.opposite_key = opposite(self.last_key)
        if keys[pygame.K_d]:
            self.x_map -= self.speed
            self.side = self.right_pose
            self.last_key = 'd'
            # self.opposite_key = opposite(self.last_key)
        if keys[pygame.K_w]:
            self.y_map += self.speed
            self.last_key = 'w'
            # self.opposite_key = opposite(self.last_key)
        if keys[pygame.K_s]:
            self.y_map -= self.speed
            self.last_key = 's'
            # self.opposite_key = opposite(self.last_key)

        self.frame_counter += 1  # Увеличение счетчика кадров
        if self.frame_counter >= 10:  # Смена кадра анимации
            self.what_anim = (self.what_anim + 1) % len(self.side)
            self.frame_counter = 0


class Wall(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = pygame.image.load('walls/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        # self.mask = pygame.mask.from_surface(self.image)


import math
from maps import *

if __name__ == '__main__':
    pygame.init()  # Инициализация Pygame
    pygame.display.set_caption('Движение героя')  # Заголовок окна
    size = width, height = 800, 640  # Размеры окна
    screen = pygame.display.set_mode(size)  # Создание окна

    all_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()

    player = Player(all_sprites)

    clock = pygame.time.Clock()  # Объект для управления временем
    running = True  # Флаг для основного цикла

    while running:  # Основной игровой цикл
        for event in pygame.event.get():  # Обработка событийa
            if event.type == pygame.QUIT:
                running = False
            all_sprites.update(event)

        # Движение персонажа

        all_sprites.update()
        screen.fill((131, 241, 236))
        all_sprites.draw(screen)

        wall_sprites = pygame.sprite.Group()

        map = get_map(1)
        x, y = player.get_map_coords()
        len_y, len_x = len(map), len(map[0])
        wall = pygame.image.load('walls/wall.png')
        for y_map in range(len_y):
            for x_map in range(len_x):
                if -32 < y + y_map * 30 < height + 32 and -32 < x + x_map * 30 < width + 32:
                    if map[y_map][x_map] == 1:
                        wall = Wall(wall_sprites, x + x_map * 30, y + y_map * 30)

        # wall_sprites.update()
        wall_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(60)  # Ограничение FPS

    pygame.quit()  # Завершение работы Pygame```
