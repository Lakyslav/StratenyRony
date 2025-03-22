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
        self.currentButtonStates = ()  # Initialize as empty tuple
        self.previousButtonStates = ()
        self.x, self.y = 0, 0

    def processInput(self):
        self.previousButtonStates = self.currentButtonStates
        self.currentButtonStates = pygame.mouse.get_pressed()  # Returns tuple of 5 elements
        self.x, self.y = pygame.mouse.get_pos()

    def isButtonDown(self, button):
        if button < 0 or button >= len(self.currentButtonStates):
            return False
        return self.currentButtonStates[button] == 1

    def isButtonPressed(self, button):
        # Check if button index is valid for both current and previous states
        if (button < 0 
            or button >= len(self.currentButtonStates) 
            or button >= len(self.previousButtonStates)):
            return False
        return self.currentButtonStates[button] and not self.previousButtonStates[button]

    def isButtonReleased(self, button):
        if (button < 0 
            or button >= len(self.currentButtonStates) 
            or button >= len(self.previousButtonStates)):
            return False
        return not self.currentButtonStates[button] and self.previousButtonStates[button]

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