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
        self.enter = ui.ButtonUI(pygame.K_RETURN, '[Výber úrovne]', 50, 200)
        self.settings = ui.ButtonUI(pygame.K_s, '[Nastavenia]', 50, 250)
        self.tutorial_button = ui.ButtonUI(pygame.K_t, '[Návod]', 50, 300)  # Tlačidlo pre návod
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Ukončiť hru]', 50, 350)

        self.background = pygame.image.load('images\menu\orig.png').convert()
        self.background = pygame.transform.scale(self.background, globals.SCREEN_SIZE)


    def onEnter(self):
        # Hranie hudby pri vstupe do hlavného menu
        globals.soundManager.playMusicFade('menu')


        
    def input(self, sm, inputStream):
        # Klávesové vstupy pre rôzne akcie
        if inputStream.keyboard.isKeyPressed(pygame.K_RETURN) or self.enter.on:
            sm.push(FadeTransitionScene([self], [LevelSelectScene()]))  # Prechod na výber úrovne
        if inputStream.keyboard.isKeyPressed(pygame.K_s) or self.settings.on:
            sm.push(FadeTransitionScene([self], [SettingsScene()]))  # Prechod na nastavenia
        if inputStream.keyboard.isKeyPressed(pygame.K_t) or self.tutorial_button.on:
            sm.push(FadeTransitionScene([self], [TutorialScene()]))  # Prechod na návod
        if inputStream.keyboard.isKeyPressed(pygame.K_ESCAPE) or self.esc.on:
            sys.exit()
    def update(self, sm, inputStream):
        # Aktualizácia stavu tlačidiel
        self.enter.update(inputStream)
        self.settings.update(inputStream)
        self.tutorial_button.update(inputStream)  # Aktualizácia tlačidla pre návod
        self.esc.update(inputStream)

    def draw(self, sm, screen):
        screen.blit(self.background, (0, 0))
        # Nastavenie pozadia a vykreslenie názvu menu
        utils.drawText(screen, 'STRATENÝ RONY', 50, 50, globals.DARK_GREY, 255)

        # Vykreslenie tlačidiel v menu
        self.enter.draw(screen)
        self.settings.draw(screen)
        self.tutorial_button.draw(screen)  # Vykreslenie tlačidla pre návod
        self.esc.draw(screen)

        

# Scéna s návodom
class TutorialScene(Scene):
    def __init__(self):
        # Tlačidlo na návrat do hlavného menu
        self.menu_button = ui.ButtonUI(pygame.K_ESCAPE, '[Návrat na menu]', 450, 400)
        
        # Fonty pre texty inštrukcií
        self.title_font = pygame.font.Font(None, 40)
        self.option_font = pygame.font.Font(None, 30)
        
        # Texty s ovládaním
        self.controls_text = [
            "Ovládanie:",
            "W - skok",
            "A - pohyb doľava",
            "D - pohyb doprava",
            "Q - Priblíženie",
            "E - Odialenie",
        ]

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

    def draw(self, sm, screen):
        screen.blit(self.background, (0, 0))

        # Vykreslenie názvu návodu
        title_surface = self.title_font.render("Návod na ovládanie", True, globals.DARK_GREY)
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 50))

        # Vykreslenie inštrukcií na ovládanie
        y_offset = 100
        for line in self.controls_text:
            control_surface = self.option_font.render(line, True, globals.DARK_GREY)
            screen.blit(control_surface, (screen.get_width() // 2 - control_surface.get_width() // 2, y_offset))
            y_offset += 40  # Nastavenie rozostupu medzi riadkami

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
        self.increase_sfx_button = ui.ButtonUI(pygame.K_w, '[+]', 450, 200)
        self.decrease_sfx_button = ui.ButtonUI(pygame.K_s, '[-]', 500, 200)

        self.increase_music_button = ui.ButtonUI(pygame.K_UP, '[+]', 450, 300)
        self.decrease_music_button = ui.ButtonUI(pygame.K_DOWN, '[-]', 500, 300)

        self.menu_button = ui.ButtonUI(pygame.K_ESCAPE, '[Menu]', 450, 400)

        # Fonty pre texty
        self.title_font = pygame.font.Font(None, 40)
        self.option_font = pygame.font.Font(None, 30)

        self.background = pygame.image.load('images\menu\orig.png').convert()
        self.background = pygame.transform.scale(self.background, globals.SCREEN_SIZE)

    def input(self, inputStream):
        if self.increase_sfx_button.is_pressed():
            self.sfx_volume = min(self.sfx_volume + 0.1, 1.0)
            globals.soundManager.setSoundVolume(self.sfx_volume)
        
        if self.decrease_sfx_button.is_pressed():
            self.sfx_volume = max(self.sfx_volume - 0.1, 0.0)
            globals.soundManager.setSoundVolume(self.sfx_volume)

        if self.increase_music_button.is_pressed():
            self.music_volume = min(self.music_volume + 0.1, 1.0)
            globals.soundManager.setMusicVolume(self.music_volume)

        if self.decrease_music_button.is_pressed():
            self.music_volume = max(self.music_volume - 0.1, 0.0)
            globals.soundManager.setMusicVolume(self.music_volume)
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

    def draw(self, sm, screen):
        screen.blit(self.background, (0, 0))

        # Vykreslenie názvu nastavení
        title_surface = self.title_font.render("Nastavenia", True, (255, 255, 255))
        screen.blit(title_surface, (screen.get_width() // 2 - title_surface.get_width() // 2, 50))

        # Texty pre hlasitosť zvukových efektov a hudby
        sfx_text = f"Hlasitosť zvuku: {self.sfx_volume:.1f}"
        music_text = f"Hlasitosť hudby: {self.music_volume:.1f}"

        sfx_surface = self.option_font.render(sfx_text, True, (255, 255, 255))
        music_surface = self.option_font.render(music_text, True, (255, 255, 255))

        screen.blit(sfx_surface, (200, 200))
        screen.blit(music_surface, (200, 300))

        # Vykreslenie tlačidiel
        self.increase_sfx_button.draw(screen)
        self.decrease_sfx_button.draw(screen)
        self.increase_music_button.draw(screen)
        self.decrease_music_button.draw(screen)
        self.menu_button.draw(screen)

class LevelSelectScene(Scene):
    def __init__(self):
        # Definovanie tlačidiel pre výber úrovne
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Odísť do menu]', 50, 300)
        self.a_button = ui.ButtonUI(pygame.K_a, '[A]', 50, 250)  # Tlačidlo pre predchádzajúcu úroveň
        self.d_button = ui.ButtonUI(pygame.K_d, '[D]', 150, 250)  # Tlačidlo pre nasledujúcu úroveň
        self.enter_button = ui.ButtonUI(pygame.K_RETURN, '[Spustiť]', 50, 350)  # Tlačidlo na výber úrovne

        self.background = pygame.image.load('images\menu\orig.png').convert()
        self.background = pygame.transform.scale(self.background, globals.SCREEN_SIZE)

    def onEnter(self):
        # Prehrávanie hudby pre menu
        globals.soundManager.playMusicFade('menu')

    def update(self, sm, inputStream):
        # Aktualizácia stavu tlačidiel
        self.esc.update(inputStream)
        self.a_button.update(inputStream)
        self.d_button.update(inputStream)
        self.enter_button.update(inputStream)

    def input(self, sm, inputStream):
        # Klávesové vstupy pre výber úrovne
        if inputStream.keyboard.isKeyPressed(pygame.K_a) or self.a_button.on:
            globals.curentLevel = max(globals.curentLevel - 1, 1)  # Prechod na predchádzajúcu úroveň
        if inputStream.keyboard.isKeyPressed(pygame.K_d) or self.d_button.on:
            globals.curentLevel = min(globals.curentLevel + 1, globals.lastCompletedLevel)  # Prechod na nasledujúcu úroveň
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
        utils.drawText(screen, 'Výber úrovní', 50, 50, globals.DARK_GREY, 255)
        
        # Vykreslenie tlačidiel
        self.esc.draw(screen)
        self.a_button.draw(screen)  # Vykreslenie tlačidla pre predchádzajúcu úroveň
        self.d_button.draw(screen)  # Vykreslenie tlačidla pre nasledujúcu úroveň
        self.enter_button.draw(screen)  # Vykreslenie tlačidla pre výber úrovne

        # Zobrazenie úrovní
        for levelNumber in range(1, globals.maxLevel + 1):
            c = globals.WHITE
            if levelNumber == globals.curentLevel:
                c = globals.GREEN
            a = 255
            if levelNumber > globals.lastCompletedLevel:
                a = 100
            utils.drawText(screen, str(levelNumber), levelNumber * 100, 100, c, a)


class GameScene(Scene):
    def __init__(self):
        # Inicializácia rôznych systémov hry
        self.cameraSystem = engine.CameraSystem()
        self.collectionSystem = engine.CollectionSystem()
        self.battleSystem = engine.BattleSystem()
        self.inputSystem = engine.InputSystem()
        self.physicsSystem = engine.PhysicsSystem()
        self.animationSystem = engine.AnimationSystem()
        # Tlačidlá pre ovládanie pohybu (W, A, D)
        self.button_a = ui.ButtonUI(pygame.K_a, '[A]', 10, globals.SCREEN_SIZE[1] - 100)
        self.button_w = ui.ButtonUI(pygame.K_w, '[W]', 45, globals.SCREEN_SIZE[1] - 120)
        self.button_d = ui.ButtonUI(pygame.K_d, '[D]', 85, globals.SCREEN_SIZE[1] - 100)

    def onEnter(self):
        # Prehrávanie hudby pre úroveň
        globals.soundManager.playMusicFade('level')
        
    def input(self, sm, inputStream):
        # Skontrolovanie vstupu ESC pre návrat
        if inputStream.keyboard.isKeyReleased(pygame.K_ESCAPE):
            sm.pop()
            sm.push(FadeTransitionScene([self], []))
        # Skontrolovanie výhry alebo prehry
        if globals.world.isWon():
            # Aktualizácia mapy úrovní s prístupnými úrovňami
            nextLevel = min(globals.curentLevel + 1, globals.maxLevel)
            levelToUnlock = max(nextLevel, globals.lastCompletedLevel)
            globals.lastCompletedLevel = levelToUnlock
            globals.curentLevel = nextLevel
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

    def draw(self, sm, screen):
        # Nastavenie pozadia
        screen.fill(globals.DARK_GREY)

        # Vykreslenie obsahu hry (entít, atď.)
        self.cameraSystem.update(screen)

        # Vykreslenie tlačidiel pre pohyb
        self.button_w.draw(screen)
        self.button_a.draw(screen)
        self.button_d.draw(screen)


class WinScene(Scene):
    def __init__(self):
        self.alpha = 0
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Návrat na výber úrovní]', 50, 200)
        self.enter = ui.ButtonUI(pygame.K_RETURN, '[Pokračuj daľej]', 50, 250)  # Tlačidlo pre pokračovanie

    def onEnter(self):
        # Prehrávanie hudby pri výhre
        globals.soundManager.playMusicFade('won')

    def onExit(self):
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
            level.loadLevel(globals.curentLevel)  # Načítanie nasledujúcej úrovne
            sm.set([FadeTransitionScene([self], [LevelSelectScene(),GameScene()])])  # Prechod na nasledujúcu úroveň

    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # Vykreslenie polopriehľadného pozadia
        bgSurf = pygame.Surface((830, 830))
        bgSurf.fill((globals.BLACK))
        utils.blit_alpha(screen, bgSurf, (0, 0), self.alpha * 0.7)

        utils.drawText(screen, 'Vyhral si!', 50, 50, globals.WHITE, self.alpha)

        # Vykreslenie tlačidiel (Esc, Pokračovať)
        self.esc.draw(screen, alpha=self.alpha)
        self.enter.draw(screen, alpha=self.alpha)


class LoseScene(Scene):
    def __init__(self):
        self.alpha = 0
        self.esc = ui.ButtonUI(pygame.K_ESCAPE, '[Návrat na výber úrovní]', 50, 200)
        self.restart_button = ui.ButtonUI(pygame.K_r, '[Reštart]', 50, 250)  # Tlačidlo pre reštart úrovne

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
            print("ESC stlačený")
            if sm:
                print("Sm existuje, prechádzam na výber úrovní")
            sm.set([FadeTransitionScene([self], [LevelSelectScene()])])


        # Skontrolovanie stlačenia tlačidla R pre reštart
        if self.restart_button.on or inputStream.keyboard.isKeyPressed(pygame.K_r):
            level.loadLevel(globals.curentLevel)  # Načítanie aktualnej úrovne
            sm.set([FadeTransitionScene([self], [LevelSelectScene(),GameScene()])])  # Prechod na aktualnu úroveň

    def draw(self, sm, screen):
        if len(sm.scenes) > 1:
            sm.scenes[-2].draw(sm, screen)

        # Vykreslenie polopriehľadného pozadia
        bgSurf = pygame.Surface((700, 500))
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
