import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    '''Инициализирует корабль и задаёт начальную позицию'''
    def __init__(self, screen, ai_settings):
        super().__init__()
        '''Инициализирует корабль и задаёт начальную позицию''' 
        self.screen = screen
        self.ai_settings = ai_settings
        #Загружает изображение корабля
        self.image = pygame.image.load('images\ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        #Каждый новый корабль появляется у нижнего края
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        #Сохранение вещественной части коробля
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False
    
    def update(self):
        '''Перемащает корабль вправо'''
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.sheep_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.sheep_speed_factor
        self.rect.centerx = self.center
    
    def blitme(self):
        '''Рисует корабль в текущей позиции'''
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        self.center = self.screen_rect.centerx
        
