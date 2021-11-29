import sys

import pygame

from settings import Settings
from src.models.ship import Ship
import src.utils.game_functions as gf
from pygame.sprite import Group
from src.models.game_stats import GameStats
from src.models.button import Button
from src.models.scoreboard import Scoreboard
import json

filename = 'score.json'

def run_game():
    #Инициализация данных pygame
    pygame.init()
    #Создание экрана 
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_widht, ai_settings.screen_height))
    #Создание кнопки
    play_button = Button(ai_settings, screen, 'Play')
    #Название окна
    pygame.display.set_caption("Alien invasion")
    #Создание класов для статистики
    stats = GameStats(ai_settings, filename)
    sb = Scoreboard(ai_settings, screen, stats)
    #Создание корабля, группы пуль ипришельцев
    ship = Ship(screen, ai_settings)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    
    while True:
        #Цикл по поиску событий и реагирования на них
        gf.check_events(ship, ai_settings, bullets, screen, stats, play_button, 
        aliens, sb, filename)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, 
               stats, sb)
            gf.update_aliens(stats, ai_settings, screen, ship, aliens, bullets,
               sb)
        gf.update_screen(screen, ai_settings, ship, bullets, aliens, stats, 
           play_button, sb)

run_game()
    
