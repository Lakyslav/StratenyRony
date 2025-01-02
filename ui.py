import pygame
import globals
import utils

class ButtonUI:
    def __init__(self, keyCode, text, x, y):
        self.keyCode = keyCode  # Klávesa, ktorá aktivuje tlačidlo
        self.text = text  # Text tlačidla
        self.x = x  # X-ová pozícia tlačidla
        self.y = y  # Y-ová pozícia tlačidla
        self.pressed = False  # Stav, či je tlačidlo stlačené
        self.on = False  # Stav, či je tlačidlo aktivované
        self.mouseHeld = False  # Stav, či je tlačidlo držané myšou
        self.keyHeld = False  # Stav, či je tlačidlo držané klávesnicou
        font = pygame.font.Font(None, 36)  # Nastavenie písma
        self.width = font.size(self.text)[0]  # Šírka tlačidla na základe textu
        self.height = font.get_height() + 1  # Výška tlačidla na základe textu

    def update(self, inputStream):
        """
        Aktualizuje stav tlačidla podľa vstupu od užívateľa.
        """
        self.pressed = inputStream.keyboard.isKeyDown(self.keyCode)  # Skontroluje, či je stlačený príslušný kláves
        self.keyHeld = self.pressed  # Uloží stav, či je kláves držaný
        self.on, self.mouseHeld = self.check_mouse_input(inputStream)  # Skontroluje stav myši

    def check_mouse_input(self, inputStream):
        """
        Skontroluje, či je myš nad tlačidlom a či je tlačidlo stlačené.
        """
        mouse_x, mouse_y = inputStream.mouse.getPosition()  # Získanie pozície myši
        button_left = self.x  # Ľavý okraj tlačidla
        button_right = self.x + self.width  # Pravý okraj tlačidla
        button_top = self.y  # Horný okraj tlačidla
        button_bottom = self.y + self.height  # Spodný okraj tlačidla
        
        # Skontroluje, či je myš nad tlačidlom
        mouse_over_button = (button_left <= mouse_x <= button_right) and (button_top <= mouse_y <= button_bottom)
        # Skontroluje, či je tlačidlo stlačené
        mouse_held = inputStream.mouse.isButtonDown(0)

        if mouse_over_button and mouse_held:
            return False, True  # Tlačidlo nie je stlačené, ale je držané
        elif mouse_over_button and inputStream.mouse.isButtonReleased(0):
            return True, False  # Tlačidlo je stlačené a uvoľnené
        return False, False  # Inak nie je stlačené ani držané

    def draw(self, screen, alpha=255):
        """
        Vykreslí tlačidlo na obrazovku.
        """
        # Nastaví farbu tlačidla podľa toho, či je stlačené alebo myš drží tlačidlo
        colour = globals.GREEN if self.mouseHeld or self.keyHeld else globals.WHITE
        # Vykreslí text na tlačidlo
        utils.drawText(screen, self.text, self.x, self.y, colour, alpha)
