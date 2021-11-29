import pygame.font
from pygame.sprite import Group
from src.models.ship import Ship

class Scoreboard():
    '''Класс для вывода игровой информации'''
    def __init__(self, ai_settings, screen, stats):
        '''Инициализация атрибутов подсчёта очков'''
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        
        #Настройка шрифта для вывода счёта
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None, 48)
        
        #Подготовка исходного изображения текущего счёта
        self.prep_score()
        #Подготовка изображения максимального счёта
        self.prep_high_score()
        #Подготовка уровня
        self.prep_level()
        #Подготовка количества жизней
        self.prep_ships()
        
    def prep_score(self):
        '''Преобразует текущий счёт в изображение'''
        self.rounded_score = int(round(self.stats.score, -1))
        self.score_str = "{:,}".format(self.rounded_score)
        self.score_image = self.font.render(self.score_str, True, self.text_color,
             self.ai_settings.bg_color)
        
        #Вывод счёта в верхней части экрана
        self.score_image_rect = self.score_image.get_rect()
        self.score_image_rect.right = self.screen_rect.right - 20
        self.score_image_rect.top = 20
    
    def prep_high_score(self):
        '''Преобразует максимальный счёт в изображение'''
        self.high_score = int(round(self.stats.high_score, -1))
        self.high_score_str = "{:,}".format(self.high_score)
        self.high_score_image = self.font.render(self.high_score_str, True,
             self.text_color, self.ai_settings.bg_color)
        self.high_score_image_rect = self.high_score_image.get_rect()
        self.high_score_image_rect.centerx = self.screen_rect.centerx
        self.high_score_image_rect.top = 20
    
    def prep_level(self):
        '''Подготовливает уровень'''
        self.level_str = str(self.stats.level)
        self.level_image = self.font.render(self.level_str, True,
             self.text_color, self.ai_settings.bg_color)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.top = self.score_image_rect.bottom
        self.level_image_rect.right = self.score_image_rect.right
        
    def prep_ships(self):
        '''Подготавлиаеит колиество жизней'''
        self.ships = Group()
        for n in range(self.stats.ships_left):
            ship = Ship(self.screen, self.ai_settings)
            ship.rect.x = 10 + n * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)
            
    
    def show_score(self):
        '''Выводит счёт на экран'''
        self.screen.blit(self.score_image, self.score_image_rect)
        self.screen.blit(self.high_score_image, self.high_score_image_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        self.ships.draw(self.screen)
