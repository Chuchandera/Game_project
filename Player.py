import pygame
import math
from maps import *


class Player(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load('player/left_player_1.png').convert_alpha()
        self.rect = self.image.get_rect()

        self.base_speed = 10
        self.speed = self.base_speed
        self.what_anim = 0

        self.last_key = ''
        self.opposite_key = ''

        self.rect = self.image.get_rect()
        self.x_player = width // 2 - self.image.get_width() // 2
        self.y_player = height // 2 - self.image.get_height() // 2

        self.x_map = -96
        self.y_map = -96

        self.left_pose = [pygame.image.load(f'player/left_player_{i}.png').convert_alpha() for i in range(1, 9)]
        self.right_pose = [pygame.image.load(f'player/right_player_{i}.png').convert_alpha() for i in range(1, 9)]

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
        update_map_forplay(player, wall_sprites)

        for wall in wall_sprites:
            if pygame.sprite.collide_mask(self, wall):
                self.x_map, self.y_map = start_x, start_y

        self.speed = self.base_speed
        self.frame_counter += 1  # Увеличение счетчика кадров
        if self.frame_counter >= 10:  # Смена кадра анимации
            self.what_anim = (self.what_anim + 1) % len(self.side)
            self.frame_counter = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        self.image = pygame.image.load('player/shot.png').convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = 8
        self.direction = self.calculate_direction(start_pos, target_pos)

    def calculate_direction(self, start_pos, target_pos):
        self.x_con, self.y_con = player.get_map_coords()
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)
        if distance == 0:
            return (0, 0)
        return (dx / distance, dy / distance)

    def update(self):
        # x, y = player.get_map_coords()
        # self.x_con, self.y_con = x - self.x_con, y - self.y_con

        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        if (self.rect.x < 0 or self.rect.x > width or
                self.rect.y < 0 or self.rect.y > height):
            self.kill()

        for wall in wall_sprites:
            if pygame.sprite.collide_mask(self, wall):
                self.kill()

    @staticmethod
    def handle_input(event, bullets, bullet_counter, frame_counter, reload_frames, max_bullet):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if bullet_counter < max_bullet:
                    mouse_pos = pygame.mouse.get_pos()
                    start_pos = (width // 2, height // 2)
                    bullet = Bullet(start_pos, mouse_pos)
                    bullets.add(bullet)
                    return bullet_counter + 1, frame_counter
        if frame_counter >= reload_frames:
            return max(0, bullet_counter - 1), 0
        return bullet_counter, frame_counter + 1


class Wall(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = pygame.image.load('walls/wall.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


class Floor(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        self.image = pygame.image.load('walls/floor.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


def update_map_forplay(player, wall_sprites):
    wall_sprites.empty()

    map = get_map(1)
    x, y = player.get_map_coords()
    len_y, len_x = len(map), len(map[0])

    for y_map in range(len_y):
        for x_map in range(len_x):
            if -32 < y + y_map * 32 < height + 32 and -32 < x + x_map * 32 < width + 32:
                block = map[y_map][x_map]
                if block == 1:
                    Wall(wall_sprites, x + x_map * 32, y + y_map * 32)


def update_map(player, wall_sprites, background_sprites):
    wall_sprites.empty()
    background_sprites.empty()  # Очищаем группу стен перед отрисовкой

    map = get_map(1)
    x, y = player.get_map_coords()
    len_y, len_x = len(map), len(map[0])

    for y_map in range(len_y):
        for x_map in range(len_x):
            if -32 < y + y_map * 32 < height + 32 and -32 < x + x_map * 32 < width + 32:
                block = map[y_map][x_map]
                if block == 1:
                    Wall(wall_sprites, x + x_map * 32, y + y_map * 32)
                if block == 0:
                    Floor(background_sprites, x + x_map * 32, y + y_map * 32)


def draw_map(screen, wall_sprites, background_sprites):
    wall_sprites.draw(screen)
    background_sprites.draw(screen)


if __name__ == '__main__':
    pygame.init()  # Инициализация Pygame
    pygame.display.set_caption('Движение героя')  # Заголовок окна
    size = width, height = 800, 640  # Размеры окна
    screen = pygame.display.set_mode(size)  # Создание окна

    bullets = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    background_sprites = pygame.sprite.Group()

    player = Player(player_sprite)

    bullet_counter, frame_counter, reload_frames, max_bullet = 0, 0, 15, 5

    clock = pygame.time.Clock()  # Объект для управления временем
    running = True  # Флаг для основного цикла

    while running:  # Основной игровой цикл
        for event in pygame.event.get():  # Обработка событийa
            if event.type == pygame.QUIT:
                running = False
            all_sprites.update(event)
            bullet_counter, frame_counter = Bullet.handle_input(event, bullets, bullet_counter, frame_counter,
                                                                reload_frames, max_bullet)

        all_sprites.update()
        player_sprite.update()

        screen.fill((131, 241, 236))
        all_sprites.draw(screen)

        update_map(player, wall_sprites, background_sprites)
        draw_map(screen, wall_sprites, background_sprites)

        bullets.update()
        bullets.draw(screen)

        player_sprite.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
