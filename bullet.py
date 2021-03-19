import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    ''' Класс для управления пулями выпущенными кораблём '''
    def __init__(self, ai_settings, ship, screen):
        ''' Создаёт объект пули в текущей позиции корабля'''
        super().__init__()
        self.screen = screen
        
        #Создание пули в позиции 0,0 и придание правильной позиции
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, 
           ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        
        #Переводим вещественную часть координат пули
        self.y = float(self.rect.y)
        
        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed
        
    def update(self):
        '''Изменяет координату пули'''
        self.y -= self.speed
        #обновляем координату
        self.rect.y = self.y
    
    def draw_bullet(self):
        '''Выводит пулю на экран'''
        pygame.draw.rect(self.screen, self.color, self.rect)
        
