import soundmanager  # Importovanie modulu na správu zvukov
import configparser

# Uloženie postupu do súboru savegame.ini
def saveProgress():
    """
    Uloží aktuálny stav hry do súboru savegame.ini.
    Ukladajú sa informácie o postupe hráča, ako sú: 
    - najvyššia dosiahnutá úroveň
    - posledná dokončená úroveň
    - aktuálna úroveň
    - počet životov hráča
    - počet nazbieraných granúl (skóre)
    - čas dosiahnutý v jednotlivých úrovniach
    """
    config = configparser.ConfigParser()  # Vytvorenie konfiguračného objektu
    # Sekcia "Progress" obsahuje základné informácie o postupe hráča
    config['Progress'] = {
        # Uloženie najvyššej dosiahnutej úrovne (nesmie prekročiť maxLevel)
        'highestLevel': min(highestLevel, maxLevel),
        # Uloženie poslednej dokončenej úrovne (nesmie prekročiť maxLevel)
        'lastCompletedLevel': min(lastCompletedLevel, maxLevel),
        # Uloženie aktuálnej úrovne (nesmie prekročiť maxLevel)
        'curentLevel': min(curentLevel, maxLevel),
        # Uloženie počtu životov hráča, ak existuje objekt player1 a má atribút battle
        'playerLives': player1.battle.lives if player1 and player1.battle else 3,
        # Uloženie skóre hráča, ak existuje objekt player1 a má atribút score
        'playerScore': player1.score.score if player1 and player1.score else 0
    }
    # Sekcia "Timers" obsahuje časy jednotlivých úrovní
    config['Timers'] = {f'level{i}': f"{timer:.2f}" for i, timer in levelTimers.items()}
    # Zapíše všetky údaje do súboru savegame.ini
    with open('savegame.ini', 'w') as configfile:
        config.write(configfile)

# Načítanie postupu zo súboru savegame.ini
def loadProgress():
    global highestLevel, lastCompletedLevel, curentLevel, player1, levelTimers
    config = configparser.ConfigParser()  # Vytvorenie konfiguračného objektu
    # Skontroluje, či existuje súbor savegame.ini a načíta jeho obsah
    if config.read('savegame.ini'):
        # Ak existuje sekcia "Progress", načítame hodnoty
        if 'Progress' in config:
            highestLevel = min(int(config['Progress'].get('highestLevel', highestLevel)), maxLevel)
            lastCompletedLevel = min(int(config['Progress'].get('lastCompletedLevel', lastCompletedLevel)), maxLevel)
            curentLevel = min(int(config['Progress'].get('curentLevel', curentLevel)), maxLevel)
            # Ak existuje hráč, nastavíme mu počet životov a skóre
            if player1:
                if player1.battle:
                    player1.battle.lives = int(config['Progress'].get('playerLives', player1.battle.lives))
                if player1.score:
                    player1.score.score = int(config['Progress'].get('playerScore', player1.score.score))
        # Ak existuje sekcia "Timers", načítame časy úrovní
        if 'Timers' in config:
            for i in range(1, highestLevel + 1):
                levelTimers[i] = float(config['Timers'].get(f'level{i}', 0.0))

# Premenná pre aktuálnu úroveň
world = None  # Aktuálny svet (úroveň)

# Budú nastavené pomocou loadProgress
maxLevel = 5
highestLevel = None
lastCompletedLevel = None 
curentLevel = None  

levelTimers = {i: 0.0 for i in range(1, 6)}

import os

def checkFileExists(filename):
    return os.path.isfile(filename)

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
