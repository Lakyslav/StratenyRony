import pygame
import engine
import utils
import level
import globals
import ui
import soundmanager
import sys


# Základná trieda pre scénu, ktorá definuje základné metódy
class Scene:
    def __init__(self):
        pass
    def onEnter(self):
        pass  # Metóda, ktorá sa vykoná pri vstupe do scény
    def onExit(self):
        pass  # Metóda, ktorá sa vykoná pri opustení scény
    def input(self, sm, inputStream):
        pass  # Spracovanie vstupov
    def update(self, sm, inputStream):
        pass  # Aktualizácia scény
    def draw(self, sm, screen):
        pass  # Vykreslenie scény na obrazovku

# Hlavná ponuka scény
class MainMenuScene(Scene): 
    def __init__(self):
        # Tlačidlá pre navigáciu v menu
        self.enter = ui.ButtonUI(pygame.K_RETURN, 'Pokračovať', 50, 200, normal_img=r"images\UI\Button BG shadow.png",hover_img=r"images\UI\Button BG.png",hover_text_color=globals.MUSTARD)
        self.new_game = ui.ButtonUI(pygame.K_n, 'Nová hra', 50, 250, normal_img=r"images\UI\Button BG shadow.png",hover_img=r"images\UI\Button BG.png",hover_text_color=globals.MUSTARD)  # New button
        self.settings = ui.ButtonUI(pygame.K_s, 'Nastavenia', 50, 300, normal_img=r"images\UI\Button BG shadow.png",hover_img=r"images\UI\Button BG.png",hover_text_color=globals.MUSTARD)
        self.tutorial_button = ui.ButtonUI(pygame.K_t, 'Návod', 50, 350, normal_img=r"images\UI\Button BG shadow.png",hover_img=r"images\UI\Button BG.png",hover_text_color=globals.MUSTARD)  # Tlačidlo pre návod
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, 'Ukončiť hru', 50, 400, normal_img=r"images\UI\Button BG shadow.png",hover_img=r"images\UI\Button BG.png",hover_text_color=globals.MUSTARD)

        self.background = pygame.image.load('images\menu\orig.png').convert()
        self.background = pygame.transform.scale(self.background, globals.SCREEN_SIZE)


    def onEnter(self):
        # Hranie hudby pri vstupe do hlavného menu
        globals.soundManager.playMusicFade('menu')


    def input(self, sm, inputStream):
        # Check if Enter key is pressed and savegame.ini does not exist
        if (inputStream.keyboard.isKeyPressed(pygame.K_RETURN) or self.enter.on) and not globals.checkFileExists('savegame.ini'):
            globals.highestLevel = 1
            globals.lastCompletedLevel = 1
            globals.curentLevel = 1
            globals.player1.battle.lives = 3
            globals.player1.score.score = 0
            globals.levelTimers = {i: 0.0 for i in range(1, 6)}
            globals.saveProgress()  # Save the reset progress
            globals.loadProgress()  # Load the saved progress
            sm.push(FadeTransitionScene([self], [LevelSelectScene()]))  # Transition to level selection

        # Reset progress if new game is triggered or "n" is pressed
        if self.new_game.on or inputStream.keyboard.isKeyPressed(pygame.K_n):
            globals.highestLevel = 1
            globals.lastCompletedLevel = 1
            globals.curentLevel = 1
            globals.player1.battle.lives = 3
            globals.player1.score.score = 0
            globals.levelTimers = {i: 0.0 for i in range(1, 6)}
            globals.saveProgress()  # Save the reset progress
            self.enter.on = True  # Trigger the enter action

        # Handle the Enter key to load progress and transition to level select
        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN) or self.enter.on and globals.checkFileExists('savegame.ini'):
            globals.loadProgress()  # Load the saved progress
            sm.push(FadeTransitionScene([self], [LevelSelectScene()]))  # Transition to level selection

        # Transition to settings if "s" is pressed
        if inputStream.keyboard.isKeyPressed(pygame.K_s) or self.settings.on:
            sm.push(FadeTransitionScene([self], [SettingsScene()]))  # Transition to settings scene

        # Transition to tutorial if "t" is pressed
        if inputStream.keyboard.isKeyPressed(pygame.K_t) or self.tutorial_button.on:
            sm.push(FadeTransitionScene([self], [TutorialScene()]))  # Transition to tutorial scene

        # Exit the game if Escape key is pressed
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE) or self.esc.on:
            sys.exit()


    def update(self, sm, inputStream):
        # Aktualizácia stavu tlačidiel
        self.enter.update(inputStream)
        self.new_game.update(inputStream)
        self.settings.update(inputStream)
        self.tutorial_button.update(inputStream)  # Aktualizácia tlačidla pre návod
        self.esc.update(inputStream)

    def draw(self, sm, screen):
        screen.blit(self.background, (0, 0))
        # Nastavenie pozadia a vykreslenie názvu menu
        utils.drawText(screen, 'Stratený Rony', 50, 50, globals.DARK_GREY, 255,utils.PixelOperator8_Bold)

        # Vykreslenie tlačidiel v menu
        self.enter.draw(screen)
        self.new_game.draw(screen)
        self.settings.draw(screen)
        self.tutorial_button.draw(screen)  # Vykreslenie tlačidla pre návod
        self.esc.draw(screen)

        

# Scéna s návodom
class TutorialScene(Scene):
    def __init__(self):
        # Tlačidlo na návrat do hlavného menu
        self.menu_button = ui.ButtonUI(pygame.K_ESCAPE, 'Menu', 440, 438, normal_img=r"images\UI\Button BG shadow.png",hover_img=r"images\UI\Button BG.png",hover_text_color=globals.MUSTARD)
        self.controls_text = ui.ButtonUI(pygame.K_AMPERSAND, '', 50, 50, normal_img=r"images\UI\Settings BG.png",width=222,height=462, align_top=True, align_center=False)
        self.tutorials_text = ui.ButtonUI(pygame.K_AMPERSAND, '', 272, 50, normal_img=r"images\UI\Settings BG.png",width=368,height=462, align_top=True, align_center=False)

    
        self.background = pygame.image.load('images\menu\orig.png').convert()
        self.background = pygame.transform.scale(self.background, globals.SCREEN_SIZE)

    def input(self, sm, inputStream):
        # Akcia pre návrat do hlavného menu
        if self.menu_button.on or inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()  # Návrat na predchádzajúcu scénu (hlavné menu)
            sm.push(FadeTransitionScene([self], []))

    def update(self, sm, inputStream):
        # Aktualizácia stavu tlačidla
        self.menu_button.update(inputStream)
        self.controls_text.update(inputStream)
        self.tutorials_text.update(inputStream)

    def draw(self, sm, screen):
        screen.blit(self.background, (0, 0))

        # Texty pre hlasitosť zvukových efektov a hudby
        nadpis = f"  Ovládanie"
        line1 = f"  W - skok"
        line2 = f"  A - pohyb doľava"
        line3 = f"  D - pohyb doprava"
        line4 = f"  ESC - návrat späť"
        # Zostavíme dynamický text, ktorý chceme zobraziť na tlačidle
        c_text = f"\n\n{nadpis}\n\n{line1}\n\n{line2}\n\n{line3}\n\n{line4}"
        tut_text = f"\n\n  Návod\n\n  Cieľom hry je prejsť 5 úrovní\n  za čo najrýchleší čas a doniesť tým \n  strateného psíka Ronyho späť za\n  jeho rodinou. Hra sa odohráva v\n  niekoľkých rôznych prostrediach\n  ako napríklad lúka,hory, a les.\n  Počas priebehu hry je možné sa\n  hocikedy vrátiť na\n  predchádzajúcu obrazovku\n  pomocou tlačidla ESC. Cieľ \n  každej úrovne je označený\n  krabicou s otáznikom"
        # Nastavíme text do tlačidla (ako text na pozadí tlačidla)
        self.controls_text.text = c_text
        self.tutorials_text.text = tut_text
        # Vykreslíme tlačidlo so správnym textom
        self.controls_text.draw(screen)
        self.tutorials_text.draw(screen)
        # Vykreslenie tlačidla na návrat
        self.menu_button.draw(screen)




# Scéna pre nastavenia zvuku
class SettingsScene(Scene):
    def __init__(self):
        # Načítame hodnoty hlasitosti priamo zo SoundManager
        self.sfx_volume = globals.soundManager.soundVolume
        self.music_volume = globals.soundManager.musicVolume

        # Inicializácia SoundManager s aktuálnymi hodnotami
        globals.soundManager.loadSettings(self.sfx_volume, self.music_volume)

        # Tlačidlá na úpravu hlasitosti
        self.increase_sfx_button = ui.ButtonUI(pygame.K_w, '+', 272, 120, normal_img=r"images\UI\Inventory Cell.png",width=40,height=40)
        self.decrease_sfx_button = ui.ButtonUI(pygame.K_s, '-', 312, 120, normal_img=r"images\UI\Inventory Cell.png",width=40,height=40)

        self.increase_music_button = ui.ButtonUI(pygame.K_UP, '+', 272, 160, normal_img=r"images\UI\Inventory Cell.png",width=40,height=40)
        self.decrease_music_button = ui.ButtonUI(pygame.K_DOWN, '-', 312, 160, normal_img=r"images\UI\Inventory Cell.png",width=40,height=40)

        self.menu_button = ui.ButtonUI(pygame.K_ESCAPE, 'Menu', 450, 444, normal_img=r"images\UI\Button BG shadow.png",hover_img=r"images\UI\Button BG.png",hover_text_color=globals.MUSTARD)


        self.dynamic_button = ui.ButtonUI(pygame.K_AMPERSAND, '', 50, 50, normal_img=r"images\UI\Settings BG.png",width=222,height=462, align_top=True)

        self.background = pygame.image.load('images\menu\orig.png').convert()
        self.background = pygame.transform.scale(self.background, globals.SCREEN_SIZE)

    def onExit(self):
        globals.soundManager.saveSettings()

    def input(self, sm, inputStream):
        # Klávesové ovládanie pre zvukové efekty
        if inputStream.keyboard.isKeyPressed(pygame.K_w):
            self.sfx_volume = min(self.sfx_volume + 0.1, 1.0)
            globals.soundManager.setSoundVolume(self.sfx_volume)  # Použitie metódy na nastavenie hlasitosti
        if inputStream.keyboard.isKeyPressed(pygame.K_s):
            self.sfx_volume = max(self.sfx_volume - 0.1, 0.0)
            globals.soundManager.setSoundVolume(self.sfx_volume)  # Použitie metódy na nastavenie hlasitosti

        # Klávesové ovládanie pre hudbu
        if inputStream.keyboard.isKeyPressed(pygame.K_UP):
            self.music_volume = min(self.music_volume + 0.1, 1.0)
            globals.soundManager.setMusicVolume(self.music_volume)  # Použitie metódy na nastavenie hlasitosti hudby
        if inputStream.keyboard.isKeyPressed(pygame.K_DOWN):
            self.music_volume = max(self.music_volume - 0.1, 0.0)
            globals.soundManager.setMusicVolume(self.music_volume)  # Použitie metódy na nastavenie hlasitosti hudby

        # Spracovanie kliknutí na tlačidlá
        if self.increase_sfx_button.on:
            self.sfx_volume = min(self.sfx_volume + 0.1, 1.0)
            globals.soundManager.setSoundVolume(self.sfx_volume)  # Použitie metódy na nastavenie hlasitosti
        if self.decrease_sfx_button.on:
            self.sfx_volume = max(self.sfx_volume - 0.1, 0.0)
            globals.soundManager.setSoundVolume(self.sfx_volume)  # Použitie metódy na nastavenie hlasitosti
        if self.increase_music_button.on:
            self.music_volume = min(self.music_volume + 0.1, 1.0)
            globals.soundManager.setMusicVolume(self.music_volume)  # Použitie metódy na nastavenie hlasitosti hudby
        if self.decrease_music_button.on:
            self.music_volume = max(self.music_volume - 0.1, 0.0)
            globals.soundManager.setMusicVolume(self.music_volume)  # Použitie metódy na nastavenie hlasitosti hudby

        # Návrat do menu
        if self.menu_button.on or inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.pop()  # Návrat na predchádzajúcu scénu
            sm.push(FadeTransitionScene([self], []))

    def update(self, sm, inputStream):
        # Aktualizácia tlačidiel
        self.increase_sfx_button.update(inputStream)
        self.decrease_sfx_button.update(inputStream)
        self.increase_music_button.update(inputStream)
        self.decrease_music_button.update(inputStream)
        self.menu_button.update(inputStream)
        self.dynamic_button.update(inputStream)


    def draw(self, sm, screen):
        # Vykreslenie pozadia celej scény
        screen.blit(self.background, (0, 0))

        # Texty pre hlasitosť zvukových efektov a hudby
        nadpis = f"Nastavenia"
        sfx_text = f"Hlasitosť zvuku: {self.sfx_volume:.1f}"
        music_text = f"Hlasitosť hudby: {self.music_volume:.1f}"

        # Zostavíme dynamický text, ktorý chceme zobraziť na tlačidle
        dynamic_text = f"\n\n{nadpis}\n\n{sfx_text}\n\n{music_text}"

        # Nastavíme text do tlačidla (ako text na pozadí tlačidla)
        self.dynamic_button.text = dynamic_text

        # Vykreslíme tlačidlo so správnym textom
        self.dynamic_button.draw(screen)
        self.increase_sfx_button.draw(screen)
        self.decrease_sfx_button.draw(screen)
        self.increase_music_button.draw(screen)
        self.decrease_music_button.draw(screen)
        self.menu_button.draw(screen)

class LevelSelectScene(Scene):
    def __init__(self):


        self.a_button = ui.ButtonUI(pygame.K_LEFT, '', 260 , 350, normal_img=r"images\UI\Arrow Left.png", hover_img=r"images\UI\Arrow Left-on.png", width=24, height=42)  # Tlačidlo pre predchádzajúcu úroveň
        self.d_button = ui.ButtonUI(pygame.K_RIGHT, '', 420-24, 350, normal_img=r"images\UI\Arrow Right.png", hover_img=r"images\UI\Arrow Right-on.png", width=24, height=42)  # Tlačidlo pre nasledujúcu úroveň


        # Definovanie tlačidiel pre výber úrovne
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, 'Menu', 65, 425, normal_img=r"images\UI\Button BG shadow.png",hover_img=r"images\UI\Button BG.png",hover_text_color=globals.MUSTARD)
        self.enter_button = ui.ButtonUI(pygame.K_RETURN, 'Spustiť', 415, 425, normal_img=r"images\UI\Button BG shadow.png",hover_img=r"images\UI\Button BG.png",hover_text_color=globals.MUSTARD)  # Tlačidlo na výber úrovne

        self.pole = ui.ButtonUI(pygame.K_AMPERSAND, '', 50, 50, normal_img=r"images\UI\Settings BG.png",width=580,height=462, align_top=True, align_center=False)

        self.background = pygame.image.load('images\menu\orig.png').convert()
        self.background = pygame.transform.scale(self.background, globals.SCREEN_SIZE)

        # Načítanie obrázkov pre jednotlivé úrovne
        self.level_images = {
            i: {
                'selected': pygame.image.load(f'images/UI/{i}.png').convert_alpha(),
                'unselected': pygame.image.load(f'images/UI/{i}-off.png').convert_alpha()
            }
            for i in range(1, 6)
        }

    def onEnter(self):
        globals.loadProgress()
        # Prehrávanie hudby pre menu
        globals.soundManager.playMusicFade('menu')

    def onExit(self):
        globals.saveProgress()

    def update(self, sm, inputStream):
        # Aktualizácia stavu tlačidiel
        self.esc.update(inputStream)
        self.a_button.update(inputStream)
        self.d_button.update(inputStream)
        self.enter_button.update(inputStream)
        self.pole.update(inputStream)


    def input(self, sm, inputStream):
        # Klávesové vstupy pre výber úrovne
        if inputStream.keyboard.isKeyPressed(pygame.K_LEFT) or inputStream.keyboard.isKeyPressed(pygame.K_a) or self.a_button.on:
            globals.curentLevel = max(globals.curentLevel - 1, 1)  # Prechod na predchádzajúcu úroveň
        if inputStream.keyboard.isKeyPressed(pygame.K_RIGHT) or inputStream.keyboard.isKeyPressed(pygame.K_d) or self.d_button.on:
            globals.curentLevel = min(globals.curentLevel + 1, globals.highestLevel)  # Prechod na nasledujúcu úroveň
        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN) or self.enter_button.on:
            level.loadLevel(globals.curentLevel)  # Načítanie vybranej úrovne
            sm.push(FadeTransitionScene([self], [GameScene()]))

        # Ukončenie a návrat do hlavného menu
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE) or self.esc.on:
            sm.pop()  # Návrat do predchádzajúcej scény (hlavné menu)
            sm.push(FadeTransitionScene([self], [MainMenuScene()]))

    def draw(self, sm, screen):

        # Nastavenie pozadia
        screen.blit(self.background, (0, 0))

        time_in_seconds = globals.levelTimers.get(globals.curentLevel, None)
        if time_in_seconds is not None and time_in_seconds != 0.00:
            minutes = int(time_in_seconds // 60)
            seconds = int(time_in_seconds % 60)
            milliseconds = int((time_in_seconds * 100) % 100)
            time_text = f"{minutes:02}:{seconds:02}:{milliseconds:02}"
        else:
            time_text = "Úroveň nedokončená"

        pole_text = f"\n\n  Výber úrovní\n\n\n\n\n\n\n  Čas: {time_text}"    

        self.pole.text = pole_text
        # Vykreslenie tlačidiel
        self.pole.draw(screen)
        self.esc.draw(screen)
        self.a_button.draw(screen)  # Vykreslenie tlačidla pre predchádzajúcu úroveň
        self.d_button.draw(screen)  # Vykreslenie tlačidla pre nasledujúcu úroveň
        self.enter_button.draw(screen)  # Vykreslenie tlačidla pre výber úrovne

        # Zobrazenie úrovní ako obrázkov
        start_x = 70  # 10 px od začiatku poľa
        end_x = 610  # 10 px od konca poľa (50 + 580 - 10)
        spacing = (end_x - start_x - 5 * 52) // 4  # Dynamický výpočet medzery medzi obrázkami
        y = 150

        for i, level_number in enumerate(range(1, globals.maxLevel + 1)):
            x = start_x + i * (52 + spacing)
            image = self.level_images[level_number]['selected'] if level_number == globals.curentLevel else self.level_images[level_number]['unselected']
            screen.blit(image, (x, y))


        


class GameScene(Scene):
    def __init__(self):
        # Inicializácia rôznych systémov hry
        self.cameraSystem = engine.CameraSystem()
        self.collectionSystem = engine.CollectionSystem()
        self.battleSystem = engine.BattleSystem()
        self.inputSystem = engine.InputSystem()
        self.physicsSystem = engine.PhysicsSystem()
        self.animationSystem = engine.AnimationSystem()

        #Časovač 
        self.display_timer = 0  # Separate display timer
        self.start_time = 0  # Time when the level starts
        # Tlačidlá pre ovládanie pohybu (W, A, D)
        self.button_a = ui.ButtonUI(pygame.K_a, 'A', 60, globals.SCREEN_SIZE[1] - 100, normal_img=r"images\UI\Inventory Cell.png",width=50,height=50,hover_text_color=globals.MUSTARD,font_path=r"font\PixelOperator8.ttf",font_size=24)
        self.button_w = ui.ButtonUI(pygame.K_w, 'W', 85, globals.SCREEN_SIZE[1] - 151, normal_img=r"images\UI\Inventory Cell.png",width=50,height=50,hover_text_color=globals.MUSTARD,font_path=r"font\PixelOperator8.ttf",font_size=24)
        self.button_d = ui.ButtonUI(pygame.K_d, 'D', 111, globals.SCREEN_SIZE[1] - 100, normal_img=r"images\UI\Inventory Cell.png",width=50,height=50,hover_text_color=globals.MUSTARD,font_path=r"font\PixelOperator8.ttf",font_size=24)

        #Hud tlačidlá
        self.time_button = ui.ButtonUI(pygame.K_AMPERSAND, '', globals.SCREEN_SIZE[0]-197, 0, normal_img=r"images\UI\Button BG.png")

    def onEnter(self):
        # Resetuj časovač
        self.display_timer = 0
        self.start_time = pygame.time.get_ticks()
        # Prehrávanie hudby pre úroveň
        globals.loadProgress()
        globals.soundManager.playMusicFade('level')

    def input(self, sm, inputStream):
        # Skontrolovanie vstupu ESC pre návrat
        if inputStream.keyboard.isKeyReleased(pygame.K_ESCAPE):
            sm.pop()
            sm.push(FadeTransitionScene([self], []))
        # Skontrolovanie výhry alebo prehry
        if globals.world.isWon():
            # Aktualizácia mapy úrovní s prístupnými úrovňami
            nextLevel = globals.curentLevel + 1
            globals.levelTimers[globals.curentLevel] = self.display_timer
            levelToUnlock = nextLevel
            globals.lastCompletedLevel = levelToUnlock
            globals.curentLevel = nextLevel
            if globals.lastCompletedLevel > globals.highestLevel:
                globals.highestLevel = globals.lastCompletedLevel

            sm.push(WinScene())
        if globals.world.isLost():
            sm.push(LoseScene())
            
    def update(self, sm, inputStream):
        # Aktualizácia systémov hry
        self.inputSystem.update(inputStream=inputStream)
        self.collectionSystem.update()
        self.battleSystem.update()
        self.physicsSystem.update()
        self.animationSystem.update()
        # Aktualizácia tlačidiel pre pohyb
        self.button_w.update(inputStream)
        self.button_a.update(inputStream)
        self.button_d.update(inputStream)


        self.time_button.update(inputStream)

        self.display_timer = (pygame.time.get_ticks() - self.start_time) / 1000


    def draw(self, sm, screen):
        # Nastavenie pozadia



        # Vykreslenie obsahu hry (entít, atď.)
        self.cameraSystem.update(screen)



        self.time_button.draw(screen)

        # Vykreslenie tlačidiel pre pohyb
        self.button_w.draw(screen)
        self.button_a.draw(screen)
        self.button_d.draw(screen)

        minutes = int(self.display_timer // 60)
        seconds = int(self.display_timer % 60)
        milliseconds = int((self.display_timer * 100) % 100)
        time_text = f"{minutes:02}:{seconds:02}:{milliseconds:02}"
        utils.drawText(screen, time_text, globals.SCREEN_SIZE[0] - 160, 10, globals.WHITE, 255,utils.PixelOperator8)



class WinScene(Scene):
    def __init__(self):
        self.alpha = 0
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, 'Výber úrovní', 50, 200, normal_img=r"images\UI\Button BG shadow.png",hover_img=r"images\UI\Button BG.png",hover_text_color=globals.MUSTARD)
        self.enter = ui.ButtonUI(pygame.K_RETURN, 'Pokračuj daľej', 50, 250, normal_img=r"images\UI\Button BG shadow.png",hover_img=r"images\UI\Button BG.png",hover_text_color=globals.MUSTARD)  # Tlačidlo pre pokračovanie
    def onEnter(self):
        # Prehrávanie hudby pri výhre
        globals.soundManager.playMusicFade('won')

    def onExit(self):
        globals.saveProgress()  # Save progress here

        # Prehrávanie hudby pri opustení scény
        globals.soundManager.playMusicFade('level')

    def update(self, sm, inputStream):
        # Zvyšovanie priehľadnosti pozadia pri vyhraní
        self.alpha = min(255, self.alpha + 10)
        self.esc.update(inputStream)  # Aktualizácia ESC tlačidla
        self.enter.update(inputStream)  # Aktualizácia tlačidla Enter

    def input(self, sm, inputStream):
        # Skontrolovanie stlačenia ESC tlačidla pre návrat
        if self.esc.on or inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.set([FadeTransitionScene([GameScene(), self], [MainMenuScene(), LevelSelectScene()])])

        # Skontrolovanie stlačenia Enter tlačidla pre pokračovanie
        if self.enter.on or inputStream.keyboard.isKeyPressed(pygame.K_RETURN):
            globals.saveProgress()  # Save progress here
            globals.loadProgress()
            level.loadLevel(globals.curentLevel)  # Load the next level
            sm.set([FadeTransitionScene([self], [LevelSelectScene(),GameScene()])]) # Prechod na nasledujúcu úroveň

    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # Vykreslenie polopriehľadného pozadia
        bgSurf = pygame.Surface(globals.SCREEN_SIZE)
        bgSurf.fill((globals.BLACK))
        utils.blit_alpha(screen, bgSurf, (0, 0), self.alpha * 0.7)

        utils.drawText(screen, 'Vyhral si!', 50, 50, globals.WHITE, self.alpha)

        # Vykreslenie tlačidiel (Esc, Pokračovať)
        self.esc.draw(screen, alpha=self.alpha)
        self.enter.draw(screen, alpha=self.alpha)


class LoseScene(Scene):
    def __init__(self):
        self.alpha = 0
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, 'Výber úrovní', 50, 200, normal_img=r"images\UI\Button BG shadow.png",hover_img=r"images\UI\Button BG.png",hover_text_color=globals.MUSTARD)
        self.restart_button = ui.ButtonUI(pygame.K_r, 'Reštart', 50, 250, normal_img=r"images\UI\Button BG shadow.png",hover_img=r"images\UI\Button BG.png",hover_text_color=globals.MUSTARD)  # Tlačidlo pre reštart úrovne

    def onEnter(self):
        # Prehrávanie hudby pri prehre
        globals.soundManager.playMusicFade('lost')

    def onExit(self):
        # Prehrávanie hudby pri opustení scény
        globals.soundManager.playMusicFade('level')

    def update(self, sm, inputStream):
        # Zvyšovanie priehľadnosti pozadia pri prehre
        self.alpha = min(255, self.alpha + 10)
        self.esc.update(inputStream)  # Aktualizácia ESC tlačidla
        self.restart_button.update(inputStream)  # Aktualizácia tlačidla pre reštart


    def input(self, sm, inputStream):
        # Skontrolovanie stlačenia ESC tlačidla pre návrat
        if self.esc.on or inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            # Skontrolujte, či je pred prechodom na novú scénu aktuálny stav správny
            if sm:
                sm.set([FadeTransitionScene([self], [LevelSelectScene()])])  # Prechod na výber úrovní

        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE):
            sm.set([FadeTransitionScene([self], [LevelSelectScene()])])


        # Skontrolovanie stlačenia tlačidla R pre reštart
        if self.restart_button.on or inputStream.keyboard.isKeyPressed(pygame.K_r):
            globals.loadProgress()
            level.loadLevel(globals.curentLevel)  # Načítanie aktualnej úrovne
            sm.set([FadeTransitionScene([self], [LevelSelectScene(),GameScene()])])  # Prechod na aktualnu úroveň

    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # Vykreslenie polopriehľadného pozadia
        bgSurf = pygame.Surface(globals.SCREEN_SIZE)
        bgSurf.fill((globals.BLACK))
        utils.blit_alpha(screen, bgSurf, (0, 0), self.alpha * 0.7)

        utils.drawText(screen, 'Prehral si, Stlač Esc', 50, 50, globals.WHITE, self.alpha)

        # Vykreslenie tlačidiel (Esc, Reštart)
        self.esc.draw(screen, alpha=self.alpha)
        self.restart_button.draw(screen, alpha=self.alpha)

class TransitionScene(Scene):
    def __init__(self, fromScenes, toScenes):
        # Inicializácia prechodovej scény s danými scenami
        self.currentPercentage = 0  # Počiatočný percentuálny pokrok prechodu
        self.fromScenes = fromScenes  # Scény, z ktorých sa prechádza
        self.toScenes = toScenes  # Scény, do ktorých sa prechádza

    def update(self, sm, inputStream):
        # Aktualizácia prechodu
        self.currentPercentage += 2  # Postupne zvyšujeme percentuálny pokrok
        if self.currentPercentage >= 100:
            sm.pop()  # Ak dosiahneme 100%, odstránime aktuálnu scénu
            for s in self.toScenes:
                sm.push(s)  # A pridáme nové scény do správcu scén
        # Aktualizácia sceny, z ktorej sa prechádza
        for scene in self.fromScenes:
            scene.update(sm, inputStream)
        # Ak existujú nové scény, aktualizujeme ich
        if len(self.toScenes) > 0:
            for scene in self.toScenes:
                scene.update(sm, inputStream)
        else:
            if len(sm.scenes) > 1:
                sm.scenes[-2].update(sm, inputStream)  # Aktualizácia predchádzajúcej scény

class FadeTransitionScene(TransitionScene):
    def draw(self, sm, screen):
        # Vykresľovanie prechodového efektu s postupným rozplynutím
        if self.currentPercentage < 50:
            # Ak prechod ešte nie je dokončený, vykreslíme scény, z ktorých sa prechádza
            for s in self.fromScenes:
                s.draw(sm, screen)
        else:
            # Ak prechod prebehol, vykreslíme nové scény
            if len(self.toScenes) == 0:
                if len(sm.scenes) > 1:
                    sm.scenes[-2].draw(sm, screen)
            else:
                for s in self.toScenes:
                    s.draw(sm, screen)

        # Vytvorenie prekrytia pre fade efekt
        overlay = pygame.Surface(globals.SCREEN_SIZE)
        # 0 = transparentné, 255 = nepriehľadné
        alpha = int(abs((255 - ((255 / 50) * self.currentPercentage))))
        overlay.set_alpha(255 - alpha)  # Nastavenie priesvitnosti
        overlay.fill(globals.BLACK)  # Naplnenie prekrytia čiernou farbou
        screen.blit(overlay, (0, 0))  # Aplikovanie prekrytia na obrazovku

class SceneManager:
    def __init__(self):
        # Inicializácia správcu scén
        self.scenes = []  # Zoznam aktívnych scén
    
    def isEmpty(self):
        # Kontrola, či zoznam scén nie je prázdny
        return len(self.scenes) == 0
    
    def enterScene(self):
        # Vstup do poslednej scény v zozname
        if len(self.scenes) > 0:
            self.scenes[-1].onEnter()

    def exitScene(self):
        # Opustenie poslednej scény v zozname
        if len(self.scenes) > 0:
            self.scenes[-1].onExit()

    def input(self, inputStream):
        # Spracovanie vstupu pre aktuálnu scénu
        if len(self.scenes) > 0:
            self.scenes[-1].input(self, inputStream)

    def update(self, inputStream):
        # Aktualizácia aktuálnej scény
        if len(self.scenes) > 0:
            self.scenes[-1].update(self, inputStream)

    def draw(self, screen):
        # Vykreslenie aktuálnej scény
        if len(self.scenes) > 0:
            self.scenes[-1].draw(self, screen)
        
        # Vykreslenie obrazovky (povinné pre zobrazenie)
        pygame.display.flip()

    def push(self, scene):
        # Pridanie novej scény na vrchol zoznamu
        self.exitScene()  # Opustenie aktuálnej scény
        self.scenes.append(scene)  # Pridanie novej scény
        self.enterScene()  # Vstup do novej scény
    
    def pop(self):
        # Odstránenie poslednej scény zo zoznamu
        self.exitScene()  # Opustenie aktuálnej scény
        self.scenes.pop()  # Odstránenie scény zo zoznamu
        self.enterScene()  # Vstup do novej (predchádzajúcej) scény

    def set(self, scenes):
        # Nastavenie nového zoznamu scén
        while len(self.scenes) > 0:
            self.pop()  # Odstránenie všetkých aktuálnych scén
        for s in scenes:
            self.push(s)  # Pridanie nových scén
