import pygame
import sys
import random

pygame.init()

# Основные настройки
window_size = (600, 800)
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()

# Платформа
platform = pygame.Rect(250, 750, 100, 10)
platform_speed = 8

# Шарик
circle = pygame.Rect(300, 400, 20, 20)
circle_speed = [4, 4]

# Жизни
lives = 3
font = pygame.font.Font(None, 36)

# Кирпичики
brick_width = 44
brick_height = 10
bricks = [pygame.Rect(x * (brick_width + 10) + 35, y * (brick_height + 10) + 50, brick_width, brick_height) for x in range(10) for y in range(5)]

# Бонусы и анти-бонусы
bonuses = []
antibonuses = []
bonus_duration = 3000  # 3000 мс = 3 секунды
bonus_active = False
bonus_end_time = 0

def draw_lives():
    lives_text = font.render(f'Lives: {lives}', True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

def game_over_screen():
    screen.fill((0, 0, 0))
    game_over_text = font.render('You Lost!', True, (255, 0, 0))
    screen.blit(game_over_text, (window_size[0] // 2 - game_over_text.get_width() // 2, window_size[1] // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

def game_win_screen():
    screen.fill((0, 0, 0))
    game_win_text = font.render('You Won!', True, (0, 255, 0))
    screen.blit(game_win_text, (window_size[0] // 2 - game_win_text.get_width() // 2, window_size[1] // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

def spawn_bonus(x, y):
    bonus = pygame.Rect(x, y, 20, 20)
    bonuses.append(bonus)

def spawn_antibonus(x, y):
    antibonus = pygame.Rect(x, y, 20, 20)
    antibonuses.append(antibonus)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and platform.left > 0:
        platform.x -= platform_speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and platform.right < window_size[0]:
        platform.x += platform_speed

    circle.x += circle_speed[0]
    circle.y += circle_speed[1]

    if circle.left <= 0 or circle.right >= window_size[0]:
        circle_speed[0] = -circle_speed[0] + random.uniform(-0.5, 0.5)
        circle_speed[1] += random.uniform(-0.5, 0.5)
    if circle.top <= 0:
        circle_speed[1] = -circle_speed[1] + random.uniform(-0.5, 0.5)
        circle_speed[0] += random.uniform(-0.5, 0.5)
    if circle.bottom >= window_size[1]:
        lives -= 1
        if lives <= 0:
            game_over_screen()
        else:
            circle.x, circle.y = 300, 400
            circle_speed = [4, 4]

    if circle.colliderect(platform) and circle_speed[1] > 0:
        circle_speed[1] = -circle_speed[1] + random.uniform(-0.5, 0.5)

    # Обработка столкновений с кирпичиками
    for brick in bricks[:]:
        if circle.colliderect(brick):
            circle_speed[1] = -circle_speed[1] + random.uniform(-0.5, 0.5)
            bricks.remove(brick)
            if random.random() < 0.3: 
                spawn_bonus(brick.x, brick.y)
            elif random.random() < 0.6: 
                spawn_antibonus(brick.x, brick.y)
            break

    # Обновление позиции бонусов и анти-бонусов
    for bonus in bonuses[:]:
        bonus.y += 2  # Скорость падения бонуса
        if platform.colliderect(bonus):
            bonuses.remove(bonus)
            platform.width += 50
            bonus_active = True
            bonus_end_time = pygame.time.get_ticks() + bonus_duration
        elif bonus.top > window_size[1]:
            bonuses.remove(bonus)

    for antibonus in antibonuses[:]:
        antibonus.y += 2  # Скорость падения анти-бонуса
        if platform.colliderect(antibonus):
            antibonuses.remove(antibonus)
            circle_speed[0] *= 1.2
            circle_speed[1] *= 1.2
        elif antibonus.top > window_size[1]:
            antibonuses.remove(antibonus)

    # Проверка окончания действия бонуса
    if bonus_active and pygame.time.get_ticks() > bonus_end_time:
        platform.width -= 50
        bonus_active = False

    screen.fill((255, 165, 0))
    pygame.draw.ellipse(screen, (255, 255, 255), circle)
    pygame.draw.rect(screen, (255, 0, 0), platform)
    draw_lives()

    for brick in bricks:
        pygame.draw.rect(screen, (0, 0, 255), brick)

    for bonus in bonuses:
        pygame.draw.rect(screen, (0, 255, 0), bonus)

    for antibonus in antibonuses:
        pygame.draw.rect(screen, (255, 0, 0), antibonus)

    pygame.display.flip()
    clock.tick(60)

    # Проверка выигрыша
    if not bricks:
        game_win_screen()