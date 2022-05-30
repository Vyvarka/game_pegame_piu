from random import randint
from time import sleep

import pygame
from pygame.sprite import Sprite

pygame.init()
# рисуем дисплей/поверхность
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
disp_x = screen.get_rect().width
disp_y = screen.get_rect().height
pygame.display.set_caption('PIU-PIU')  # даем название поверхности
bg = pygame.image.load('images/bg.jpg')  # выбираем фон
speed_boss = 4
score = 0
score_boss = 0


# __________________________________создание групп для выявления коллизий______________________________
bullets_boss = pygame.sprite.Group()
ufo_group = pygame.sprite.Group()


# __________________________________ФУНКЦИЯ ОБНОВЛЕНИЯ ДИСПЛЕЯ______________________________________
def draw_window():
    # перерисовываем фон
    screen.blit(bg, (0, 0))
    # рисуем текст "общий счет"
    text = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text, (20, disp_y//2))
    # рисуем текст "убито боссов"
    text_b = font.render(f'Bosses killed: {score_boss}', True, (255, 255, 255))
    screen.blit(text_b, (20, disp_y//2+30))
    # рисуем пули на поверхности
    for bul in bullets:
        if bul.y < disp_y//3 or bul.y > disp_y//3*2:
            bul.draw()
        else:
            bul.draw_2()
    # рисуем НЛО на поверхности
    for ufo in lst_ufo:
        ufo.draw(screen)
    # рисуем персонажа на поверхности
    plr_1.draw(screen)
    # рисуем ракеты босса на поверхности
    for bul in bull_boss:
        bul.draw(screen)
    # рисуем босса на поверхности
    if boss.timer >= 200:
        if boss.health > 0:
            boss.draw(screen)
    # обновляем дисплей
    pygame.display.update()


# __________________________________КЛАСС PLAYER______________________________________
class Player:
    def __init__(self, widht, height, speed):
        self.ship = pygame.image.load('images/spaceship.png')
        self.rect = self.ship.get_rect()
        # присваиваем характеристики персонажу
        self.widht = widht  # размер
        self.height = height
        self.speed = speed  # скорость
        # координаты
        self.x = int(disp_x//2-self.widht//2)
        self.y = int(disp_y-self.height-self.speed)
        # переменные для реализации прыжка
        self.jump = False  # переменная флаг
        self.count_jump = 9  # высота прыжка (обязательно изменить значения в цикле, если меняем здесь)
        self.ship_limit = 3

    def draw(self, scr):
        scr.blit(self.ship, (self.x, self.y))


plr_1 = Player(38, 60, 10)


# __________________________________КЛАСС BULLET______________________________________
class Bullet:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_bull = plr_1.speed*2

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def draw_2(self):
        pygame.draw.circle(screen, (250, 0, 0), (self.x, self.y), self.radius+2)


# __________________________________КЛАСС ALIEN(НЛО)______________________________________
class Alien(Sprite):
    def __init__(self, x, y, widht, height, speed):
        super().__init__()
        self.ufo = pygame.image.load('images/ufo_2.png')
        self.rect = self.ufo.get_rect()
        self.widht = widht
        self.height = height
        self.speed = speed
        self.x = x
        self.y = y

    def draw(self, scr):
        scr.blit(self.ufo, (self.x, self.y))


# _______________________________________КЛАСС BOSS_________________________________________
class Boss:
    def __init__(self, x, y, speed=4):
        self.boss = pygame.image.load('images/boss_1.png')
        self.widht = 80
        self.height = 120
        self.speed = speed
        self.health = 10
        self.timer = 0
        self.x = x
        self.y = y

    def draw(self, scr):
        scr.blit(self.boss, (self.x, self.y))
        pygame.draw.rect(scr, (0, 255, 0), (self.x, self.y-10, self.widht-8*(10-self.health), 5))


# __________________________________КЛАСС BULLET BOSS______________________________________
class BulletBoss:
    def __init__(self, x, y, speed=30):
        self.bull_b = pygame.image.load('images/bull_boss_1.png')
        self.widht = 21
        self.height = 60
        self.speed = speed
        self.x = x
        self.y = y

    def draw(self, scr):
        scr.blit(self.bull_b, (self.x, self.y))


# __________________________________КЛАСС СТАТИСТИКА______________________________________
class GameStats():
    """Отслеживание статистики для игры Alien Invasion."""
    def __init__(self):
        pass

    def rest_stats(self):
        pass


# __________________________________ЗАПУСК ИГРЫ С ПОМОЩЬЮ ОСНОВНОГО ЦИКЛА______________________________________
font = pygame.font.SysFont('verdana', 26, True)
bull_boss = []
boss = Boss(randint(disp_x//6, (disp_x//6)*5), disp_y//12)
bullets = []
lst_ufo = []
run = True
while run:
    pygame.time.delay(25)
    # отслеживание событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            # выходим из игры путем нажатия клавиши
            if event.key == pygame.K_q:
                run = False
            # создаем "пулю" путем нажатия клавиши
            if event.key == pygame.K_f:
                if len(bullets) < 5:
                    bullets.append(Bullet(plr_1.x + plr_1.widht // 2, plr_1.y, 5, (255, 255, 255)))
            # создаем босса начального уровня
            if event.key == pygame.K_i:
                boss = Boss(randint(disp_x//6, (disp_x//6)*5), disp_y//12, speed_boss)
    # Создаем корабли пришельцев и добавляем их в список
    if len(lst_ufo) < 4:
        aln = Alien(randint(100, disp_x-100), randint(50, disp_y//4), 60, 31, randint(2, 4))
        lst_ufo.append(aln)
        ufo_group.add(aln)
    # Передвигаем корабли пришельцев в зависимости от положения корабля игрока. Удаляем при выходе за границы экрана
    for ufo in lst_ufo:
        if ufo.x < disp_x and ufo.x > 0:
            if ufo.y < disp_y and ufo.y > 0:
                if ufo.x < (plr_1.x - 2*plr_1.widht):
                    ufo.x += ufo.speed
                    ufo.y += ufo.speed
                elif ufo.x > (plr_1.x + 2*plr_1.widht):
                    ufo.x -= ufo.speed
                    ufo.y += ufo.speed
                else:
                    ufo.y += ufo.speed*2
            else:
                lst_ufo.pop(lst_ufo.index(ufo))
                sleep(1)
    # реализуем выстрел. Объект Bullet двигается и ПРОпадает при:
    # - попадании в НЛО;
    # - выходе за границы экрана;
    # - попадании в босса.
    for bullet in bullets:
        if disp_y > bullet.y > 0:  # условие выхода за границы экрана
            bullet.y -= bullet.speed_bull
            for i in lst_ufo:
                if i.x <= bullet.x and (i.x + i.widht + i.speed) >= bullet.x:  # условия попадания в НЛО
                    if i.y <= bullet.y and (i.y + i.height + i.speed) >= bullet.y:
                        lst_ufo.pop(lst_ufo.index(i))
                        bullets.pop(bullets.index(bullet))
                        score += 1
                        break  # нужен для того чтобы не вылетала ошибка при стрельбе
            try:
                if bullet.x >= boss.x and bullet.x <= boss.x + boss.widht + boss.speed:  # условия попадания в БОССА
                    if bullet.y >= boss.y and bullet.y <= boss.y + boss.height // 4 * 3:
                        if boss.timer >= 200:
                            bullets.pop(bullets.index(bullet))
                            boss.health -= 1
            except ValueError:
                continue
        else:
            bullets.pop(bullets.index(bullet))  # удаление объекта при выходе за границы экрана
    # двигаем босса горизонтально в определенных границах
    if boss.health > 0:
        if boss.x > disp_x//7 and boss.x < (disp_x//7)*6:
            boss.x += boss.speed  # босс идет вправо/влево
        else:
            boss.x -= boss.speed  # босс разворачивается на границе
            boss.speed *= (-1)
    # таймер появления босса
    if boss.timer <= 200:
        boss.timer += 1
    # пересоздаем босса
    if boss.health == 0:
        score += 15
        score_boss += 1
        if speed_boss <= 12:
            speed_boss += 1
        boss = Boss(randint(disp_x//6, (disp_x//6)*5), disp_y//12, speed_boss)
    # создаем ракеты, которыми стреляет босс
    if boss.timer >= 200:
        if (boss.x - plr_1.x)**2 < 1000 or ((boss.x + boss.widht) - plr_1.x)**2 < 1000:
            if not bull_boss or bull_boss[0].y > disp_y/2:
                if len(bull_boss) < 4:
                    bull_boss.append(BulletBoss(boss.x - 10, boss.y + 50))  # ракета слева от босса
                    bull_boss.append(BulletBoss(boss.x + boss.widht + 10, boss.y + 50))  # ракета справа от босса
    # двигаем ракеты босса
    for bull in bull_boss:
        if bull.y < disp_y:
            bull.y += bull.speed
            if bull.speed >= 18 + speed_boss:
                bull.speed -= 2
            if (bull.y + bull.height) >= plr_1.y:
                if bull.x >= plr_1.x and bull.x <= (plr_1.x + plr_1.widht + plr_1.speed):
                    bull_boss.pop(bull_boss.index(bull))
                    score -= 20
        else:
            bull_boss.pop(bull_boss.index(bull))
    # Проверка коллизий "пришелец — корабль"
    """
    if pygame.sprite.spritecollideany(plr_1, ufo_group):
        print('Ship hit!!!')
    """

    # создаем "список" событий
    keys = pygame.key.get_pressed()
    # двигаем объект Player с помощью клавиш
    if keys[pygame.K_LEFT] and plr_1.x > plr_1.speed:
        plr_1.x -= plr_1.speed
    if keys[pygame.K_RIGHT] and plr_1.x < (disp_x-plr_1.widht-plr_1.speed):
        plr_1.x += plr_1.speed
    # реализуем прыжок через пробел
    if not plr_1.jump:
        """
        if keys[pygame.K_DOWN] and y < (600 - height - speed):
            y += speed
        if keys[pygame.K_UP] and y > speed:
            y -= speed
        """
        if keys[pygame.K_SPACE]:
            plr_1.jump = True
    else:
        if plr_1.count_jump < -9 or plr_1.count_jump > 9:
            plr_1.jump = False
            plr_1.count_jump = 9
        else:
            if plr_1.count_jump >= 0:
                plr_1.y -= plr_1.count_jump ** 2 / 2
                plr_1.count_jump -= 1
            if plr_1.count_jump < 0:
                plr_1.y += plr_1.count_jump ** 2 / 2
                plr_1.count_jump -= 1
    draw_window()


pygame.quit()
