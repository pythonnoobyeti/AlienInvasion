import sys

import pygame
from time import sleep

from bullet import Bullet
from alien import Alien
import json

def fire_bullet(ai_settings, bullets,ship,screen):
    '''Создание пули'''
    if len(bullets) < ai_settings.max_num_bullet:
            #Создание пули и сохранение её в Group
            new_bullet = Bullet(ai_settings, ship, screen)
            bullets.add(new_bullet)

def check_keydown_events(event, ship, bullets, ai_settings, screen, stats,
    aliens, filename, sb):
    '''Проверяет события с нажатием клавиш'''
    if event.key == pygame.K_q:
        save_high_score(filename, stats)
        sys.exit()
    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, bullets, ship, screen)
    elif event.key == pygame.K_p:
        check_play_key(stats, aliens, bullets, ship, ai_settings, screen, sb)

def check_keyup_events(event, ship):
    '''Проверяет события с отпусканием клавиш'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ship, ai_settings, bullets, screen, stats, play_button, 
        aliens, sb, filename):
    '''Обрабатывает нажатия клавиш и события мыши'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score(filename, stats)
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ship, bullets, ai_settings, screen, 
            stats, aliens, filename, sb)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, 
            aliens, bullets, ship, ai_settings, screen, sb)

def check_play_button(stats, play_button, mouse_x, mouse_y, aliens, 
    bullets, ship, ai_settings, screen, sb):
    '''Определяет пересечение точки щелчка мыши и кнопки Play'''
    button_cliced = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_cliced and not stats.game_active:
        start_game(stats, aliens, bullets, ship, ai_settings, screen, sb)

def check_play_key(stats, aliens, bullets, ship, ai_settings, screen, sb):
    '''Обнуляет параметры при нажатии клавиши p и начинает игру'''
    if not stats.game_active:
        start_game(stats, aliens, bullets, ship, ai_settings, screen, sb)    
            
def start_game(stats, aliens, bullets, ship, ai_settings, screen, sb):
    '''Обнуляет все параметры перед началом новой игры'''
    stats.reset_stats()
    ai_settings.initialize_dynamic_settings()
    stats.game_active = True
    pygame.mouse.set_visible(False)
    
    #Сброс игры
    sb.prep_score()
    sb.prep_high_score()
    sb.prep_level()
    sb.prep_ships()
        
    #Обнуление пуль и пришельцев
    aliens.empty()
    bullets.empty()
        
    #Возвращение корабля в центр
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def update_screen(screen, ai_settings, ship, bullets, aliens, stats, 
    play_button, sb):
    '''Функция обновления экрана'''
    #Заполнить экран серым цветом
    screen.fill(ai_settings.bg_color)
    #Вывод счёта
    sb.show_score()
    #Добавление корабля
    ship.blitme()
    #Вывод пуль
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    #Вывод на экран пришельцев
    aliens.draw(screen)
    #Кнопка play отображается, если игна не активка
    if not stats.game_active:
        play_button.draw_button()
    #Обновление экрана
    pygame.display.flip()

def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb):
    '''Обновление координат пуль и удаление старых'''
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    #Проверка коллизий пули и пришельца
    check_alien_bullet_collision(ai_settings, screen, ship, aliens, bullets,
            stats, sb)

def check_alien_bullet_collision(ai_settings, screen, ship, aliens, bullets, 
            stats, sb):
    '''Удаляет пулю и пришельца при столкновении'''
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
            check_high_score(stats, sb)
    if len(aliens) == 0:
        #Уничтожает старые пули
        bullets.empty()
        #Повышаем скорость игры
        ai_settings.increase_speed()
        #Повышает уровень игры
        stats.level += 1
        sb.prep_level()
        #Создаём новый флот
        create_fleet(ai_settings, screen, ship, aliens)
        
    

def get_number_aliens_x(ai_settings, alien_widht):
    '''Вычисляет количество пришельцев в ряду'''
    available_space_x = ai_settings.screen_widht - (alien_widht * 2)
    num_aliens_x = int(available_space_x / (alien_widht * 2))
    return num_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    '''Определяет количество рядов'''
    available_space_y = (ai_settings.screen_height -
                  (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows
    
    
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''Создаёт пришельца и добавляет в ряд'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + (alien_width * 2 * alien_number)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien) 
    

def create_fleet(ai_settings, screen, ship, aliens):
    '''Содаёт флот пришельцев'''
    #Создаёт пришельца и вычисляет количество рядов и пришельцев в ряду
    alien = Alien(ai_settings, screen)
    num_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings,  ship.rect.height, 
                    alien.rect.height)
    #Создаёт флот пришельцев
    for row in range(number_rows):
        for alien_number in range(num_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row)
    
def check_fleet_edges(ai_settings, aliens):
    '''Проверяет достижение граней флотом'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''Меняет направление флота'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop
    ai_settings.fleet_direction *= -1
            

def update_aliens(stats, ai_settings, screen, ship, aliens, bullets, sb):
    '''Обновляет позиции всех пришельцев во флоте, 
    определяет достижение граней'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    #Проверка колизий между пришельцами и кораблём
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(stats, ai_settings, screen, ship, aliens, bullets, sb)
    #Проверяет достижение пришельцами нижней грани экрана
    check_aliens_bottom(stats, ai_settings, screen, ship, aliens, bullets, sb)
        
def ship_hit(stats, ai_settings, screen, ship, aliens, bullets, sb):
    '''Действия при столкновении пришельцев с кораблём'''
    if stats.ships_left > 1:
        #Минус один корабль
        stats.ships_left -= 1
        #Подготовка количства жизней
        sb.prep_ships()
        #Обнуляет пришельцев и пули
        aliens.empty()
        bullets.empty()
        #Создаёт новый флот и возвращает корабль в центр
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        #Пауза
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(stats, ai_settings, screen, ship, aliens, bullets, sb):
    '''Проверяет достижение пришельцами нижней грани экрана'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #Происходит тожеб что и при столкновении с кораблём
            ship_hit(stats, ai_settings, screen, ship, aliens, bullets, sb)
            break

def check_high_score(stats, sb):
    '''Проверяетб появился ли новый рекорд'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def save_high_score(filename, stats):
    '''Сохраняет лучшиц счёт'''
    with open(filename, 'w') as f_obj:
            json.dump(stats.high_score, f_obj)
