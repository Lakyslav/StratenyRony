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
                # Starting platform with granules
                pygame.Rect(100, 250, 200, 50),

                # Platform after a jump
                pygame.Rect(400, 180, 200, 50),

                # Platform with an enemy
                pygame.Rect(800, 180, 200, 50),

                # Platform after the bird obstacle
                pygame.Rect(1200, 180, 200, 50),

                # Platforms leading to the goal
                pygame.Rect(1600, 130, 200, 50),
                pygame.Rect(2000, 80, 200, 50),
                pygame.Rect(2350, 30, 250, 50),
                pygame.Rect(2300, 200, 150, 50),
                pygame.Rect(2700, 250, 400, 50),
            ],
            winPlatforms= [
                pygame.Rect(3100, 200, 50, 50)  # Goal platform
            ],
            deathPlatforms = [
                pygame.Rect(0, 1000, 4000, 50)  # Death floor
            ],
            entities = [
                # Starting granules
                utils.makeGranule(200, 180),
                utils.makeGranule(200, 200),
                utils.makeGranule(250, 200),

                # Enemy on the second platform
                utils.makeEnemy(850, 160),

                # Bird obstacle
                utils.makeEnemyPatrol(1400, 150, axis='y', distance=400, patrol_speed=4),
                utils.makeEnemyPatrol(2600, 90, axis='x', distance=600, patrol_speed=6),

                utils.makeGranule(2890,25),
                # Player
                globals.player1
            ],
            invisiblePlatforms = [  # Invisible walls for the level
                pygame.Rect(50, -300, 50, 1200),
            ],
            backgrounds = [
                # zdroj obrázka a rýchlosť pohybu (čím menšie číslo tým rýchlejšie)
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
                pygame.Rect(100, 300, 375, 150),  #1
                pygame.Rect(600, 300, 400, 150),  #2
                pygame.Rect(1100, 250, 50, 50),   #3
                pygame.Rect(1175, 400, 50, 150),  #4 
                pygame.Rect(1250, 250, 50, 50),   #5
                pygame.Rect(1380, 400, 100, 150), #6
                pygame.Rect(1575, 350, 200, 150), #7
                pygame.Rect(1850, 300, 100, 150), #8
                pygame.Rect(2130, 250, 100, 250), #9
                pygame.Rect(2275, 200, 150, 250), #10
                pygame.Rect(2525, 250, 100, 250), #11
                pygame.Rect(2625, 300, 150, 200), #12

                # Jaskyňa s 75px vertikálnym priestorom medzi platformami
                pygame.Rect(2975, 350, 300, 200),  #13
                    pygame.Rect(2975, -125, 1200, 400),
                pygame.Rect(3125, 400, 300, 200),  #13

                pygame.Rect(3425, 500, 100, 200),  #13
                pygame.Rect(3525, 625, 500, 200),  #13
                        pygame.Rect(3675, 500, 100, 50),  #13
                pygame.Rect(4025, -125, 600, 950),


            ],
            winPlatforms= [
                pygame.Rect(3900, 575, 50, 50)
            ],
            deathPlatforms = [
                pygame.Rect(0, 800, 4000, 50)
            ],
            entities = [
                utils.makeGranule(200, 200),
                utils.makeGranule(1175, 350),
                utils.makeGranule(1800, 250),
                utils.makeGranule(2400, 150),
                utils.makeGranule(2900, 300),
                utils.makeGranule(3675, 460),
                # Pohybujúci nepriateľ pozdĺž osi Y
                utils.makeEnemyPatrol(500, 350, axis='y', distance=300, patrol_speed=4),
                utils.makeEnemy(750,275),
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
            platform_image = pygame.image.load('images\platformy\platforma_003.png'),
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
                pygame.Rect(1325, 225, 100, 50),
                pygame.Rect(1475, 175, 100, 50),
                pygame.Rect(1775, 125, 200, 50),
                pygame.Rect(2025, 75, 150, 50),
                pygame.Rect(2225, 200, 250, 50),
                pygame.Rect(2525, 270, 300, 50),
                pygame.Rect(2825, 200, 200, 50),
                pygame.Rect(3025, 150, 200, 50),
                pygame.Rect(3225, 100, 150, 50),
                pygame.Rect(3425, 50, 250, 50),
            ],
            winPlatforms= [
                pygame.Rect(3525, 0, 50, 50)
            ],
            deathPlatforms = [
                pygame.Rect(0, 800, 2000, 50)
            ],
            entities = [
                utils.makeGranule(200, 200),
                utils.makeEnemyPatrol(450, 200, axis='x', distance=200),
                utils.makeEnemyPatrol(750, 50, axis='y', distance=300, patrol_speed=3),
                utils.makeEnemyPatrol(1650, 200, axis='y', distance=350, patrol_speed=4),
                utils.makeEnemyPatrol(1775, 200, axis='x', distance=250, patrol_speed=3),
                utils.makeEnemy(1875, 100),
                utils.makeEnemy(2570, 250),
                utils.makeEnemy(2875, 175),
                utils.makeEnemy(3075, 125),
                utils.makeEnemy(3275, 75),
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
            platform_image = pygame.image.load('images\platformy\platforma_012.png'),
            win_image = pygame.image.load('images\platformy\platforma_031.png'),
            winFunc= wonLevel,
            loseFunc= lostLevel
        )
    



    # Resetovanie všetkých entít v úrovni
    for entity in globals.world.entities:
        entity.reset(entity)
