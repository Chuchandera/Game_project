import pygame
import math
from board_class import *
import json

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = pygame.image.load('player/left_player_1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.is_moving = False
        self.base_speed = 5
        self.speed = self.base_speed
        self.what_anim = 0
        self.score = 0
        self.last_key = ''
        self.opposite_key = ''
        self.hp = 3
        self.rect = self.image.get_rect()
        self.x_player = width // 2 - self.image.get_width() // 2
        self.y_player = height // 2 - self.image.get_height() // 2

        self.left_pose = [pygame.image.load(f'player/left_player_{i}.png').convert_alpha() for i in range(1, 9)]
        self.right_pose = [pygame.image.load(f'player/right_player_{i}.png').convert_alpha() for i in range(1, 9)]

        self.side = self.left_pose
        self.frame_counter = 0
        self.mask = pygame.mask.from_surface(self.image)

    def get_player_coord(self):
        return self.x_player, self.y_player

    def update(self, *args, **kwargs):
        if not game_paused:
            global delta_x
            global delta_y
            global collision_x
            global collision_y
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
    @property
    def center(self):
        return (self.x_player + self.rect.width // 2, self.y_player + self.rect.height // 2)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos):
        super().__init__()
        self.image = pygame.image.load('player/shot.png').convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.speed = 15
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
        if not game_paused and not dead:
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed
            if not collision_x:
                self.rect.x += delta_x
            if not collision_y:
                self.rect.y += delta_y
            if (self.rect.x < 0 or self.rect.x > width or 
                    self.rect.y < 0 or self.rect.y > height):
                self.kill()
                return

            for wall in board.wall_sprites:
                if pygame.sprite.collide_mask(self, wall):
                    self.kill()

    @staticmethod
    def handle_input(event, bullets, bullet_counter, frame_counter, reload_frames, max_bullet, reloading):
        if not game_paused and not dead:
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

class Zombie(pygame.sprite.Sprite):
    def __init__(self, start_pos, player, board):
        super().__init__()
        self.original_image = pygame.image.load('player/image.png').convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (32, 32))
        self.rect = self.image.get_rect(topleft=start_pos)
        self.timer = 0
        if diff == 'Легко':
            self.speed = 3
            self.health = 2
        if diff == 'Нормально':
            self.speed = 4
            self.health = 3
        if diff == 'Сложно':
            self.speed = 6
            self.health = 4
        self.player = player
        self.board = board
        self.mask = pygame.mask.from_surface(self.image)
        self.detection_range = 600
        self.x = float(start_pos[0])
        self.y = float(start_pos[1])
        self.dx = 0
        self.dy = 0

    def update(self):
        if not game_paused and not dead:
            if not collision_x:
                self.rect.x += delta_x
            if not collision_y:
                self.rect.y += delta_y
            distance_to_player = math.hypot(self.player.center[0] - self.rect.centerx,
                                             self.player.center[1] - self.rect.centery)
            if distance_to_player <= self.detection_range and not self.is_path_blocked():
                self.chase()
            else:
                self.dx = 0
                self.dy = 0
            for bul in bullets:
                if self.rect.colliderect(bul.rect):
                    self.health -= 1
                    bul.kill()
            if self.rect.colliderect(player.rect):
                if self.timer >= 20:
                    player.hp -= 1
                    player.score -= 500
                    self.timer = 0
                    player_death_sound.play()
                else:
                    self.timer += 1
            if self.health == 0:
                zombie_agr_sound.stop()
                player.score += 1000
                self.kill()

    def is_path_blocked(self):
        x1, y1 = self.rect.center
        x2, y2 = self.player.center
        for i in range(1, 100):
            x = x1 + (x2 - x1) * i / 100
            y = y1 + (y2 - y1) * i / 100
            temp_rect = pygame.Rect(x - 1, y - 1, 2, 2)
            for wall in self.board.wall_sprites:
                if temp_rect.colliderect(wall.rect):
                    return True
        return False

    def chase(self):
        zombie_agr_sound.play()
        dx = self.player.center[0] - self.rect.centerx
        dy = self.player.center[1] - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance > 0:
            self.dx = dx / distance * self.speed
            self.dy = dy / distance * self.speed
        self.rect.x += self.dx
        self.rect.y += self.dy

    def get_pos(self):
        return self.x, self.y
    
def save_scores():
    try:
        x1, x2, x3 = load_scores()
        if level == 1:
            if player.score > x1:
                x1 = player.score
        if level == 2:
            if player.score > x2:
                x2 = player.score
        if level == 3:
            if player.score > x3:
                x3 = player.score
        settings = {
                "1": x1,
                "2": x2,
                "3": x3
            }
        with open('jsons/score.json', "w") as f:
            json.dump(settings, f)
    except Exception:
        print('Ошибка при загрузки в score.json файл')

def load_scores():
    try:
        with open('jsons/score.json', 'r') as f:
            settings = json.load(f)
            score_1 = settings.get("1", 0)
            score_2 = settings.get("2", 0)
            score_3 = settings.get("3", 0)
            return score_1, score_2, score_3
    except Exception as e:
        print("Ошибка при чтении файла score.json, использованы значения по умолчанию.")
    
def Start(lvl, difficulty, mus_volume, game_vol, index):
    pygame.init()
    global music_volume, game_volume, diff, width, steps_channel, height, board, shoot_sound, reload_sound, steps_sound, current_music_index, game_paused, screen, font, level, zombie_agr_sound, player_death_sound, time
    level = lvl
    time = 0
    MUSIC_FILES = ['music_data/Pantera - This Love (8 Bit).mp3',
                   'music_data/Pantera - Floods (8-Bit Version).mp3',
                   'music_data/Iron_Man_2022_8_Bit_Tribute_to_Black_Sabbath_8_Bit_Universe.mp3',
                   'music_data/G.O.A.T., Polyphia (8bit_ Cover).mp3',
                   'music_data/Deftones - My Own Summer (Shave It) (8 bit cover) by 8biTune.mp3']

    current_music_index = index
    music_volume = mus_volume
    game_volume = game_vol
    diff = difficulty
    pygame.mixer.set_num_channels(32)
    zombie_agr_sound = pygame.mixer.Sound('sounds/zombie.mp3')
    zombie_agr_sound.set_volume(game_volume * 0.2)
    reload_sound = pygame.mixer.Sound('sounds/reload.mp3')
    reload_sound.set_volume(game_volume)
    shoot_sound = pygame.mixer.Sound('sounds/shoot.mp3')
    shoot_sound.set_volume(game_volume * 0.3)
    pygame.mixer.Channel(1)
    steps_sound = pygame.mixer.Sound('sounds/footsteps.mp3')
    steps_sound.set_volume(game_volume)
    steps_channel = pygame.mixer.Channel(0)
    pygame.display.set_caption('Движение героя')
    player_death_sound = pygame.mixer.Sound('sounds/death.mp3')
    player_death_sound.set_volume(game_volume * 0.1)
    info = pygame.display.Info()
    width = info.current_w
    height = info.current_h
    screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN | pygame.NOFRAME)
    global deltak
    deltak = 1
    global player_sprite
    global bullets
    bullets = pygame.sprite.Group()
    player_sprite = pygame.sprite.Group()
    global player
    player = Player(player_sprite)
    board = Bullet.board = Board(level, screen, player.get_player_coord())
    if diff == 'Легко':
        max_bullet= 35
        deltak = 0.75
    if diff == 'Нормально':
        max_bullet = 25
        deltak = 1
    if diff == 'Сложно':
        max_bullet = 15
        deltak = 1.25
    Bullet.board.create_board()
    bullet_counter, frame_counter, reload_frames, reloading = 0, 0, 8, False
    clock = pygame.time.Clock()
    reload_timer = 0
    running = True
    font = pygame.font.Font(None, 36)
    game_paused = False

    def load_and_play_music():
        pygame.mixer.music.load(MUSIC_FILES[current_music_index])
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play()
    global zombie_group
    global dead
    dead = False
    global is_win
    is_win = False
    zombie_group = pygame.sprite.Group()
    for pos in board.zombie_spawn_points:
        zombie = Zombie(pos, player, board)
        zombie_group.add(zombie)
    load_and_play_music()
    deltaz = 0
    is_fr = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not dead and not is_win:
                    game_paused = not game_paused
                if event.key == pygame.K_p and dead and not is_win:
                    Start(lvl, difficulty, mus_volume, game_vol, index)
                if event.key == pygame.K_l and (game_paused or is_win):
                    from menu import main_menu
                    main_menu(current_music_index)
                if event.key == pygame.K_LSHIFT and not dead and not is_win:
                    player.base_speed += 2
                    player.speed += 2
            if event.type == pygame.KEYUP and not dead and not is_win:
                if event.key == pygame.K_LSHIFT:
                    player.base_speed -= 2
                    player.speed -= 2
            bullet_counter, frame_counter, reloading = Bullet.handle_input(event, bullets, bullet_counter, frame_counter,
                                                                            reload_frames, max_bullet, reloading)
        if not game_paused and not dead and not is_win:
            player_sprite.update()
            screen.fill((131, 241, 236))
            Bullet.board.draw_board()
            bullets.update()
            bullets.draw(screen)
            player_sprite.draw(screen)
            zombie_group.update()
            zombie_group.draw(screen)
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
            health_text = font.render(f"HP: {player.hp}", True, (255, 0, 0))
            screen.blit(health_text, (10, 10))
            health_text = font.render(f"Score: {player.score}", True, (255, 0, 0))
            screen.blit(health_text, (10, 30))
            text_surface = font.render(f"Патроны: {max_bullet - bullet_counter}", True, (255, 255, 255))
            text_rect = text_surface.get_rect(bottomright=(150, height - 10))
            screen.blit(text_surface, text_rect)
            if not player.hp == 0:
                time += 1
            if player.hp == 0:
                dead = True
                text_surface = font.render("Вы погибли! Нажмите P, чтобы начать заново", True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(width // 2, height // 2))
                screen.blit(text_surface, text_rect)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_P:
                            Start()
            if len(zombie_group) == 0:
                is_win = True
        elif game_paused:
            text_surface = font.render("Пауза (Нажмите Esc для продолжения или L, чтобы вернуться в меню)", True, (255, 255, 255))
            txt = font.render("Управление: ЛКМ - атака, R - перезарядка, WASD - управление, Shift - Бег",  True, (255, 255, 255))
            txt_rect = txt.get_rect(center=(width // 2, height // 2 + 100))
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            screen.blit(text_surface, text_rect)
            screen.blit(txt, txt_rect)
        elif is_win is True:
            if time <= 15 * 60:
                deltaz = 1.5
            elif time <= 20 * 60:
                deltaz = 1.25
            elif time <= 30 * 0:
                deltaz = 1
            else:
                deltaz = 0.75
            text_surface = font.render("Вы победили! Ваши очки записаны. Для возвращения в меню нажмите L)", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            screen.blit(text_surface, text_rect)
            if is_fr:
                player.score = int(player.score * deltak * deltaz)
                save_scores()
                is_fr = False
        pygame.display.flip()
        clock.tick(60)
        if not pygame.mixer.music.get_busy():
            current_music_index = (current_music_index + 1) % len(MUSIC_FILES)
            load_and_play_music()

    pygame.quit()


if __name__ == "__main__":
    Start(1, 'Легко', 0.5, 0.5, 3)