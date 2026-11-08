import pygame
from pathlib import Path


class AudioManager:

    def __init__(self):

        self.audio_folder = (
            Path(__file__).resolve().parents[2]
            / "assets"
            / "audio"
        )

        self.music_enabled = True
        self.sound_enabled = True

        self.music_volume = 0.35
        self.sound_volume = 0.60

        self.sounds = {}

        self.initialise_audio()

    def initialise_audio(self):

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()

            sound_files = {
                "hover": "hover.wav",
                "click": "click.wav",
                "start": "start.wav",
                "submit": "submit.wav",
                "result": "result.wav"
            }

            for name, filename in sound_files.items():

                path = self.audio_folder / filename

                if path.exists():
                    self.sounds[name] = pygame.mixer.Sound(
                        str(path)
                    )
                    self.sounds[name].set_volume(
                        self.sound_volume
                    )

            self.music_path = self.audio_folder / "background.mp3"

            print("Audio system initialised successfully!")

        except pygame.error as error:
            print(f"Audio initialisation failed: {error}")

    def play_sound(self, name):

        if not self.sound_enabled:
            return

        sound = self.sounds.get(name)

        if sound:
            sound.set_volume(self.sound_volume)
            sound.play()

    def play_music(self):

        if not self.music_enabled:
            return

        try:
            if self.music_path.exists():
                pygame.mixer.music.load(str(self.music_path))
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(-1)

        except pygame.error as error:
            print(f"Music playback failed: {error}")

    def stop_music(self):

        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    def toggle_music(self):

        self.music_enabled = not self.music_enabled

        if self.music_enabled:
            self.play_music()
        else:
            self.stop_music()

    def toggle_sound(self):

        self.sound_enabled = not self.sound_enabled

    def set_music_volume(self, volume):

        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sound_volume(self, volume):

        self.sound_volume = max(0.0, min(1.0, volume))

        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)