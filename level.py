import pygame
import utils
import engine
import globals

class Level:
    def __init__(self, platforms=None, winPlatforms=None, entities=None, winFunc=None, loseFunc=None, deathPlatforms=None, invisiblePlatforms=None, platform_image=None,win_image=None):
        # Inicializácia úrovne s predvolenými hodnotami, ak nie sú poskytnuté
        self.platforms = platforms if platforms is not None else []  # Platformy
        self.winPlatforms = winPlatforms if winPlatforms is not None else []  # Výherné platformy
        self.entities = entities if entities is not None else []  # Entitiy na úrovni
        self.winFunc = winFunc  # Funkcia pre výhru
        self.loseFunc = loseFunc  # Funkcia pre prehru
        self.deathPlatforms = deathPlatforms if deathPlatforms is not None else []  # Platformy, ktoré spôsobujú smrť
        self.invisiblePlatforms = invisiblePlatforms if invisiblePlatforms is not None else []  # Neviditeľné platformy
        self.platform_image = platform_image  # Pridanie parametra platform_image
        self.win_image = win_image  # Pridanie parametra win_image

    # Skontroluje, či bola úroveň vyhraná
    def isWon(self):
        if self.winFunc is None:
            return False
        return self.winFunc(self)  # Volanie funkcie na zistenie výhry
    
    # Skontroluje, či bola úroveň prehraná
    def isLost(self):
        if self.loseFunc is None:
            return False
        return self.loseFunc(self)  # Volanie funkcie na zistenie prehry


def lostLevel(level):
    # Prehra sa neberie ako prehra, ak hráč má ešte životy
    for entity in level.entities:
        if entity.type == 'player':  # Hľadá entitu typu hráč
            if entity.battle is not None:
                if entity.battle.lives > 0:  # Ak má hráč životy
                    return False
    return True  # Ak hráč nemá životy, prehra je potvrdená


def wonLevel(level):
    # Prejde všetky výherné platformy
    for platform in level.winPlatforms:
        # Skontroluje všetky entity na úrovni
        for entity in level.entities:
            if entity.type == 'player':  # Ak je entita hráč
                player_rect = entity.position.rect  # Získanie obdĺžnika pozície hráča
                # Skontroluje, či sa hráč zráža s výhernou platformou
                if player_rect.colliderect(platform):
                    return True  # Hráč vyhral
    return False  # Ak sa hráč nezrazil s výhernou platformou, nevyhral


def loadLevel(levelNumber):
    if levelNumber == 1:
        globals.world = Level(
            platforms = [
                pygame.Rect(100, 300, 400, 50),
                pygame.Rect(100, 250, 50, 50),
                pygame.Rect(450, 250, 50, 50),
                pygame.Rect(600, 300, 400, 50),
                pygame.Rect(1050, 360, 400, 50),
            ],
            winPlatforms= [
                pygame.Rect(1050, 310, 50, 50)
            ],
            deathPlatforms = [
                pygame.Rect(0, 400, 2000, 50)
            ],
            invisiblePlatforms = [  # Neviditeľná stena pozdĺž osi Y
                pygame.Rect(50, -300, 50, 600),
            ],
            entities = [
                utils.makeGranule(100,200),
                utils.makeGranule(200,250),
                utils.makeEnemy(150,275),
                utils.makeEnemy(940,275),
                utils.makeEnemy(605,275),
                globals.player1
            ],
            platform_image = pygame.image.load('images\platformy\platforma_000.png'),
            win_image = pygame.image.load('images\platformy\platforma_031.png'),
            winFunc= wonLevel,
            loseFunc= lostLevel
        )
    elif levelNumber == 2:
        globals.world = Level(
            platforms = [
                pygame.Rect(100, 300, 375, 50),
                pygame.Rect(600, 300, 400, 50),
                pygame.Rect(1100, 250, 50, 50),
                pygame.Rect(1250, 250, 50, 50),
                pygame.Rect(1400, 400, 100, 50)
            ],
            winPlatforms= [
                pygame.Rect(1450, 350, 50, 50)
            ],
            deathPlatforms = [
                pygame.Rect(0, 400, 2000, 50)
            ],
            entities = [
                utils.makeGranule(100,200),
                #Pohybujúci nepriateľ pozdĺž osi Y
                utils.makeEnemyPatrol(500, 350, axis='y', distance=200,patrol_speed= 4), 
                globals.player1
            ],
            invisiblePlatforms = [  # Neviditeľná stena pozdĺž osi Y
                pygame.Rect(50, -300, 50, 600)
            ],
            platform_image = pygame.image.load('images\platformy\platforma_001.png'),
            win_image = pygame.image.load('images\platformy\platforma_031.png'),
            winFunc= wonLevel,
            loseFunc= lostLevel
        )
    elif levelNumber == 3:
        globals.world = Level(
            platforms = [
                pygame.Rect(100, 300, 400, 50),
                pygame.Rect(350, 250, 50, 50),
                pygame.Rect(400, 200, 50, 100),
            ],
            winPlatforms= [
                pygame.Rect(650, 350, 50, 50)
            ],
            deathPlatforms = [
                pygame.Rect(0, 400, 2000, 50)
            ],
            entities = [
                utils.makeGranule(100, 200),
                # pohybujúci nepriateľ pozdĺž osi X
                utils.makeEnemyPatrol(450, 200, axis='x', distance=200),  
                globals.player1
            ],
            invisiblePlatforms = [  # Neviditeľná stena pozdĺž osi Y
                pygame.Rect(50, -300, 50, 600)
            ],
            platform_image = pygame.image.load('images\platformy\platforma_002.png'),
            win_image = pygame.image.load('images\platformy\platforma_031.png'),
            winFunc= wonLevel,
            loseFunc= lostLevel
        )

    # Resetovanie všetkých entít v úrovni
    for entity in globals.world.entities:
        entity.reset(entity)
