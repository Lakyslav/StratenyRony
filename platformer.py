import pygame
import engine
import utils
import scene
import globals  
import inputstream
import soundmanager 

# Inicializácia pygame a ostatných komponentov
pygame.init()  # Inicializácia pygame knižnice
screen = pygame.display.set_mode(globals.SCREEN_SIZE)  # Nastavenie veľkosti okna
pygame.display.set_caption('Stratený Rony')  # Nastavenie názvu okna

# Nastavenie ikony hry
icon = pygame.image.load('images\dachshund_zivot.png')  # Načítanie obrázka pre ikonu
pygame.display.set_icon(icon)  # Nastavenie ikony hry

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

    if sceneManager.isEmpty():  # Ak je zoznam scén prázdny ukončíme hru
        running = False
    
    #print(f"FPS: {int(clock.get_fps())}")
    sceneManager.input(inputStream) # Spracovanie vstupu
    sceneManager.update(inputStream) # aktualizácia
    sceneManager.draw(screen) # kreslenie scén

    clock.tick(60)  # Udržiavanie 60 FPS

pygame.quit() # Ukončenie pygame po ukončení hry
