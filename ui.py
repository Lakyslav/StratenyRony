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
        :param normal_img: Cesta k normálnemu obrázku tlačidla.
        :param hover_img: Cesta k obrázku tlačidla pri prechode myšou (voliteľné).
        :param width: Požadovaná šírka tlačidla (voliteľné).
        :param height: Požadovaná výška tlačidla (voliteľné).
        :param align_top: Či má byť text zarovnaný hore (True) alebo na stred vertikálne (False).
        :param hover_text_color: Farba textu pri prechode myšou (voliteľné).
        :param align_center: Či má byť text zarovnaný na stred horizontálne (True) alebo zľava doprava (False).
        :param font_size: Veľkosť písma textu.
        :param font_path: Cesta k vlastnému fontu (voliteľné).
        """
        self.keyCode = keyCode
        self.text = text
        self.x = x
        self.y = y
        self.pressed = False
        self.on = False
        self.mouseHeld = False
        self.keyHeld = False
        self.align_top = align_top
        self.align_center = align_center
        self.hover_text_color = hover_text_color

        # Načítanie obrázkov
        self.normal_img = pygame.image.load(normal_img).convert_alpha()
        self.hover_img = pygame.image.load(hover_img).convert_alpha() if hover_img else self.normal_img

        # Nastavenie veľkosti tlačidla
        self.width = width if width else self.normal_img.get_width()
        self.height = height if height else self.normal_img.get_height()

        self.normal_img = pygame.transform.scale(self.normal_img, (self.width, self.height))
        self.hover_img = pygame.transform.scale(self.hover_img, (self.width, self.height))
        self.image = self.normal_img

        # Nastavenie písma
        self.font_size = font_size
        self.font_path = font_path
        self.font = pygame.font.Font(font_path, font_size) if font_path else pygame.font.Font(None, font_size)

    def set_font(self, font_path, font_size):
        """Nastaví nový font a veľkosť textu."""
        self.font = pygame.font.Font(font_path, font_size)

    def update(self, inputStream):
        """Aktualizuje stav tlačidla na základe vstupu používateľa."""
        self.pressed = inputStream.keyboard.isKeyDown(self.keyCode)
        self.keyHeld = self.pressed
        self.on, self.mouseHeld = self.check_mouse_input(inputStream)

        mouse_x, mouse_y = inputStream.mouse.getPosition()
        self.image = self.hover_img if self.is_mouse_over(mouse_x, mouse_y) or self.pressed else self.normal_img

    def is_mouse_over(self, mouse_x, mouse_y):
        """Skontroluje, či je myš nad tlačidlom."""
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height

    def check_mouse_input(self, inputStream):
        """Skontroluje, či je tlačidlo kliknuté myšou."""
        mouse_x, mouse_y = inputStream.mouse.getPosition()
        mouse_over_button = self.is_mouse_over(mouse_x, mouse_y)
        mouse_held = inputStream.mouse.isButtonDown(0)

        if mouse_over_button and mouse_held:
            return False, True
        elif mouse_over_button and inputStream.mouse.isButtonReleased(0):
            return True, False
        return False, False

    def draw(self, screen, alpha=255):
        """Nakreslí tlačidlo s textom."""
        screen.blit(self.image, (self.x, self.y))

        lines = self.text.split('\n')
        total_text_height = sum(self.font.get_height() for line in lines)

        if self.align_top:
            text_y = self.y
        else:
            text_y = self.y + (self.height - total_text_height) // 2

        mouse_x, mouse_y = pygame.mouse.get_pos()
        is_hovered_or_pressed = self.is_mouse_over(mouse_x, mouse_y) or self.pressed

        text_color = self.hover_text_color if is_hovered_or_pressed and self.hover_text_color else globals.WHITE

        for line in lines:
            text_surface = self.font.render(line, True, text_color)
            text_width, text_height = text_surface.get_size()

            text_x = self.x + (self.width - text_width) // 2 if self.align_center else self.x + 10
            screen.blit(text_surface, (text_x, text_y))
            text_y += text_height
