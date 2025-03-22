import pygame  # Používame Pygame na prácu so zvukmi a hudbou
import configparser  # Na prácu s nastaveniami uloženými v INI súbore

class SoundManager:
    ALLOWED_VOLUMES = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]  
    # Hodnoty hlasitosti, ktoré môžeme použiť

    def __init__(self, initial_sound_volume=0.2, initial_music_volume=0.2):
        pygame.mixer.init()  # Spustíme systém na prehrávanie zvukov a hudby
        # Načítame nastavenia z INI súboru, ak existuje
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')

        # Nastavíme hlasitosti podľa INI alebo použijeme predvolené hodnoty
        if 'Audio' in self.config:
            self.soundVolume = float(self.config['Audio'].get('soundvolume', initial_sound_volume))
            self.musicVolume = float(self.config['Audio'].get('musicvolume', initial_music_volume))
        else:
            self.soundVolume = initial_sound_volume
            self.musicVolume = initial_music_volume

        # Oprava hlasitostí na povolené hodnoty
        self.soundVolume = self._clampVolume(self.soundVolume)
        self.musicVolume = self._clampVolume(self.musicVolume)

        self.targetMusicVolume = self.musicVolume  # Cieľová hlasitosť hudby
        self.nextMusic = None  # Hudba na prehranie po aktuálnej skladbe
        self.currentMusic = None  # Aktuálne prehrávaná hudba

        # Načítame zvuky a priradíme ich ku konkrétnym udalostiam v hre
        self.sounds = {
            'jump': pygame.mixer.Sound('sounds\\jump.wav'),  
            'granule': pygame.mixer.Sound('sounds\\coin.wav'),  
            'hurt': pygame.mixer.Sound('sounds\\hurt.wav'),  
            'win': pygame.mixer.Sound('sounds\\power_up.wav'),  
            'lose': pygame.mixer.Sound('sounds\\hurt.wav')  
        }

        # Načítame hudbu, ktorá sa bude prehrávať v rôznych častiach hry
        self.music = {
            'level': 'music\\Time_for_adventure.mp3',  
            'menu': 'music\\PianoPack-Track01.wav',  
            'lost': 'music\\Piano Pack - Track 05.wav',  
            'won': 'music\\Piano Pack - Track 09.wav'  
        }

        # Nastavíme hlasitosti a spustíme hudbu pre menu
        self.setSoundVolume(self.soundVolume)
        self.setMusicVolume(self.musicVolume)
        if self.musicVolume > 0:
            self.playMusic('menu')

    def _clampVolume(self, volume):
        """Obmedzí hlasitosť na najbližšiu povolenú hodnotu."""
        return min(self.ALLOWED_VOLUMES, key=lambda x: abs(x - volume))

    def playSound(self, soundName):
        """Prehrá konkrétny zvuk na nastavenej hlasitosti."""
        self.sounds[soundName].set_volume(self.soundVolume)
        self.sounds[soundName].play()

    def playMusic(self, musicName):
        """Prehrá hudbu podľa názvu, ak už nehrá tá istá skladba."""
        if musicName is self.currentMusic:
            return
        pygame.mixer.music.load(self.music[musicName])
        pygame.mixer.music.set_volume(self.musicVolume)
        self.currentMusic = musicName
        pygame.mixer.music.play(-1)  # Prehrá hudbu dookola

    def playMusicFade(self, musicName):
        """Prehrá hudbu so zmenou hlasitosti (fade-out)."""
        if musicName is self.currentMusic:
            return
        self.nextMusic = musicName
        self.fadeOut()

    def fadeOut(self):
        """Stíši aktuálnu hudbu postupne (fade-out)."""
        pygame.mixer.music.fadeout(500)

    def update(self):
        """Pravidelne kontroluje hlasitosť a spúšťa ďalšiu hudbu po fade-oute."""
        if abs(self.musicVolume - self.targetMusicVolume) >= 0.001:
            if self.musicVolume < self.targetMusicVolume:
                self.musicVolume = min(self.musicVolume + 0.005, self.targetMusicVolume)
            elif self.musicVolume > self.targetMusicVolume:
                self.musicVolume = max(self.musicVolume - 0.005, self.targetMusicVolume)
            self.setMusicVolume(self.musicVolume)

        if self.nextMusic is not None and not pygame.mixer.music.get_busy():
            self.currentMusic = None
            self.musicVolume = max(self.musicVolume, 0.01)
            self.setMusicVolume(self.musicVolume)
            self.playMusic(self.nextMusic)
            self.nextMusic = None

    def setSoundVolume(self, volume):
        """Nastaví hlasitosť pre všetky zvuky."""
        volume = self._clampVolume(volume)
        if abs(self.soundVolume - volume) < 0.001:
            return
        self.soundVolume = volume
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def setMusicVolume(self, volume):
        """Nastaví hlasitosť pre aktuálne prehrávanú hudbu."""
        volume = self._clampVolume(volume)
        if abs(self.musicVolume - volume) < 0.001:
            return
        self.musicVolume = volume
        pygame.mixer.music.set_volume(volume)

    def saveSettings(self):
        """Uloží aktuálne hlasitosti do INI súboru."""
        if 'Audio' not in self.config:
            self.config.add_section('Audio')
        self.config.set('Audio', 'soundvolume', str(round(self.soundVolume, 2)))
        self.config.set('Audio', 'musicvolume', str(round(self.musicVolume, 2)))
        with open('settings.ini', 'w') as configfile:
            self.config.write(configfile)

    def loadSettings(self, default_sound_volume=0.2, default_music_volume=0.2):
        """Načíta hlasitosti z INI súboru alebo použije predvolené hodnoty."""
        if not self.config.read('settings.ini'):
            self.soundVolume = default_sound_volume
            self.musicVolume = default_music_volume
            return
        if 'Audio' in self.config:
            self.soundVolume = float(self.config['Audio'].get('soundvolume', default_sound_volume))
            self.musicVolume = float(self.config['Audio'].get('musicvolume', default_music_volume))
        else:
            self.soundVolume = default_sound_volume
            self.musicVolume = default_music_volume
        self.soundVolume = self._clampVolume(self.soundVolume)
        self.musicVolume = self._clampVolume(self.musicVolume)
        self.setSoundVolume(self.soundVolume)
        self.setMusicVolume(self.musicVolume)
