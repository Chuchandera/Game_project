import pygame
import math
from board_class import *

class Player(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load('player/left_player_1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.is_moving = False
        self.base_speed = 5
        self.speed = self.base_speed
        self.what_anim = 0

        self.last_key = ''
        self.opposite_key = ''

        self.rect = self.image.get_rect()
        self.x_player = width // 2 - self.image.get_width() // 2
        self.y_player = height // 2 - self.image.get_height() // 2

        self.left_pose = [pygame.image.load(f'player/left_player_{i}.png').convert_alpha() for i in range(1, 9)]
        self.right_pose = [pygame.image.load(f'player/right_player_{i}.png').convert_alpha() for i in range(1, 9)]

        self.side = self.left_pose
        self.frame_counter = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, *args, **kwargs):
        if not game_paused:
            self.image = self.side[self.what_anim]
            self.rect.topleft = (self.x_player, self.y_player)
            self.is_moving = False
            delta_x, delta_y = 0, 0
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                delta_x = self.speed
                self.side = self.left_pose
                self.is_moving = True
            if keys[pygame.K_d]:
                delta_x = - self.speed
                self.side = self.right_pose
                self.is_moving = True
            if keys[pygame.K_w]:
                delta_y = self.speed
                self.is_moving = True
            if keys[pygame.K_s]:
                delta_y = -self.speed
                self.is_moving = True

            temp_delta_x = delta_x
            temp_delta_y = delta_y
            board.update_board(temp_delta_x, 0)
            collision_x = False
            for wall in board.wall_sprites:
                if pygame.sprite.collide_mask(self, wall):
                    collision_x = True
                    break
            if collision_x:
                board.update_board(-temp_delta_x, 0)
                temp_delta_x = 0

            board.update_board(0, temp_delta_y)
            collision_y = False
            for wall in board.wall_sprites:
                if pygame.sprite.collide_mask(self, wall):
                    collision_y = True
                    break

            if collision_y:
                board.update_board(0, -temp_delta_y)
                temp_delta_y = 0
            if self.is_moving and steps_sound and not steps_channel.get_busy(): 
                steps_sound.play()
            elif not self.is_moving and steps_sound: 
                steps_sound.stop()
            self.speed = self.base_speed
            self.frame_counter += 1
            if self.frame_counter >= 10:
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
        self.x_con, self.y_con = board.get_map_coords() 
        dx = target_pos[0] - start_pos[0]
        dy = target_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)
        if distance == 0:
            return (0, 0)
        return (dx / distance, dy / distance)

    def update(self):
        if not game_paused:
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed
            if (self.rect.x < 0 or self.rect.x > width or 
                    self.rect.y < 0 or self.rect.y > height):
                self.kill()
                return

            for wall in board.wall_sprites:
                if pygame.sprite.collide_mask(self, wall):
                    self.kill()

    @staticmethod
    def handle_input(event, bullets, bullet_counter, frame_counter, reload_frames, max_bullet, reloading):
        if not game_paused:
            if event.type == pygame.MOUSEBUTTONDOWN and not reloading:
                    if bullet_counter < max_bullet:
                        mouse_pos = pygame.mouse.get_pos()
                        start_pos = (width // 2, height // 2)
                        bullet = Bullet(start_pos, mouse_pos)
                        bullets.add(bullet)
                        shoot_sound.play()
                        return bullet_counter + 1, frame_counter, reloading 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                return bullet_counter, frame_counter, True
        return bullet_counter, frame_counter, reloading


def Start(difficulty, mus_volume, game_vol, index):
    pygame.init()
    global music_volume, game_volume, diff, width, steps_channel, height, board, shoot_sound, reload_sound, steps_sound, current_music_index, game_paused, screen, font
    MUSIC_FILES = ['music_data/Pantera - This Love (8 Bit).mp3',
                   'music_data/Pantera - Floods (8-Bit Version).mp3',
                   'music_data/Iron_Man_2022_8_Bit_Tribute_to_Black_Sabbath_8_Bit_Universe.mp3',
                   'music_data/G.O.A.T., Polyphia (8bit_ Cover).mp3',
                   'music_data/Deftones - My Own Summer (Shave It) (8 bit cover) by 8biTune.mp3']

    current_music_index = index
    music_volume = mus_volume
    game_volume = game_vol
    diff = difficulty
    reload_sound = pygame.mixer.Sound('sounds/reload.mp3')
    reload_sound.set_volume(game_volume)
    shoot_sound = pygame.mixer.Sound('sounds/shoot.mp3')
    shoot_sound.set_volume(game_volume * 0.3)
    steps_sound = pygame.mixer.Sound('sounds/footsteps.mp3')
    steps_sound.set_volume(game_volume)
    steps_channel = pygame.mixer.Channel(0)
    pygame.display.set_caption('Движение героя')
    info = pygame.display.Info()
    width = info.current_w
    height = info.current_h
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.NOFRAME)
    global player_sprite
    global bullets
    bullets = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    global player
    player = Player(player_sprite)
    board = Bullet.board = Board(1, screen, -100, -100)
    Bullet.board.create_board()
    bullet_counter, frame_counter, reload_frames, max_bullet, reloading = 0, 0, 8, 45, False
    clock = pygame.time.Clock()
    reload_timer = 0
    running = True
    font = pygame.font.Font(None, 36)

    game_paused = False

    def load_and_play_music():
        pygame.mixer.music.load(MUSIC_FILES[current_music_index])
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play()

    load_and_play_music()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_paused = not game_paused
                    print(f"game_paused: {game_paused}")
            bullet_counter, frame_counter, reloading = Bullet.handle_input(event, bullets, bullet_counter, frame_counter,
                                                                            reload_frames, max_bullet, reloading)

        if not game_paused:
            player_sprite.update()
            screen.fill((131, 241, 236))
            Bullet.board.draw_board()
            bullets.update()
            bullets.draw(screen)
            player_sprite.draw(screen)

            # Обработка перезарядки
            if reloading:
                reload_timer += 1
                if reload_timer == 1:
                    if reload_sound:
                        reload_sound.stop()
                        reload_sound.play()
                if reload_timer >= reload_frames * 8:
                    reloading = False
                    reload_timer = 0
                    bullet_counter = 0
                    pygame.time.delay(5)

            # Отрисовка HUD (количество патронов)
            text_surface = font.render(f"Патроны: {max_bullet - bullet_counter}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(bottomright=(150, height - 10))
            screen.blit(text_surface, text_rect)
        else:
            text_surface = font.render("Пауза (Нажмите Esc для продолжения)", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        clock.tick(60)
        if not pygame.mixer.music.get_busy():
            current_music_index = (current_music_index + 1) % len(MUSIC_FILES)
            load_and_play_music()

    pygame.quit()