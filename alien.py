import pygame

from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self, ai_settings, screen):
        super().__init__()
        self.ai_settings = ai_settings
        self.screen = screen
        #Выводим пришельца на экран и присваиваем атрибут rect
        self.image = pygame.image.load('images/aliens.bmp')
        self.rect = self.image.get_rect()
        #Задаём нужные координаты
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        #Определяем вещественную координату
        self.x = float(self.rect.x)
        
    def update(self):
        '''Перемещает пришельцев вправо'''
        self.x += (self.ai_settings.alien_speed * 
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x
    
    def check_edges(self):
        self.screen_rect = self.screen.get_rect()
        if self.rect.right >= self.screen_rect.right:
            return True
        if self.rect.left<= 0:
            return True
