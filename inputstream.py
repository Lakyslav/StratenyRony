import pygame
import engine
import utils
import level
import scene
import globals

# Trieda na spracovanie vstupu z klávesnice
class Keyboard:
    def __init__(self):
        # Uchovávanie aktuálnych a predchádzajúcich stavov kláves
        self.currentKeyStates = None  # Aktuálny stav kláves
        self.previousKeyStates = None  # Predchádzajúci stav kláves
    
    # Spracovanie vstupu z klávesnice
    def processInput(self):
        # Uloženie aktuálnych stavov kláves do predchádzajúcich stavov
        self.previousKeyStates = self.currentKeyStates
        # Získanie aktuálneho stavu všetkých kláves
        self.currentKeyStates = pygame.key.get_pressed()

    # Kontrola, či je daná klávesa stlačená
    def isKeyDown(self, keyCode):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        # Vráti True, ak je klávesa stlačená
        return self.currentKeyStates[keyCode] == True
    
    # Kontrola, či bola klávesa práve stlačená 
    def isKeyPressed(self, keyCode):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        # Vráti True, ak bola klávesa práve stlačená
        return self.currentKeyStates[keyCode] == True and self.previousKeyStates[keyCode] == False
    
    # Kontrola, či bola klávesa práve uvoľnená 
    def isKeyReleased(self, keyCode):
        if self.currentKeyStates is None or self.previousKeyStates is None:
            return False
        # Vráti True, ak bola klávesa práve uvoľnená
        return self.currentKeyStates[keyCode] == False and self.previousKeyStates[keyCode] == True


# Trieda na spracovanie vstupu myši
class Mouse:
    def __init__(self):
        # Uchovávanie aktuálnych a predchádzajúcich stavov myši
        self.currentButtonStates = None  # Aktuálny stav tlačidiel myši
        self.previousButtonStates = None  # Predchádzajúci stav tlačidiel myši
        self.x, self.y = 0, 0  # Súradnice myši

    # Spracovanie vstupu myši
    def processInput(self):
        # Uloženie aktuálnych stavov tlačidiel myši do predchádzajúcich stavov
        self.previousButtonStates = self.currentButtonStates
        # Získanie aktuálnych stavov tlačidiel myši
        self.currentButtonStates = pygame.mouse.get_pressed()
        # Získanie aktuálnych súradníc myši
        self.x, self.y = pygame.mouse.get_pos()

    # Kontrola, či je dané tlačidlo myši stlačené
    def isButtonDown(self, button):
        if self.currentButtonStates is None or self.previousButtonStates is None:
            return False
        # Vráti True, ak je tlačidlo myši stlačené
        return self.currentButtonStates[button] == 1

    # Kontrola, či bolo tlačidlo myši práve stlačené
    def isButtonPressed(self, button):
        if self.currentButtonStates is None or self.previousButtonStates is None:
            return False
        # Vráti True, ak bolo tlačidlo myši práve stlačené
        return self.currentButtonStates[button] == 1 and self.previousButtonStates[button] == 0

    # Kontrola, či bolo tlačidlo myši práve uvoľnené
    def isButtonReleased(self, button):
        if self.currentButtonStates is None or self.previousButtonStates is None:
            return False
        # Vráti True, ak bolo tlačidlo myši práve uvoľnené
        return self.currentButtonStates[button] == 0 and self.previousButtonStates[button] == 1

    # Získanie aktuálnych súradníc myši
    def getPosition(self):
        return self.x, self.y


# Trieda na spracovanie vstupu 
class InputStream:
    def __init__(self):
        # Inštancia triedy Keyboard na spracovanie vstupu z klávesnice
        self.keyboard = Keyboard()
        # Inštancia triedy Mouse na spracovanie vstupu z myši
        self.mouse = Mouse()
    
    # Spracovanie vstupu
    def processInput(self):
        # Volanie metódy na spracovanie vstupu
        self.keyboard.processInput()
        self.mouse.processInput()
