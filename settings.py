class Settings():
    '''Класс с настройками'''
    def __init__(self):
        '''Инициализирует статические настройки игры'''
        #Инициализирует настройки экрана
        self.screen_widht = 1200
        self.screen_height = 700
        self.bg_color = (230, 230, 230)
        
        #Настройки корабля
        self.ship_limit = 3
        
        #Параметры пули
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.max_num_bullet = 3
        
        #Параметры пришельев
        self.fleet_drop = 10
        
        #Темп ускорения игры
        self.speedup_scale = 1.1
        #Темп роста стоимости пришельцев
        self.score_scale = 1.5
        
        #Инициализация динамических парамтров
        self.initialize_dynamic_settings()
    
    def initialize_dynamic_settings(self):
        '''Инициализирует динамические параметры'''
        self.sheep_speed_factor = 0.5
        self.bullet_speed = 3
        self.alien_speed = 0.5
        
        #Подсчёт очков (базовая стоимость пришельца)
        self.alien_points = 50
        
        #feet_direction - 1 вправо, -1 влево
        self.fleet_direction = 1
    
    def increase_speed(self):
        '''Увеличивает скорость игры'''
        self.sheep_speed_factor *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points*self.score_scale)
        
        
