import pygame
import random
import sys
import json

pygame.init()
pygame.mixer.init()
SCREEN_WIDTH = 0
SCREEN_HEIGHT = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
BACKGROUND_IMAGES = ['menubacks/backmenu1.png', 'menubacks/backmenu2.png', 'menubacks/backmenu3.png', 'menubacks/backmenu4.png', 'menubacks/backmenu5.png', 'menubacks/backmenu6.png']
MUSIC_FILES = ['music_data/Pantera - This Love (8 Bit).mp3',
               'music_data/Pantera - Floods (8-Bit Version).mp3',
               'music_data/Iron_Man_2022_8_Bit_Tribute_to_Black_Sabbath_8_Bit_Universe.mp3',
               'music_data/G.O.A.T., Polyphia (8bit_ Cover).mp3',
               'music_data/Deftones - My Own Summer (Shave It) (8 bit cover) by 8biTune.mp3']
current_music_index = 0
music_volume = 0.2
game_volume = 0.6
difficulty = "Легко"
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.NOFRAME)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_width(), screen.get_height()
SETTINGS_FILE = "jsons/settings.json"
SCORES_FILE = "jsons/score.json"


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action=None, action_arg=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.action_arg = action_arg
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.action:
                if self.action_arg is not None:
                    self.action(self.action_arg)
                else:
                    self.action()


def draw_text(screen, text, font, color, x, y, align="center"):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    if align == "left":
        text_rect.midleft = (x, y)
    elif align == "right":
        text_rect.midright = (x, y)
    screen.blit(text_surface, text_rect)

def load_scores():
    try:
        with open(SCORES_FILE, 'r') as f:
            settings = json.load(f)
            score_1 = settings.get("1", 0)
            score_2 = settings.get("2", 0)
            score_3 = settings.get("3", 0)
            return score_1, score_2, score_3
    except Exception as e:
        print("Ошибка при чтении файла score.json, использованы значения по умолчанию.")
        return 0, 0, 0

def game(level):
    pygame.mixer.music.stop()
    from Player import Start
    Start(level, difficulty, music_volume, game_volume, current_music_index)
    pygame.quit()
    sys.exit()

def show_level_selection():
    global show_level_selection_flag
    show_level_selection_flag = True
    level1_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 50, "Уровень 1", WHITE, LIGHT_BLUE, game, 1)
    level2_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2, 200, 50, "Уровень 2", WHITE, LIGHT_BLUE, game, 2)
    level3_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100, 200, 50, "Уровень 3", WHITE, LIGHT_BLUE, game, 3)
    back_button = Button(50, 50, 100, 40, "Назад", WHITE, LIGHT_BLUE, lambda: setattr(show_level_selection, 'running', False))

    show_level_selection.running = True
    score_1, score_2, score_3 = load_scores()
    while show_level_selection.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            level1_button.handle_event(event)
            level2_button.handle_event(event)
            level3_button.handle_event(event)
            back_button.handle_event(event)

        screen.blit(background_image, (bg_x, 0))

        draw_text(screen, "Выберите уровень", pygame.font.Font(None, 60), WHITE, SCREEN_WIDTH // 2, 200)

        level1_button.draw(screen)
        level2_button.draw(screen)
        level3_button.draw(screen)

        font = pygame.font.Font(None, 36)
        draw_text(screen, f"Ваши очки: {score_1}", font, WHITE, level1_button.rect.right + 150, level1_button.rect.centery, align="left")
        draw_text(screen, f"Ваши очки: {score_2}", font, WHITE, level2_button.rect.right + 150, level2_button.rect.centery, align="left")
        draw_text(screen, f"Ваши очки: {score_3}", font, WHITE, level3_button.rect.right + 150, level3_button.rect.centery, align="left")
        back_button.draw(screen)

        pygame.display.flip()

def options():
    global music_volume, game_volume, difficulty, show_save_message, save_message_start_time, bg_x, bg_direction
    slider_width = 200
    music_slider_x = SCREEN_WIDTH // 2 - slider_width // 2
    game_slider_x = SCREEN_WIDTH // 2 - slider_width // 2
    back_button = Button(50, 50, 100, 40, "Назад", WHITE, LIGHT_BLUE, lambda: setattr(options, 'running', False)) #Кнопка назад теперь белая
    difficulties = ["Легко", "Нормально", "Сложно"]

    def change_difficulty():
        global difficulty
        current_index = difficulties.index(difficulty)
        next_index = (current_index + 1) % len(difficulties)
        difficulty = difficulties[next_index]
        difficulty_button.text = f"Сложность: {difficulty}"

    def save_settings():
        global music_volume, game_volume, difficulty, show_save_message, save_message_start_time
        settings = {
            "music_volume": music_volume,
            "game_volume": game_volume,
            "difficulty": difficulty
        }
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f)
        show_save_message = True
        save_message_start_time = pygame.time.get_ticks()
    difficulty_button = Button(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 3 + 100, 220, 40, f"Сложность: {difficulty}", WHITE, LIGHT_BLUE, change_difficulty)
    difficulty_button.font = pygame.font.Font(None, 28)
    save_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 3 + 200, 200, 40, "Сохранить", WHITE, LIGHT_BLUE, save_settings)
    font = pygame.font.Font(None, 36)
    options.running = True
    bg_speed = 0.05
    bg_range = 2
    while options.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            back_button.handle_event(event)
            save_button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if music_slider_x <= event.pos[0] <= music_slider_x + slider_width and SCREEN_HEIGHT // 3 - 10 <= event.pos[1] <= SCREEN_HEIGHT // 3 + 10:
                        music_volume = (event.pos[0] - music_slider_x) / slider_width
                        music_volume = max(0, min(music_volume, 1))
                        pygame.mixer.music.set_volume(music_volume)

                    if game_slider_x <= event.pos[0] <= game_slider_x + slider_width and SCREEN_HEIGHT // 3 - 10 + 50 <= event.pos[1] <= SCREEN_HEIGHT // 3 + 10 + 50:
                        game_volume = (event.pos[0] - game_slider_x) / slider_width
                        game_volume = max(0, min(game_volume, 1))
            difficulty_button.handle_event(event)
        bg_x += bg_speed * bg_direction
        if bg_x > bg_range:
            bg_direction = -1
        elif bg_x < -bg_range:
            bg_direction = 1
        screen.blit(background_image, (bg_x, 0))
        draw_text(screen, "Настройки", pygame.font.Font(None, 60), WHITE, SCREEN_WIDTH // 2, 100)
        pygame.draw.rect(screen, GRAY, (music_slider_x, SCREEN_HEIGHT // 3 - 10, slider_width, 20))
        pygame.draw.rect(screen, LIGHT_BLUE, (music_slider_x, SCREEN_HEIGHT // 3 - 10, int(music_volume * slider_width), 20))
        draw_text(screen, f"Громкость музыки: {int(music_volume * 100)}%", pygame.font.Font(None, 24), WHITE, music_slider_x - 10, SCREEN_HEIGHT // 3, align="right")
        pygame.draw.rect(screen, GRAY, (game_slider_x, SCREEN_HEIGHT // 3 - 10 + 50, slider_width, 20))
        pygame.draw.rect(screen, LIGHT_GREEN, (game_slider_x, SCREEN_HEIGHT // 3 - 10 + 50, int(game_volume * slider_width), 20))
        draw_text(screen, f"Громкость игры: {int(game_volume * 100)}%", pygame.font.Font(None, 24), WHITE, game_slider_x - 10, SCREEN_HEIGHT // 3 + 50, align="right")

        back_button.draw(screen)
        difficulty_button.draw(screen)
        save_button.draw(screen)

        if show_save_message:
            current_time = pygame.time.get_ticks()
            if current_time - save_message_start_time <= 5000:
                text_surface = font.render("Настройки сохранены!", True, WHITE)
                text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 250))
                screen.blit(text_surface, text_rect)
            else:
                show_save_message = False

        pygame.display.flip()


def main_menu(itg):
    global background_image, bg_x, bg_direction, music_volume, game_volume, difficulty, current_music_index
    background_image = pygame.image.load(random.choice(BACKGROUND_IMAGES)).convert()
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
    current_music_index = itg
    bg_x = 0
    bg_direction = 1

    def load_and_play_music():
        pygame.mixer.music.load(MUSIC_FILES[current_music_index])
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play()

    load_and_play_music()

    play_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50, "Играть", WHITE, LIGHT_BLUE, show_level_selection)
    options_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50, "Настройки", WHITE, LIGHT_BLUE, options)
    exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150, 200, 50, "Выйти", WHITE, LIGHT_BLUE, lambda: pygame.quit() or sys.exit())

    running = True
    bg_speed = 0.05
    bg_range = 2

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            play_button.handle_event(event)
            options_button.handle_event(event)
            exit_button.handle_event(event)

        bg_x += bg_speed * bg_direction
        if bg_x > bg_range:
            bg_direction = -1
        elif bg_x < -bg_range:
            bg_direction = 1

        screen.blit(background_image, (bg_x, 0))
        draw_text(screen, "Пиксельный Апокалипсис", pygame.font.Font(None, 72), WHITE, SCREEN_WIDTH // 2, 200)

        play_button.draw(screen)
        options_button.draw(screen)
        exit_button.draw(screen)

        if not pygame.mixer.music.get_busy():
            current_music_index = (current_music_index + 1) % len(MUSIC_FILES)
            load_and_play_music()

        pygame.display.flip()

show_level_selection_flag = False
show_save_message = False
save_message_start_time = 0
bg_x = 0
bg_direction = 1

if __name__ == "__main__":
    main_menu(1)