import soundmanager  # Importovanie modulu na správu zvukov


# Premenná pre aktuálnu úroveň
world = None  # Aktuálny svet (úroveň)

maxLevel = 3  # Maximálny počet úrovní
lastCompletedLevel = 3  # Posledná dokončená úroveň
curentLevel = 3  # Aktuálna úroveň (počiatočná)

# Rozmery obrazovky
#1024×576
SCREEN_SIZE = (1024, 576)  # Veľkosť obrazovky (šírka, výška)

# Definovanie farieb pomocou RGB hodnôt
DARK_GREY = (50, 50, 50)  # Tmavo šedá farba
BLACK = (0, 0, 0)  # Čierna farba
WHITE = (255, 255, 255)  # Biela farba
GREEN = (0, 255, 0)  # Zelená farba
RED = (255, 0, 0)  # Červená farba
MUSTARD = (209, 206, 25)  # Horčicová farba

player1 = None  # Využíva sa v platformer.py

# Vytvorenie inštancie správy zvukov
soundManager = soundmanager.SoundManager()  