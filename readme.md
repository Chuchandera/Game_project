# Игра "Пиксельный апокалипсис" 24.02.2025
## Оглавление:
* __[Идея игры](#Основ)__
* __[Функции](#задачи)__
* __[Техническая реализация](#прог)__
* __[Интрефейс пользователя](#интер)__
* __[Интрефейс Меню](#интер1)__
* __[Спрайты](#струк)__
* __[Хранение данных](#дан)__

## [Идея проекта](#Основ)
__Целью__ нашей команды стало создание увлекательной и динамичной игры, погружающей игроков в мир зомби-апокалипсиса. Мы стремились разработать проект, который сочетал бы в себе простоту управления и захватывающий игровой процесс, позволяя каждому участнику ощутить напряжение и адреналин, присущие борьбе за выживание в условиях постапокалиптического мира. На каждом уровне игры главной задачей становится полное уничтожение всех зомби, что мы обозначили как «зачистка» территории.

## [Функции игры](#задачи)
### Основные функции игры:
* Передвижение персонажа
* Стрельба при нажатии кнопки
* Возможность перезарядки
* Зомби, атакующие персонажа
### Функции главного меню:
* Настраиваемая сложность, звук
* Изменяемый задний фон
* Возможность выбора уровня
* Меню паузы, запускаемое в игре



## [Техническая реализация](#прог)
### Предустановка программ:
Для корректной работы и отладки программы нужно установить рабочую среду [__python__](https://www.jetbrains.com/pycharm/), а также добавить модуль __PyQt6__.

> Для установки модуля __Pygame__ в рабочей среде откройте __Terminal__ и введите строку:

```
pip install pygame
```

Для создания БД и отладки запросов установить [__sqliteStudio__](https://sqlitestudio.pl/)
### Средства разработки:
* язык программирования __python__ версия __3.11.2__
* текстовый формат обмена данными [__json__](https://ru.wikipedia.org/wiki/JSON)

## [Интрефейс Меню](#интер)
При запуске приложения появляется главное меню, где можно:
* _Начать Игру_
* _Изменить Настройки_
* _Выйти из игры_

![image](https://github.com/user-attachments/assets/94d60d17-f6a3-49a7-8cc6-0cd9f8e478fa)


В меню настроек можно настраивать:
1. _Громкость музыки_
2. _Громкость игры_
3. _Сложность игры_

![image](https://github.com/user-attachments/assets/8ab691d9-e87d-4480-9741-f1f1dfdd1d1b)

## [Игровые механики](#интер1)

За управления отвечают - _WASD_

Для перезарядки необходимо нажать - _R_

При приближении к зомби они начинают стремительно мчаться в сторону игрока, готовые нанести сокрушительный удар. Их неумолимая жажда разрушения и безумие делают каждую встречу с ними настоящим испытанием. Если игрок не успеет расправиться с этими ужасными созданиями вовремя, то последствия могут быть фатальными — он рискует потерять свою жизнь и, соответственно, проиграть.


## [Структура модулей игры](#струк)
### Модуль __menu__
Модуль отвечает за основной интерфейс и вызов вспомогательных модулей.

### Модуль __Player__
Модуль содержит класс персонажа и пули, а также функцию Start, запускающую игру
### Модуль __board_class__
Модуль включает в себя класс доски:
``` python
class Board:
    def __init__(self, map_number, screen, player_coordinates):

        self.board_screen = screen
        self.zombie_spawn_points = []
        self.board, x, y = get_map(map_number)
        self.board_len_y, self.board_len_x = len(self.board), len(self.board[0])

        self.left = player_coordinates[0] + x
        self.top = player_coordinates[1] + y

        self.cell_size = 32
        self.wall_sprites = pygame.sprite.Group()
        self.board_sprites = pygame.sprite.Group()

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
                elif block in [0, 2]:
                    Floor(self.board_sprites, x + x_map * 32, y + y_map * 32)
                    if block == 2:
                        self.zombie_spawn_points.append((x + x_map * 32, y + y_map * 32))


    def update_board(self, delta_x, delta_y):
        self.set_view(self.left + delta_x, self.top + delta_y)
        for cube in self.wall_sprites:
            cube.change_coords(delta_x, delta_y)
        for cube in self.board_sprites:
            cube.change_coords(delta_x, delta_y)

    def draw_board(self):
        self.wall_sprites.draw(self.board_screen)
        self.board_sprites.draw(self.board_screen)

```

А также 2 класса стен и пола, схожего типа:
``` python
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


```

### Модуль __maps__
Модуль включает в себя функции для получения матриц для карт:
``` python
def get_map(num):
    if num == 1:
        global map_1
        return map_1, -80, -900
    elif num == 2:
        global map_2
        return map_2, -150, -1000
    elif num == 3:
        global map_3
        return map_3, -120, -1100
```
В мтрице соблюдаются простые правила:
* 32*32 - один пиксель
* 0 - пол
* 1 - стена
* 2 - зомби
* 4 - ничего, пустота

## [Спрайты](#бд)
База данных в формате SQLite назвается 'users'.
### Спрайт героя
![image](https://github.com/user-attachments/assets/3dd1cdb9-35fd-460a-9a5f-f5a3e87cf592)

### Спрайт пули
![image](https://github.com/user-attachments/assets/aa78770e-877c-4ba4-b38d-459994626bcf)

### Стена
![image](https://github.com/user-attachments/assets/1f67b8b1-b584-44f1-954a-8eb6864cffe7)

### Пол
![image](https://github.com/user-attachments/assets/1c129ac7-7873-4d0d-b825-7fb0f68cd13a)

## [Хранение данных](#дан)
Данные о рекорде игрока хранятся в файле формата _json_, что позволяет сохранять прогресс
```json:
{
  "music_volume": 0.2,
  "game_volume": 0.6,
  "difficulty": "\u041b\u0435\u0433\u043a\u043e"
}
```
