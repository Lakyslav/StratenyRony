import pygame
import utils
import level
import scene
import globals
import ui

# Trieda systému (základná trieda pre rôzne systémy)
class System():
    def __init__(self):
        pass
    
    # Metóda na kontrolu entity
    def check(self, entity):
        return True
    
    # Metóda na aktualizáciu všetkých entít v úrovni
    def update(self, screen=None, inputStream=None):
        for entity in globals.world.entities:
            if self.check(entity):
                self.updateEntity(screen,inputStream, entity)
    
    # Metóda na aktualizáciu konkrétnej entity
    def updateEntity(self, screen, inputStream, entity):
        pass

class AnimationSystem(System):
    def check(self, entity):
        return entity.animations is not None
    
    # Aktualizácia animácií entity
    def updateEntity(self, screen, inputStream, entity):    
        entity.animations.animationList[entity.state].update()

class PhysicsSystem(System):
    def check(self, entity):
        return entity.position is not None

    def update(self):
        # Prechádzanie všetkými entitami a volanie metódy updatePatrol, ak existuje
        for entity in globals.world.entities:
            if hasattr(entity, 'updatePatrol'):
                entity.updatePatrol(entity)  # Posielame entitu ako argument pre updatePatrol

        # Teraz aktualizujeme všetky entity s ich individuálnou fyzikou
        for entity in globals.world.entities:
            if self.check(entity):  # Skontrolujeme, či je entita platná na aktualizáciu
                self.updateEntity(None, None, entity)  # Aktualizujeme entitu s fyzikou a pohybom

    def updateEntity(self, screen, inputStream, entity):
        new_x = entity.position.rect.x
        new_y = entity.position.rect.y

        if entity.intention is not None:
            if entity.intention.moveLeft:
                new_x -= 5
                entity.direction = 'left'
                entity.state = 'walking'
            if entity.intention.moveRight:
                new_x += 5
                entity.direction = 'right'
                entity.state = 'walking'
            if not entity.intention.moveLeft and not entity.intention.moveRight:
                entity.state = 'idle'
            if entity.intention.jump and entity.on_ground:

                globals.soundManager.playSound('jump')
                if entity.super_jump == True:
                    entity.speed = -7.5
                    entity.super_jump = False

                else:
                    entity.speed = -5

        # horizontálny pohyb
        new_x_rect = pygame.Rect(
            int(new_x),
            int(entity.position.rect.y),
            entity.position.rect.width,
            entity.position.rect.height)

        x_collision = False

        #...kontrola kolízií s každou platformou
        for platform in globals.world.platforms + globals.world.invisiblePlatforms:
            if platform.colliderect(new_x_rect):
                x_collision = True
                break

        if x_collision == False:
            entity.position.rect.x = new_x

        # vertikálny pohyb
        entity.speed += entity.acceleration
        new_y += entity.speed

        new_y_rect = pygame.Rect(
            int(entity.position.rect.x),
            int(new_y),
            entity.position.rect.width,
            entity.position.rect.height)

        y_collision = False
        entity.on_ground = False

        #...kontrola kolízií s každou platformou
        for platform in globals.world.platforms + globals.world.invisiblePlatforms:
            if platform.colliderect(new_y_rect):
                y_collision = True
                entity.speed = 0
                # ak je platforma pod hráčom
                if platform[1] > new_y:
                    # prilepíme hráča na platformu
                    entity.position.rect.y = platform[1] - entity.position.rect.height
                    entity.on_ground = True
                break

        if y_collision == False:
            entity.position.rect.y = int(new_y)

        # resetovanie úmyslov
        if entity.intention is not None:
            entity.intention.moveLeft = False
            entity.intention.moveRight = False
            entity.intention.jump = False

class InputSystem(System):
    def check(self, entity):
        return entity.input is not None and entity.intention is not None
    
    # Aktualizácia vstupu pre konkrétnu entitu
    def updateEntity(self, screen, inputStream, entity):
        # hore = skok
        if inputStream.keyboard.isKeyDown(entity.input.up):
            entity.intention.jump = True
        else:
            entity.intention.jump = False
        # vľavo = pohyb vľavo
        if inputStream.keyboard.isKeyDown(entity.input.left):
            entity.intention.moveLeft = True
        else:
            entity.intention.moveLeft = False
        # vpravo = pohyb vpravo    
        if inputStream.keyboard.isKeyDown(entity.input.right):
            entity.intention.moveRight = True
        else:
            entity.intention.moveRight = False
        # b1 = zoom out
        if inputStream.keyboard.isKeyDown(entity.input.b1):
            entity.intention.zoomOut = True
        else:
            entity.intention.zoomOut = False        
        # b2 = zoom in
        if inputStream.keyboard.isKeyDown(entity.input.b2):
            entity.intention.zoomIn = True
        else:
            entity.intention.zoomIn = False 
        if inputStream.keyboard.isKeyPressed(pygame.K_c):
            print(f"Entity Coordinates: X={entity.position.rect.x}, Y={entity.position.rect.y+50}")

class CollectionSystem(System):
    def check(self, entity):     # Kontrola, či entita je hráč a má atribút score
        return entity.type == 'player' and entity.score is not None
    
    # Aktualizácia zbierania predmetov
    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            # Kontrola, či iná entita nie je hráč a či je zbierateľná
            if otherEntity is not entity and otherEntity.type == 'collectable':
                #Pokiaľ má kolíziu s iným telesom
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    globals.soundManager.playSound('granule') #Prehraj zvuk
                    globals.world.entities.remove(otherEntity) #Vymaž z mapy
                    entity.score.score += 1 # Zvých počet granúľ

                    # Kontrola či máme 3 granule
                    if entity.score.score % 3 == 0:
                        # Priadaj život
                        entity.battle.lives += 1
                        entity.score.score = 0


class SuperJumpSystem(System):
    def check(self, entity):
        return entity.type == 'player'
    
    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'superjump':
                if entity.position.rect.colliderect(otherEntity.position.rect) and entity.super_jump == False:
                    globals.soundManager.playSound('granule') #Prehraj zvuk
                    entity.super_jump = True  # Aktivácia super skoku
  

class BattleSystem(System):
    def check(self, entity):
        return entity.type == 'player' and entity.battle is not None
    
    # Aktualizácia boja a kolízií s nebezpečnými entitami
    def updateEntity(self, screen, inputStream, entity):
        for otherEntity in globals.world.entities:
            if otherEntity is not entity and otherEntity.type == 'danger':
                if entity.position.rect.colliderect(otherEntity.position.rect):
                    globals.soundManager.playSound('hurt')
                    entity.battle.lives -= 1
                    # reset pozície hráča
                    entity.position.rect.x = 100
                    entity.position.rect.y = 0
                    entity.speed = 0 
                    entity.acceleration = 0.2
        for deathPlatform in globals.world.deathPlatforms:
            if entity.position.rect.colliderect(deathPlatform):
                globals.soundManager.playSound('hurt')  # Zahráme zvuk poškodenia
                entity.battle.lives -= 1  # Znížime životy
                # reset pozície hráča
                entity.position.rect.x = 100
                entity.position.rect.y = 0
                entity.speed = 0
                entity.acceleration = 0.2

# Systém pre kameru
class CameraSystem(System):

    # Overenie, či entity majú kameru
    def check(self, entity):
        return entity.camera is not None
    
    # Aktualizácia entity, ktorá má kameru
    def updateEntity(self, screen, inputStream, entity):

        # Nastavenie orezávacieho obdlžníka (klipovacieho)
        cameraRect = entity.camera.rect
        clipRect = pygame.Rect(cameraRect.x, cameraRect.y, cameraRect.width, cameraRect.height)
        screen.set_clip(clipRect)

        offsetX = cameraRect.x + cameraRect.w / 2 - (entity.camera.worldX * entity.camera.zoomLevel)
        offsetY = cameraRect.y + cameraRect.h / 2 - (entity.camera.worldY * entity.camera.zoomLevel)

        # Parallax pozadia
        if globals.world.backgrounds:
            screen.fill(globals.BLACK)

            for bg_image, speed in globals.world.backgrounds:
                bg_width, _ = bg_image.get_size()

                # Get parallax scrolling offset
                camera_x = int(entity.camera.worldX * speed)
                offset = camera_x % bg_width

                # Calculate two valid positions for the background
                first_x = -offset
                second_x = first_x + bg_width

                # Draw exactly two images only
                screen.blit(bg_image, (first_x, 0))
                screen.blit(bg_image, (second_x, 0))



        # Aktualizácia pozície kamery, ak sleduje nejakú entitu
        if entity.camera.entityToTrack is not None:
            trackedEntity = entity.camera.entityToTrack

            currentX = entity.camera.worldX
            currentY = entity.camera.worldY
            
            # Výpočet cieľovej pozície pre kameru (sledovaná entita)
            targetX = trackedEntity.position.rect.x + trackedEntity.position.rect.w / 2
            targetY = (
                trackedEntity.position.rect.y + trackedEntity.position.rect.h / 2
                - globals.SCREEN_SIZE[1] / 5  # Shift up by a quarter of the screen height
            )

            # Interpolácia pre hladkú zmenu pozície kamery
            entity.camera.worldX = (currentX * 0.95) + (targetX * 0.05)
            entity.camera.worldY = (currentY * 0.95) + (targetY * 0.05)
        
        # Filter entities to only render those within 1000 pixels of the player
        visible_entities = [e for e in globals.world.entities if abs(e.position.rect.x - globals.player1.position.rect.x) < 1000]
        # Filter platforms to only render those within 1000 pixels of the player
        visible_platforms = [p for p in globals.world.platforms if abs(p.x - globals.player1.position.rect.x) < 1000]
        
        visible_win_platforms = [p for p in globals.world.winPlatforms if abs(p.x - globals.player1.position.rect.x) < 1000]
        
        # Print the number of visible entities
        #print(f"Number of visible entities: {len(visible_entities)}")
        #print(f"Number of visible platforms: {len(visible_platforms)}")
        #print(f"Number of visible win platforms: {len(visible_win_platforms)}")


        # Načítanie obrázkov platformy a víťaznej platformy
        platform_image = globals.world.platform_image
        win_image = globals.world.win_image
        platform_scaled = pygame.transform.scale(platform_image, (50, 50))  # Zmena veľkosti platformy na 50x50
        win_scaled = pygame.transform.scale(win_image, (50, 50))  # Zmena veľkosti víťaznej platformy na 50x50

        # Vykreslenie platforiem (na mieste horčicovej farby)
        # Vykreslenie platforiem (na mieste horčicovej farby)
        for p in visible_platforms + visible_win_platforms:  # Only render visible platforms
            newPosRect = pygame.Rect(
                (p.x * entity.camera.zoomLevel) + offsetX,
                (p.y * entity.camera.zoomLevel) + offsetY,
                p.w * entity.camera.zoomLevel,
                p.h * entity.camera.zoomLevel
            )

            if p in visible_platforms:
                # Vykreslenie platformy s obrázkom (opakujeme podľa šírky a výšky platformy)
                for i in range(newPosRect.width // 50):  # opakovanie podľa šírky platformy
                    for j in range(newPosRect.height // 50):  # opakovanie podľa výšky platformy
                        screen.blit(platform_scaled, (newPosRect.x + i * 50, newPosRect.y + j * 50))

            if p in visible_win_platforms:
                # Vykreslenie víťaznej platformy s obrázkom
                for i in range(newPosRect.width // 50):
                    for j in range(newPosRect.height // 50):
                        screen.blit(win_scaled, (newPosRect.x + i * 50, newPosRect.y + j * 50))

        # Vykreslenie entít
        for e in visible_entities:  # Use the filtered list of entities
            s = e.state
            a = e.animations.animationList[s]
            a.draw(screen,
                (e.position.rect.x * entity.camera.zoomLevel) + offsetX,
                (e.position.rect.y * entity.camera.zoomLevel) + offsetY,
                e.direction == 'left', False, entity.camera.zoomLevel, 255)


        self.granule_button = ui.ButtonUI(pygame.K_AMPERSAND, '', 0, 0, normal_img=r"images\UI\Money Panel EMPTY HUD.png",width=92,height=50,)
        self.zivot_button = ui.ButtonUI(pygame.K_AMPERSAND, '', 0, 50, normal_img=r"images\UI\Money Panel EMPTY HUD.png",width=92,height=50,)
        self.super_button = ui.ButtonUI(pygame.K_AMPERSAND, '',  globals.SCREEN_SIZE[0]-210, 50, normal_img=r"images\UI\Button BG.png",width=210)
        self.granule_button.draw(screen)
        self.zivot_button.draw(screen)



        # Vykreslenie HUD pre entitu (skóre a životy)
        if entity.score is not None:
            screen.blit(utils.granule0, (entity.camera.rect.x + 10, entity.camera.rect.y + 20))
            utils.drawText(screen, str(entity.score.score), entity.camera.rect.x + 50, entity.camera.rect.y + 20, globals.WHITE, 255, utils.PixelOperator8)

        # Vykreslenie životov pre entitu
        if entity.battle is not None:
            screen.blit(utils.zivot_image, (entity.camera.rect.x + 10, entity.camera.rect.y + 65))
            utils.drawText(screen, str(entity.battle.lives), entity.camera.rect.x + 50, entity.camera.rect.y + 70, globals.WHITE, 255, utils.PixelOperator8)

        if entity.super_jump is not None:
            if entity.super_jump == True:
                self.super_button.draw(screen)
                utils.drawText(screen, "SUPER SKOK", entity.camera.rect.x + globals.SCREEN_SIZE[0]-205, entity.camera.rect.y + 60, globals.MUSTARD, 255, utils.PixelOperator8)


        # Zrušenie klipovacieho obdlžníka po vykreslení
        screen.set_clip(None)

# Trieda reprezentujúca kameru
class Camera():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)  # Pozícia a veľkosť kamery
        self.worldX = 0  # Počiatočná pozícia kamery na X
        self.worldY = 0  # Počiatočná pozícia kamery na Y
        self.entityToTrack = None  # Entita, ktorú kamera sleduje
        self.zoomLevel = 1  # Úroveň priblíženia (zoom)

    # Nastavenie svetovej pozície kamery
    def setWorldPos(self, x, y):
        self.worldX = x
        self.worldY = y

    # Sledovanie entity kamerou
    def trackEntity(self, e):
        self.entityToTrack = e

# Trieda reprezentujúca pozíciu entity
class Position():
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)  # Pozícia a veľkosť entity

# Trieda pre animácie entity
class Animations():
    def __init__(self):
        self.animationList = {}  # Zoznam animácií pre rôzne stavy
    # Pridanie animácie pre daný stav
    def add(self, state, animation):
        self.animationList[state] = animation

# Trieda pre jednotlivé animácie
class Animation():
    def __init__(self, imageList):
        # Ak je zadaný jeden obrázok (pygame.Surface), obalí ho do zoznamu
        if isinstance(imageList, pygame.Surface):
            self.imageList = [imageList]
        else:
            self.imageList = imageList  # Inak použije zoznam obrázkov
        self.imageIndex = 0  # Index aktuálneho obrázka
        self.animationTimer = 0  # Časovač na zmenu obrázka
        self.animationSpeed = 12  # Rýchlosť prechodu medzi obrázkami

    # Aktualizácia animácie (prejde na ďalší obrázok, ak je čas)
    def update(self):
        self.animationTimer += 1
        if self.animationTimer >= self.animationSpeed:  # Ak uplynul čas
            self.animationTimer = 0  # Resetuje časovač
            self.imageIndex += 1  # Prejde na ďalší obrázok
            if self.imageIndex > len(self.imageList) - 1:  # Ak sme na konci animácie, vráti sa na začiatok
                self.imageIndex = 0

    # Vykreslenie animácie na obrazovku
    def draw(self, screen, x, y, flipX, flipY, zoomLevel, alpha):
        image = self.imageList[self.imageIndex]  # Vyberie aktuálny obrázok animácie
        # Vypočíta nové rozmery obrázka podľa úrovne zväčšenia
        newWidth = int(image.get_rect().w * zoomLevel)
        newHeight = int(image.get_rect().h * zoomLevel)
        # Vykreslí obrázok s možným otočením a zväčšením
        screen.blit(pygame.transform.scale(pygame.transform.flip(image, flipX, flipY), (newWidth, newHeight)), (x, y))


# Trieda pre skóre entity
class Score():
    def __init__(self):
        self.score = 0  # Počiatočné skóre

# Trieda pre životy entity
class Battle():
    def __init__(self):
        self.lives = 3  # Počiatočný počet životov

# Trieda pre vstupy z klávesnice
class Input:
    def __init__(self, up, down, left, right, b1, b2):
        self.up = up  # Klávesa pre skok
        self.down = down  # Klávesa pre pohyb nadol
        self.left = left  # Klávesa pre pohyb doľava
        self.right = right  # Klávesa pre pohyb doprava
        self.b1 = b1  # Prvý ďalší vstup (napríklad zoom out)
        self.b2 = b2  # Druhý ďalší vstup (napríklad zoom in)

# Trieda pre zámery entity (čo má entita robiť)
class Intention:
    def __init__(self):
        self.moveLeft = False  # Pohyb doľava
        self.moveRight = False  # Pohyb doprava
        self.jump = False  # Skok
        self.zoomIn = False  # Priblíženie
        self.zoomOut = False  # Oddialenie

# Funkcia na resetovanie entity
def resetEntity(entity):
    pass  # Resetuje stav entity (momentálne prázdne)

# Hlavná trieda pre entitu (postavu, objekt)
class Entity():
    def __init__(self):
        self.state = 'idle'  # Počiatočný stav entity
        self.type = 'normal'  # Typ entity
        self.position = None  # Pozícia entity
        self.animations = Animations()  # Animácie entity
        self.direction = 'right'  # Počiatočný smer pohybu
        self.camera = None  # Kamera zameraná na entitou
        self.score = None  # Skóre entity (hráča)
        self.battle = None  # Informácie o boji entity (životy)
        self.speed = 0  # Počiatočná rýchlosť gravitácie
        self.acceleration = 0  # Gravitačné zrýchlenie
        self.input = None  # Vstupy z klávesnice
        self.intention = Intention()  # Zámery entity
        self.on_ground = False  # Zistíme, či je entita na zemi
        self.reset = resetEntity  # Funkcia na resetovanie entity
        self.super_jump = False  # Premenná pre Super Jump