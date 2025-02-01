import pygame
import engine
import globals

# Inicializácia písma pre text
pygame.font.init()
font = pygame.font.Font(pygame.font.get_default_font(), 24)
PixelOperator8 = pygame.font.Font('font\PixelOperator8.ttf', 24)
PixelOperator8_Bold = pygame.font.Font('font\PixelOperator8_Bold.ttf', 24)

# Funkcia na vykreslenie obrázka s priehľadnosťou
# Inšpirované zdrojom: https://nerdparadise.com/programming/pygameblitopacity
def blit_alpha(target, source, location, opacity):
    x = location[0]
    y = location[1]
    temp = pygame.Surface((source.get_width(), source.get_height())).convert()
    temp.blit(target, (-x, -y))  # Skopíruje cieľ na dočasnú plochu
    temp.blit(source, (0, 0))  # Skopíruje zdroj na dočasnú plochu
    temp.set_alpha(opacity)  # Nastaví priehľadnosť
    target.blit(temp, location)  # Vykreslí do cieľovej plochy





# Funkcia na vykreslenie textu
def drawText(screen, t, x, y, fg, alpha,Usedfont = font):
    # Vytvorenie textu pomocou vlastného fontu, s vybranou farbou (fg)
    text = Usedfont.render(t, True, fg)
    

    # Získanie obdlžníka textu (na určenie pozície a rozmerov)
    text_rect = text.get_rect()
    
    # Nastavenie ľavého horného rohu textu na pozíciu (x, y)
    text_rect.topleft = (x, y)
    
    # Vykreslenie textu s nastavenou priehľadnosťou (alpha) na obrazovku (screen)
    blit_alpha(screen, text, (x, y), alpha)

# Načítanie obrázkov pre rôzne objekty v hre
zivot_image = pygame.image.load('images\dachshund_zivot.png')

granule0 = pygame.image.load('images\granule_0.png')
granule1 = pygame.image.load('images\granule_1.png')
granule2 = pygame.image.load('images\granule_2.png')

# Funkcia na vytvorenie granule (objektu, ktorý hráč zbiera)
def makeGranule(x, y):
    entity = engine.Entity()  # Vytvorí novú entitu
    entity.position = engine.Position(x, y, 23, 23)  # Nastaví pozíciu a veľkosť
    entityAnimation = engine.Animation([granule0, granule1, granule2])  # Animácia granule
    entity.animations.add('idle', entityAnimation)  # Pridanie animácie do entity
    entity.type = 'collectable'  # Typ entity je zbierateľný objekt
    return entity



super0 = pygame.image.load('images\platformy\platforma_071.png')
super1 = pygame.image.load('images\platformy\platforma_072.png')
super0 = pygame.transform.scale(super0, (45, 45))
super1 = pygame.transform.scale(super1, (45, 45))

def makeSuperJump(x, y):
    entity = engine.Entity()  # Vytvorí novú entitu
    entity.position = engine.Position(x, y, 45, 45)  # Nastaví pozíciu a veľkosť
    entityAnimation = engine.Animation([super0, super1])  # Animácia granule
    entity.animations.add('idle', entityAnimation)  # Pridanie animácie do entity
    entity.type = 'superjump'  # Typ entity je super jump
    return entity

# Načítanie obrázku nepriateľa
enemy0 = pygame.image.load('images\spike_monster.png')

# Funkcia na vytvorenie nepriateľa
def makeEnemy(x, y):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 50, 26)  # Nastaví pozíciu a veľkosť
    entityAnimation = engine.Animation(enemy0)  # Animácia pre nepriateľa
    entity.animations.add('idle', entityAnimation)  # Pridanie animácie do entity
    entity.type = 'danger'  # Typ entity je nebezpečný (nepriateľ)
    return entity

# Načítanie obrázkov pre animáciu vrána
crow0 = pygame.image.load('images\crow_0.png')
crow1 = pygame.image.load('images\crow_1.png')
crow2 = pygame.image.load('images\crow_2.png')
crow3 = pygame.image.load('images\crow_3.png')
crow4 = pygame.image.load('images\crow_4.png')

# Funkcia na vytvorenie nepriateľa s patrolovaním
def makeEnemyPatrol(x, y, axis='y', distance=100,patrol_speed = 2):
    entity = engine.Entity()
    entity.position = engine.Position(x, y, 72, 96)  # Nastaví pozíciu a veľkosť
    
    # Animácia pre nepriateľa
    entityAnimation = engine.Animation([crow0, crow1, crow2, crow3, crow4])
    entity.animations.add('idle', entityAnimation)  # Pridanie animácie do entity
    entity.type = 'danger'  # Typ entity je nebezpečný
    
    # Parametre pre patrolovanie (pohyb sem a tam)
    entity.patrol_direction = 1  # 1 pre pohyb vpred, -1 pre pohyb späť
    entity.patrol_distance = distance  # Vzdialenosť, ktorú prejde
    entity.start_position = y if axis == 'y' else x  # Počiatočná pozícia
    entity.patrol_axis = axis  # Osa (y alebo x), po ktorej sa pohybuje
    entity.patrol_speed = patrol_speed  # Rýchlosť pohybu
    
    # Funkcia na aktualizáciu pohybu patrolovania
    def updatePatrol(entity):
        if entity.patrol_axis == 'y':
            if entity.patrol_direction == 1:
                entity.position.rect.y -= entity.patrol_speed  # Pohyb nahor
                if entity.position.rect.y <= entity.start_position - entity.patrol_distance:
                    entity.patrol_direction = -1  # Zmena smeru
            else:
                entity.position.rect.y += entity.patrol_speed  # Pohyb nadol
                if entity.position.rect.y >= entity.start_position:
                    entity.patrol_direction = 1  # Zmena smeru
        elif entity.patrol_axis == 'x':
            if entity.patrol_direction == 1:
                entity.position.rect.x += entity.patrol_speed  # Pohyb doprava
                if entity.position.rect.x >= entity.start_position + entity.patrol_distance:
                    entity.patrol_direction = -1  # Zmena smeru
                    entity.direction = 'right'
            else:
                entity.position.rect.x -= entity.patrol_speed  # Pohyb doľava
                if entity.position.rect.x <= entity.start_position:
                    entity.patrol_direction = 1  # Zmena smeru
                    entity.direction = 'left'

    # Priradí funkciu aktualizácie patrolovania k entite
    entity.updatePatrol = updatePatrol

    return entity

# Načítanie obrázkov pre animácie hráča
idle0 = pygame.image.load('images\dachshund_0.png')
idle1 = pygame.image.load('images\dachshund_1.png')

walk1 = pygame.image.load('images\dachshund_2.png')
walk2 = pygame.image.load('images\dachshund_3.png')

fall1 = pygame.image.load('images\dachshund_3.png')

# Funkcia na resetovanie hráča (obnoví pozíciu)
def resetPlayer(entity):
    entity.position.rect.x = 100  # Resetuje pozíciu
    entity.position.rect.y = 0
    entity.speed = 0  # Vynuluje rýchlosť
    entity.acceleration = 0.2  # Nastaví akceleráciu
    entity.camera.setWorldPos(300, 0)  # Nastaví pozíciu kamery
    entity.direction = 'right'  # Počiatočný smer je vpravo

# Funkcia na vytvorenie hráča na pozícii (x, y)
def makePlayer(x, y):
    entity = engine.Entity()  # Vytvorí entitu pre hráča
    # Nastaví pozíciu a veľkosť hráča
    entity.position = engine.Position(x, y, 72, 50)
    
    # Animácie pre rôzne stavy (idle, walking, falling)
    entityIdleAnimation = engine.Animation([idle0, idle1]) 
    entityWalkingAnimation = engine.Animation([walk1, walk2])
    entityFallingAnimation = engine.Animation([walk2, fall1])
    
    # Pridanie animácií
    entity.animations.add('FLY', entityFallingAnimation)
    entity.animations.add('idle', entityIdleAnimation)
    entity.animations.add('walking', entityWalkingAnimation)

    # Nastavenie ďalších vlastností hráča
    entity.score = engine.Score()  # Skóre
    entity.battle = engine.Battle()  # Životy a boj
    entity.intention = engine.Intention()  # Úmysly (správanie)
    entity.acceleration = 0.2  # Akcelerácia
    entity.type = 'player'  # Typ entity je hráč
    entity.reset = resetPlayer  # Funkcia na resetovanie hráča
    return entity
