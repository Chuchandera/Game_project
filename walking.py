import pygame
from maps import *



if __name__ == '__main__':
    pygame.init()  # Инициализация Pygame
    pygame.display.set_caption('Движение героя')  # Заголовок окна
    size = width, height = 960, 800  # Размеры окна
    screen = pygame.display.set_mode(size)  # Создание окна

    clock = pygame.time.Clock()  # Объект для управления временем
    running = True  # Флаг для основного цикла

    # Загрузка изображений для анимации
    left_pose = [
        pygame.image.load('player/left_player_1.png'),
        pygame.image.load('player/left_player_2.png'),
        pygame.image.load('player/left_player_3.png'),
        pygame.image.load('player/left_player_4.png')
    ]

    right_pose = [
        pygame.image.load('player/right_player_1.png'),
        pygame.image.load('player/right_player_2.png'),
        pygame.image.load('player/right_player_3.png'),
        pygame.image.load('player/right_player_4.png')
    ]


    back = pygame.image.load('backs/background_2.jpg')

    x, y = -96, -96  # Начальные координаты
    what_anim = 0  # Индекс текущего кадра
    side = left_pose  # Начальная анимация

    # Флаги для отслеживания нажатия клавиш
    key_a_pressed, key_d_pressed, key_w_pressed, key_s_pressed = False, False, False, False
    frame_counter = 0  # Счетчик кадров

    while running:  # Основной игровой цикл
        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:  # Проверка нажатия клавиш
                if event.key == pygame.K_a:
                    side = left_pose
                    key_a_pressed = True
                elif event.key == pygame.K_d:
                    side = right_pose
                    key_d_pressed = True
                elif event.key == pygame.K_w:
                    key_w_pressed = True
                elif event.key == pygame.K_s:
                    key_s_pressed = True

            if event.type == pygame.KEYUP:  # Проверка отпускания клавиш
                if event.key == pygame.K_a:
                    key_a_pressed = False
                elif event.key == pygame.K_d:
                    key_d_pressed = False
                elif event.key == pygame.K_w:
                    key_w_pressed = False
                elif event.key == pygame.K_s:
                    key_s_pressed = False

        # Движение персонажа
        if key_a_pressed or key_d_pressed or key_w_pressed or key_s_pressed:
            if key_a_pressed:
                x += 2
            if key_d_pressed:
                x -= 2
            if key_w_pressed:
                y += 2
            if key_s_pressed:
                y -= 2

            frame_counter += 1  # Увеличение счетчика кадров

            if frame_counter >= 10:  # Смена кадра анимации
                what_anim = (what_anim + 1) % len(side)
                frame_counter = 0

        # screen.fill((131,241,236))  # Очистка экрана

        screen.blit(back, (x, y))
        screen.blit(side[what_anim], (480, 400))  # Отрисовка текущего персонажа

        pygame.display.flip()  # Обновление экрана
        clock.tick(60)  # Ограничение FPS

    pygame.quit()  # Завершение работы Pygame