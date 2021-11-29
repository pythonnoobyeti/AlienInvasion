import json

class GameStats():
    '''Отслеживание статистики игры'''
    def __init__(self, ai_settings, filename):
        '''Инициализирует статистику'''
        self.ai_settings = ai_settings
        #Самый высокий счёт
        with open(filename, 'r') as f_o:
            self.high_score = int(json.load(f_o))
        self.reset_stats()
        #Игра запускается в активном состоянии
        self.game_active = False
    
    def reset_stats(self):
        '''Инициализирует статистику изменившуюся в ходе игры'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
