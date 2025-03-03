import pygame
import utils
import engine
import globals

class Level:
    def __init__(self, platforms=None, winPlatforms=None, entities=None, winFunc=None, 
                 loseFunc=None, deathPlatforms=None, invisiblePlatforms=None, 
                 platform_image=None, win_image=None, bg_paths=None):
        # Inicializácia úrovne s predvolenými hodnotami, ak nie sú poskytnuté
        self.platforms = platforms if platforms is not None else []  # Platformy
        self.winPlatforms = winPlatforms if winPlatforms is not None else []  # Výherné platformy
        self.entities = entities if entities is not None else []  # Entitiy na úrovni
        self.winFunc = winFunc  # Funkcia pre výhru
        self.loseFunc = loseFunc  # Funkcia pre prehru
        self.deathPlatforms = deathPlatforms if deathPlatforms is not None else []  # Platformy, ktoré spôsobujú smrť
        self.invisiblePlatforms = invisiblePlatforms if invisiblePlatforms is not None else []  # Neviditeľné platformy
        self.platform_image = platform_image
        self.win_image = win_image
        self.bg_paths = bg_paths if bg_paths is not None else []
        self.backgrounds = []
        self.load_backgrounds()

    def load_backgrounds(self):
        """Pre-load and scale all background images for this level."""
        for path, speed in self.bg_paths:
            bg_image = pygame.image.load(path).convert_alpha()
            scaled_bg = pygame.transform.scale(bg_image, globals.SCREEN_SIZE)
            self.backgrounds.append((scaled_bg, speed))

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
    for entity in level.entities:
        if entity.type == 'player' and entity.battle and entity.battle.lives > 0:
            return False
    return True


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
    if globals.world is None:
        globals.world = Level()

    if levelNumber == 1:
        globals.world = Level(
            platforms = [
                pygame.Rect(100, 250, 200, 50),
                pygame.Rect(400, 180, 200, 50),
                pygame.Rect(800, 180, 200, 50),
                pygame.Rect(1200, 180, 200, 50),
                pygame.Rect(1600, 130, 200, 50),
                pygame.Rect(2000, 80, 200, 50),
                pygame.Rect(2350, 30, 250, 50),
                pygame.Rect(2300, 200, 150, 50),
                pygame.Rect(2700, 250, 400, 50),
            ],
            winPlatforms= [
                pygame.Rect(3100, 200, 50, 50)  # Cieľ
            ],
            deathPlatforms = [
                pygame.Rect(0, 1000, 4000, 50)  # Zem smrti
            ],
            entities = [
                utils.makeGranule(200, 180),
                utils.makeGranule(200, 200),
                utils.makeGranule(250, 200),
                utils.makeSuperJump(1255,160),
                utils.makeEnemy(850, 160),
                utils.makeEnemyPatrol(1400, 150, axis='y', distance=400, patrol_speed=4),
                utils.makeEnemyPatrol(2600, 90, axis='x', distance=600, patrol_speed=6),
                utils.makeGranule(2890,25),
                globals.player1
            ],
            invisiblePlatforms = [  
                pygame.Rect(50, -300, 50, 1200),
            ],
            bg_paths = [
                ('images/pozadia/level1_1.png', 0.2),
                ('images/pozadia/level1_3.png', 0.4),
                ('images/pozadia/level1_6.png', 0.6),
                ('images/pozadia/level1_7.png', 0.8),
                ('images/pozadia/level1_8.png', 1),
            ],
            platform_image = pygame.image.load('images/platformy/platforma_000.png'),
            win_image = pygame.image.load('images/platformy/platforma_031.png'),
            winFunc= wonLevel,
            loseFunc= lostLevel
        )
    elif levelNumber == 2:
        globals.world = Level(
            platforms = [
                pygame.Rect(100, 300, 375, 50),  #1
                pygame.Rect(600, 300, 400, 50),  #2
                pygame.Rect(1100, 250, 50, 50),   #3
                pygame.Rect(1175, 400, 50, 50),  #4 
                pygame.Rect(1250, 250, 50, 50),   #5
                pygame.Rect(1380, 400, 100, 50), #6
                pygame.Rect(1575, 350, 200, 50), #7
                pygame.Rect(1850, 300, 100, 50), #8
                pygame.Rect(2130, 250, 100, 50), #9
                pygame.Rect(2375, 200, 150, 50), #10
                pygame.Rect(2525, 250, 100, 50), #11
                pygame.Rect(2625, 300, 150, 50), #12
                pygame.Rect(2975, 350, 300, 50),  #13
                pygame.Rect(2975, -125, 50, 400),
                    pygame.Rect(2975, 225, 1000, 50),
                pygame.Rect(3125, 400, 300, 50),  #13
                    pygame.Rect(3375, 400, 50, 100),  #13
                pygame.Rect(3425, 500, 100, 50),  #13
                    pygame.Rect(3475, 550, 50, 100),  #13
                pygame.Rect(3525, 625, 500, 50),  #13
                pygame.Rect(3875, 500, 100, 50),  #13
                    pygame.Rect(3975, 225, 50, 400),  #13
                pygame.Rect(4025, -125, 600, 50),
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
                utils.makeEnemyPatrol(500, 350, axis='y', distance=300, patrol_speed=4),
                utils.makeEnemy(750,275),
                globals.player1
            ],
            invisiblePlatforms = [  # Neviditeľná stena pozdĺž osi Y
                pygame.Rect(50, -300, 50, 600)
            ],
            bg_paths = [
                ('images/pozadia/level2_1.png', 0.2),
                ('images/pozadia/level2_2.png', 0.5),
                ('images/pozadia/level2_3.png', 0.7),
                ('images/pozadia/level2_4.png', 1),
            ],
            platform_image = pygame.image.load('images/platformy/platforma_003.png'),
            win_image = pygame.image.load('images/platformy/platforma_031.png'),
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
                pygame.Rect(1525, 175, 100, 50),
                pygame.Rect(1775, 125, 200, 50),
                pygame.Rect(2025+100, 75, 150, 50),
                pygame.Rect(2225+200, 200, 250, 50),
                pygame.Rect(2525+300, 270, 300, 50),
                pygame.Rect(2825+300, 200, 200, 50),
                pygame.Rect(3025+300, 150, 200, 50),
                pygame.Rect(3225+300, 100, 150, 50),
                pygame.Rect(3425+300, 50, 250, 50),
            ],
            winPlatforms= [
                pygame.Rect(3525+300, 0, 50, 50)
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
                utils.makeEnemy(2570+300, 250),
                utils.makeEnemy(2875+300, 175),
                utils.makeEnemy(3075+300, 125),
                utils.makeEnemy(3275+300, 75),
                globals.player1
            ],
            invisiblePlatforms = [
                pygame.Rect(50, -300, 50, 600)
            ],
            bg_paths = [
                ('images/pozadia/level3_1.png', 0.2),
                ('images/pozadia/level3_2.png', 0.3),
                ('images/pozadia/level3_3.png', 0.5),
                ('images/pozadia/level3_4.png', 0.6),
                ('images/pozadia/level3_5.png', 0.8),
                ('images/pozadia/level3_6.png', 1),
            ],
            platform_image = pygame.image.load('images/platformy/platforma_012.png'),
            win_image = pygame.image.load('images/platformy/platforma_031.png'),
            winFunc= wonLevel,
            loseFunc= lostLevel
        )
    elif levelNumber == 4:
        globals.world = Level(
            platforms=[
                pygame.Rect(100, 300, 1000, 50),  # Štartovacia platforma 
                pygame.Rect(450, 175, 200, 50),  # 2
                pygame.Rect(800, 125, 400, 50),  # 3
                pygame.Rect(960, 30-30, 250, 50),  # 3.5
                pygame.Rect(600+50, 30-30, 200, 50),  # 4
                pygame.Rect(200, 30-30, 200, 50),  # 5
                pygame.Rect(250, -115, 100, 50),  # 5.5
                pygame.Rect(200+150, -165, 500, 50),  # 6
                pygame.Rect(970, -165, 100, 50),  # 7
                pygame.Rect(1000+170, -165, 200, 50),  # 8
                pygame.Rect(1315, -280, 50, 50),  # 9
                pygame.Rect(1170, -330, 150, 50),  # 9
                pygame.Rect(620+150, -190-110, 200, 50),  # koniec 
            ],
            winPlatforms=[
                pygame.Rect(620+150, -350, 50, 50),  # Cieľová platforma 
            ],
            entities=[
                utils.makeSuperJump(495,280 ), #1
                utils.makeSuperJump(1075,100 ), #2
                utils.makeSuperJump(335,-40),
                utils.makeSuperJump(1320,-180),
                utils.makeEnemy(520,175-25),
                utils.makeEnemyPatrol(985, 50, axis='x', distance=250, patrol_speed=3),
                utils.makeEnemyPatrol(1060, -50, axis='x', distance=250, patrol_speed=5),
                utils.makeEnemyPatrol(860, -100, axis='y', distance=150, patrol_speed=2),
                utils.makeEnemyPatrol(1070, -200, axis='y', distance=250, patrol_speed=5),
                utils.makeGranule(445,155),
                utils.makeGranule(600,155),
                utils.makeGranule(1060,-50),
                utils.makeGranule(1050,-50),
                globals.player1,  # Hráč
            ],
            deathPlatforms=[
                pygame.Rect(100, 350, 2000, 50)
            ],
            invisiblePlatforms=[
                pygame.Rect(50, -300, 50, 800),  # Neviditeľná stena
            ],
            bg_paths = [
                ('images/pozadia/level4_1.png', 0.2),
                ('images/pozadia/level4_2.png', 0.3),
                ('images/pozadia/level4_3.png', 0.5),
                ('images/pozadia/level4_4.png', 0.6),
                ('images/pozadia/level4_5.png', 0.8),
                ('images/pozadia/level4_6.png', 1),
            ],
            platform_image=pygame.image.load('images/platformy/platforma_012.png'),
            win_image=pygame.image.load('images/platformy/platforma_031.png'),
            winFunc=wonLevel,
            loseFunc=lostLevel,
        )

    elif levelNumber == 5:
        globals.world = Level(
        platforms = [
                pygame.Rect(100, 300, 250, 50),  # Štartovacia platforma 
                pygame.Rect(450, 300, 250, 50), #2
                pygame.Rect(800, 300, 100, 50), #3
                    pygame.Rect(1080, 300-80, 100, 50),  # 4
                        pygame.Rect(1080+50, 300-180, 50, 50),  # 4
                        pygame.Rect(1080+100, 300-205, 50, 25),  # 4
                        pygame.Rect(800, 300-160, 100, 50),  # 5
                            pygame.Rect(600, 300-210, 100, 50),
                            pygame.Rect(400, 300-210, 100, 50),
                                    pygame.Rect(350, 300-290, 50, 100),
                                        pygame.Rect(500, 300-360, 100, 50),
                                        pygame.Rect(800, 300-360, 50, 50),
                                        pygame.Rect(850+160, 300-360, 50, 50),

            ],
            winPlatforms= [
                pygame.Rect(975+240, 300-360, 50, 50)
            ],
            deathPlatforms = [
                pygame.Rect(0, 500, 3000, 50)
            ],
            entities = [
                utils.makeSuperJump(790,280),
                utils.makeSuperJump(1160,210),
                utils.makeSuperJump(470,50),

                utils.makeEnemyPatrol(365,400,'y',300,6),

                utils.makeEnemyPatrol(520,150,'y',200,4),

                utils.makeEnemyPatrol(710,300,'y',600,11),
                utils.makeEnemyPatrol(910,300,'y',600,9),
            
                globals.player1
            ],
            invisiblePlatforms = [  # Neviditeľná stena pozdĺž osi Y
                pygame.Rect(50, -300, 50, 600)
            ],
            bg_paths= [
                (r'images/pozadia/level5_1.png', 0.2),
                (r'images/pozadia/level5_2.png', 0.4),
                (r'images/pozadia/level5_3.png', 0.6),
                (r'images/pozadia/level5_4.png', 0.8),
                (r'images/pozadia/level5_5.png', 1),
            ],
            platform_image = pygame.image.load('images\platformy\platforma_000.png'),
            win_image = pygame.image.load('images\platformy\platforma_031.png'),
            winFunc= wonLevel,
            loseFunc= lostLevel
        )



    # Resetovanie všetkých entít v úrovni
    for entity in globals.world.entities:
        entity.reset(entity)
