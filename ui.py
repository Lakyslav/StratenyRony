import pygame
import globals
import utils

class ButtonUI:
    def __init__(self, keyCode, text, x, y, normal_img, hover_img=None, width=None, height=None, align_top=False, hover_text_color=None, align_center=True, font_size=30, font_path=None):
        """
        Inicializuje tlačidlo s možnosťou úpravy fontu a veľkosti textu.
        
        :param keyCode: Kláves priradený k tlačidlu.
        :param text: Text, ktorý sa zobrazí na tlačidle.
        :param x: X-ová súradnica tlačidla.
        :param y: Y-ová súradnica tlačidla.
        :param normal_img: Cesta k obrázku tlačidla v normálnom stave.
        :param hover_img: Cesta k obrázku tlačidla pri prechode myšou (voliteľné).
        :param width: Šírka tlačidla (voliteľné, ak nie je zadané, použije sa veľkosť obrázka).
        :param height: Výška tlačidla (voliteľné, ak nie je zadané, použije sa veľkosť obrázka).
        :param align_top: Ak je True, text bude zarovnaný hore, inak na stred vertikálne.
        :param hover_text_color: Farba textu pri prechode myšou (voliteľné).
        :param align_center: Ak je True, text bude zarovnaný na stred horizontálne.
        :param font_size: Veľkosť písma textu.
        :param font_path: Cesta k vlastnému fontu (voliteľné).
        """
        self.keyCode = keyCode  # Klávesová skratka priradená tlačidlu
        self.text = text  # Text, ktorý sa zobrazí na tlačidle
        self.x = x  # X-ová súradnica tlačidla
        self.y = y  # Y-ová súradnica tlačidla
        self.pressed = False  # Indikátor, či je tlačidlo stlačené
        self.on = False  # Indikátor, či bolo tlačidlo aktivované
        self.mouseHeld = False  # Indikátor, či je tlačidlo držané myšou
        self.keyHeld = False  # Indikátor, či je tlačidlo držané klávesnicou
        self.align_top = align_top  # Ak je True, text bude zarovnaný hore
        self.align_center = align_center  # Ak je True, text bude zarovnaný na stred
        self.hover_text_color = hover_text_color  # Farba textu pri prechode myšou

        # Načítanie obrázkov tlačidla
        self.normal_img = pygame.image.load(normal_img).convert_alpha()  # Normálny stav tlačidla
        self.hover_img = pygame.image.load(hover_img).convert_alpha() if hover_img else self.normal_img  # Hover efekt tlačidla

        # Nastavenie šírky a výšky tlačidla (ak nie sú zadané, použije sa veľkosť obrázka)
        self.width = width if width else self.normal_img.get_width()
        self.height = height if height else self.normal_img.get_height()

        # Zmena veľkosti obrázkov tlačidla na zadané rozmery
        self.normal_img = pygame.transform.scale(self.normal_img, (self.width, self.height))
        self.hover_img = pygame.transform.scale(self.hover_img, (self.width, self.height))
        self.image = self.normal_img  # Aktuálny obrázok tlačidla (normálny alebo hover)

        # Nastavenie fontu
        self.font_size = font_size  # Veľkosť písma
        self.font_path = font_path  # Cesta k vlastnému fontu
        self.font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.Font(None, font_size)  # Načítanie fontu

    def set_font(self, font_path, font_size):
        """Nastaví nový font a veľkosť textu."""
        self.font = pygame.font.Font(font_path, font_size)

    def update(self, inputStream):
        """
        Aktualizuje stav tlačidla na základe vstupu používateľa (klávesnica a myš).
        
        :param inputStream: Vstupný prúd pre detekciu vstupov (klávesnica a myš).
        """
        self.pressed = inputStream.keyboard.isKeyDown(self.keyCode)  # Kontrola, či je priradený kláves stlačený
        self.keyHeld = self.pressed  # Aktualizácia stavu držaného tlačidla
        self.on, self.mouseHeld = self.check_mouse_input(inputStream)  # Kontrola, či bolo tlačidlo kliknuté myšou

        # Získanie pozície myši
        mouse_x, mouse_y = inputStream.mouse.getPosition()

        # Zmena obrázka tlačidla podľa toho, či je nad ním myš alebo je stlačené
        self.image = self.hover_img if self.is_mouse_over(mouse_x, mouse_y) or self.pressed else self.normal_img

    def is_mouse_over(self, mouse_x, mouse_y):
        """
        Skontroluje, či je myš nad tlačidlom.
        
        :param mouse_x: X-ová pozícia myši.
        :param mouse_y: Y-ová pozícia myši.
        :return: True, ak je myš nad tlačidlom, inak False.
        """
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

    def check_mouse_input(self, inputStream):
        """
        Skontroluje, či bolo tlačidlo stlačené alebo držané myšou.
        
        :param inputStream: Vstupný prúd na kontrolu stavu myši.
        :return: (bool, bool) - Prvý parameter označuje kliknutie, druhý označuje držanie myši.
        """
        mouse_x, mouse_y = inputStream.mouse.getPosition()
        mouse_over_button = self.is_mouse_over(mouse_x, mouse_y)
        mouse_held = inputStream.mouse.isButtonDown(0)  # Skontroluje, či je stlačené ľavé tlačidlo myši

        # Ak je myš nad tlačidlom a tlačidlo myši je držané
        if mouse_over_button and mouse_held:
            return False, True
        # Ak je myš nad tlačidlom a tlačidlo bolo práve uvoľnené
        elif mouse_over_button and inputStream.mouse.isButtonReleased(0):
            return True, False
        return False, False

    def draw(self, screen, alpha=255):
        """
        Nakreslí tlačidlo na obrazovku.
        
        :param screen: Obrazovka, na ktorú sa tlačidlo vykreslí.
        :param alpha: Priehľadnosť tlačidla (predvolená hodnota je 255 = nepriehľadné).
        """
        screen.blit(self.image, (self.x, self.y))  # Vykreslenie obrázka tlačidla

        # Rozdelenie textu na viaceré riadky, ak obsahuje znak nového riadku '\n'
        lines = self.text.split('\n')
        total_text_height = sum(self.font.get_height() for line in lines)

        # Nastavenie pozície textu v závislosti od zarovnania
        if self.align_top:
            text_y = self.y
        else:
            text_y = self.y + (self.height - total_text_height) // 2

        # Získanie pozície myši na zistenie, či je tlačidlo v stave hover
        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered_or_pressed = self.is_mouse_over(mouse_x, mouse_y) or self.pressed

        # Nastavenie farby textu (ak je definovaná iná farba pre hover, použije sa pri prechode myšou)
        text_color = self.hover_text_color if is_hovered_or_pressed and self.hover_text_color else globals.WHITE

        # Vykreslenie textu na tlačidlo
        for line in lines:
            text_surface = self.font.render(line, True, text_color)
            text_width, text_height = text_surface.get_size()

            text_x = self.x + (self.width - text_width) // 2 if self.align_center else self.x + 10
            screen.blit(text_surface, (text_x, text_y))
            text_y += text_height
