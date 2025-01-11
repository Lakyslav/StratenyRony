import pygame
import utils
import engine
import globals

class Level:
    def __init__(self, platforms=None, winPlatforms=None, entities=None, winFunc=None, loseFunc=None, deathPlatforms=None, invisiblePlatforms=None, platform_image=None,win_image=None, backgrounds=None):
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
        self.backgrounds = backgrounds if backgrounds is not None else []

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
            backgrounds = [

                (pygame.image.load(r'images/pozadia/level1_1.png').convert_alpha(), 0.2),
                (pygame.image.load(r'images/pozadia/level1_2.png').convert_alpha(), 0.3),
                (pygame.image.load(r'images/pozadia/level1_10.png').convert_alpha(), 0.8),
                (pygame.image.load(r'images/pozadia/level1_3.png').convert_alpha(), 0.5),
                (pygame.image.load(r'images/pozadia/level1_5.png').convert_alpha(), 0.5),
                (pygame.image.load(r'images/pozadia/level1_6.png').convert_alpha(), 0.5),
                (pygame.image.load(r'images/pozadia/level1_7.png').convert_alpha(), 0.5),
                (pygame.image.load(r'images/pozadia/level1_8.png').convert_alpha(), 1),

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
                        backgrounds = [

                (pygame.image.load(r'images/pozadia/level2_1.png').convert_alpha(), 0.2),
                (pygame.image.load(r'images/pozadia/level2_2.png').convert_alpha(), 0.5),
                (pygame.image.load(r'images/pozadia/level2_3.png').convert_alpha(), 0.7),
                (pygame.image.load(r'images/pozadia/level2_4.png').convert_alpha(), 1),
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
                pygame.Rect(600, 150, 400, 50),
                pygame.Rect(1050, 275, 200, 50),
                pygame.Rect(1300, 225, 100, 50),
                pygame.Rect(1450, 175, 100, 50),
                pygame.Rect(1750, 125, 200, 50),
                pygame.Rect(2000, 75, 150, 50),
                pygame.Rect(2200, 200, 250, 50),
                pygame.Rect(2500, 270, 300, 50),
                pygame.Rect(2800, 200, 200, 50),
                pygame.Rect(3000, 150, 200, 50),
                pygame.Rect(3200, 100, 150, 50),
                pygame.Rect(3400, 50, 250, 50),
            ],
            winPlatforms= [
                pygame.Rect(3500, 0, 50, 50)
            ],
            deathPlatforms = [
                pygame.Rect(0, 400, 2000, 50)
            ],
            entities = [
                utils.makeGranule(100, 200),
                utils.makeEnemyPatrol(450, 200, axis='x', distance=200),
                utils.makeEnemyPatrol(750, 50, axis='y', distance=300, patrol_speed=3),
                utils.makeEnemyPatrol(1625, 200, axis='y', distance=350, patrol_speed=4),
                utils.makeEnemyPatrol(1750, 200, axis='x', distance=250, patrol_speed=3),
                utils.makeEnemy(1850, 100),
                utils.makeEnemy(2545, 250),
                utils.makeEnemy(2850, 175),
                utils.makeEnemy(3050, 125),
                utils.makeEnemy(3250, 75),
                globals.player1
            ],
            invisiblePlatforms = [
                pygame.Rect(50, -300, 50, 600)
            ],
            backgrounds = [
                (pygame.image.load(r'images/pozadia/level3_1.png').convert_alpha(), 0.2),
                (pygame.image.load(r'images/pozadia/level3_2.png').convert_alpha(), 0.3),
                (pygame.image.load(r'images/pozadia/level3_3.png').convert_alpha(), 0.5),
                (pygame.image.load(r'images/pozadia/level3_4.png').convert_alpha(), 0.6),
                (pygame.image.load(r'images/pozadia/level3_5.png').convert_alpha(), 0.8),
                (pygame.image.load(r'images/pozadia/level3_6.png').convert_alpha(), 1),
            ],
            platform_image = pygame.image.load('images\platformy\platforma_002.png'),
            win_image = pygame.image.load('images\platformy\platforma_031.png'),
            winFunc= wonLevel,
            loseFunc= lostLevel
        )




    # Resetovanie všetkých entít v úrovni
    for entity in globals.world.entities:
        entity.reset(entity)
