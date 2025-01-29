import pygame


class Player(pygame.sprite.Sprite):
    image = pygame.image.load('player/left_player_1.png')

    def __init__(self, group):
        super().__init__(group)

        self.base_speed = 3
        self.speed = self.base_speed
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
        self.mask = pygame.mask.from_surface(self.image)

    def get_map_coords(self):
        return self.x_map, self.y_map

    def update(self, *args, **kwargs):
        self.image = self.side[self.what_anim]
        self.rect.topleft = (self.x_player, self.y_player)

        start_x, start_y = self.x_map, self.y_map
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_map += self.speed
            self.side = self.left_pose
            self.last_key = 'a'
        if keys[pygame.K_d]:
            self.x_map -= self.speed
            self.side = self.right_pose
            self.last_key = 'd'
        if keys[pygame.K_w]:
            self.y_map += self.speed
            self.last_key = 'w'
        if keys[pygame.K_s]:
            self.y_map -= self.speed
            self.last_key = 's'

        global wall_sprites
        update_map(player, wall_sprites)

        for wall in wall_sprites:
            if pygame.sprite.collide_mask(self, wall):
                self.x_map, self.y_map = start_x, start_y

        self.speed = self.base_speed
        self.frame_counter += 1  # Увеличение счетчика кадров
        if self.frame_counter >= 10:  # Смена кадра анимации
            self.what_anim = (self.what_anim + 1) % len(self.side)
            self.frame_counter = 0


class Wall(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = pygame.image.load('walls/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


def update_map(player, wall_sprites):
    wall_sprites.empty()  # Очищаем группу стен перед отрисовкой

    map = get_map(1)
    x, y = player.get_map_coords()
    len_y, len_x = len(map), len(map[0])

    for y_map in range(len_y):
        for x_map in range(len_x):
            if -32 < y + y_map * 30 < height + 32 and -32 < x + x_map * 30 < width + 32:
                if map[y_map][x_map] == 1:
                    Wall(wall_sprites, x + x_map * 30, y + y_map * 30)


def draw_map(screen, wall_sprites):
    wall_sprites.draw(screen)









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

        update_map(player, wall_sprites)
        draw_map(screen, wall_sprites)

        wall_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(120)

    pygame.quit()
