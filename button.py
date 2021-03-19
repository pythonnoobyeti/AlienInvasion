import pygame.font

class Button():
    '''Кнопка для запуска игры'''
    def __init__(self, ai_settings, screen, msg):
        '''Инициализирует атрибуты кнопки'''
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        
        #Назначение параметров кнопки
        self.width, self.height = 100, 50
        self.button_color = (89, 152, 0)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        #Построение прямоугольника кнопки
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        
        #Сообщене создаётся только один раз
        self.prep_msg(msg)
        
    def prep_msg(self, msg):
        '''Преоразует msg в прямоугольник и выравнивает по центру'''
        self.msg_image = self.font.render(msg, True, self.text_color,
            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        '''Отображение пустой кнопки и вывод на экарн текста'''
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        
        
        
