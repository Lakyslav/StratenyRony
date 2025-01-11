import pygame
import engine
import utils
import level
import scene
import globals  
import inputstream
import soundmanager 




# Inicializácia pygame a ostatných komponentov
pygame.init()  # Inicializácia pygame knižnice
screen = pygame.display.set_mode(globals.SCREEN_SIZE)  # Nastavenie veľkosti okna
pygame.display.set_caption('Stratený Rony')  # Nastavenie názvu okna
clock = pygame.time.Clock()  # Hodiny na kontrolu FPS (rýchlosti snímok za sekundu)

# Inicializácia SoundManageru po načítaní nastavení
globals.soundManager = soundmanager.SoundManager()  # Inicializujeme SoundManager

# Inicializácia ďalších herných komponentov
sceneManager = scene.SceneManager()  # Vytvorenie správcu scén
mainMenu = scene.MainMenuScene()  # Vytvorenie hlavnej ponuky (menu)
sceneManager.push(mainMenu)  # Pridanie hlavnej ponuky do správcu scén

inputStream = inputstream.InputStream()  # Vytvorenie inštancie pre spracovanie vstupu

# Inicializácia hráča a kamery
globals.player1 = utils.makePlayer(300, 0)  # Vytvorenie hráča na pozícii (300, 0)
globals.player1.camera = engine.Camera(0, 0, *globals.SCREEN_SIZE)  # Vytvorenie kamery
globals.player1.camera.trackEntity(globals.player1)  # Kamera bude sledovať hráča
globals.player1.input = engine.Input(pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d, pygame.K_q, pygame.K_e)  # Inicializácia vstupu pre hráča

# Hlavný herný cyklus
running = True  # Premenná na riadenie behu hry
while running:
    # Skontroluj, či nie je požiadavka na zatvorenie
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Ukončí herný cyklus

    inputStream.processInput()  # Spracovanie vstupu z klávesnice a myši
    globals.soundManager.update()  # Aktualizácia zvukového manažéra

    if sceneManager.isEmpty():  # Ak je zoznam scén prázdny, končíme hru
        running = False
    
    # Spracovanie vstupu, aktualizácia a kreslenie scén
    sceneManager.input(inputStream)
    sceneManager.update(inputStream)
    sceneManager.draw(screen)

    clock.tick(60)  # Udržiavanie 60 FPS

# Ukončenie pygame po ukončení hry
pygame.quit()






