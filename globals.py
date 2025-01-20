import soundmanager  # Importovanie modulu na správu zvukov
import configparser

# Ulož potup do savegame.ini
def saveProgress():
    config = configparser.ConfigParser()
    config['Progress'] = {
        'maxLevel': maxLevel,
        'lastCompletedLevel': lastCompletedLevel,
        'curentLevel': curentLevel,
        'playerLives': player1.battle.lives if player1 and player1.battle else 3,
        'playerScore': player1.score.score if player1 and player1.score else 0
    }
    config['Timers'] = {f'level{i}': f"{timer:.2f}" for i, timer in levelTimers.items()}
    with open('savegame.ini', 'w') as configfile:
        config.write(configfile)

# Načítaj postup zo savegame.ini
def loadProgress():
    global maxLevel, lastCompletedLevel, curentLevel, player1, levelTimers
    config = configparser.ConfigParser()
    if config.read('savegame.ini'):
        if 'Progress' in config:
            maxLevel = int(config['Progress'].get('maxLevel', maxLevel))
            lastCompletedLevel = int(config['Progress'].get('lastCompletedLevel', lastCompletedLevel))
            curentLevel = int(config['Progress'].get('curentLevel', curentLevel))
            if player1:
                if player1.battle:
                    player1.battle.lives = int(config['Progress'].get('playerLives', player1.battle.lives))
                if player1.score:
                    player1.score.score = int(config['Progress'].get('playerScore', player1.score.score))
        if 'Timers' in config:
            for i in range(1, maxLevel + 1):
                levelTimers[i] = float(config['Timers'].get(f'level{i}', 0.0))


# Premenná pre aktuálnu úroveň
world = None  # Aktuálny svet (úroveň)

# Budú nastavené pomocou loadProgress
maxLevel = None  
lastCompletedLevel = None 
curentLevel = None  

levelTimers = {i: 0.0 for i in range(1, 4)}




# Rozmery obrazovkyz
SCREEN_SIZE = (1024, 576)  # Veľkosť obrazovky (šírka, výška)

# Definovanie farieb pomocou RGB hodnôt
DARK_GREY = (50, 50, 50)  # Tmavo šedá farba
BLACK = (0, 0, 0)  # Čierna farba
WHITE = (255, 255, 255)  # Biela farba
GREEN = (0, 255, 0)  # Zelená farba
RED = (255, 0, 0)  # Červená farba
MUSTARD = (209, 206, 25)  # Horčicová farba

player1 = None  # Hráč, inicializovaný neskôr v platformer.py

# Vytvorenie inštancie správy zvukov
soundManager = soundmanager.SoundManager()
