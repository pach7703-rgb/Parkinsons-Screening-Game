import pygame
import sys

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GAME_DIR = Path(__file__).resolve().parent

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(GAME_DIR))

from game.settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

from game.utilities.assets import load_all_assets
from game.utilities.audio import AudioManager
from game.utilities.buttons import Button

from game.scenes.menu import MenuScene
from game.scenes.selection import SelectionScene
from game.scenes.instructions import InstructionsScene
from game.scenes.loading import LoadingScene
from game.scenes.drawing import DrawingScene
from game.scenes.results import ResultsScene


class ParkinsonsGame:

    def __init__(self):

        pygame.init()

        pygame.display.set_caption("Parkinson's Screening Game")

        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )

        self.clock = pygame.time.Clock()

        self.assets = load_all_assets()

        self.audio = AudioManager()
        Button.set_audio_manager(self.audio)

        self.audio.play_music()

        self.current_scene = "menu"
        self.test_type = None
        self.running = True

        self.prediction = None
        self.confidence = None

        self.menu_scene = MenuScene(
            self.screen,
            self.assets
        )

        self.scene = self.menu_scene

    def change_scene(self, scene_name):

        self.current_scene = scene_name

        if scene_name == "instructions":
            self.audio.play_sound("start")

        elif scene_name == "drawing":
            self.audio.play_sound("start")

        elif scene_name == "results":
            self.audio.play_sound("result")

        if scene_name == "menu":

            self.scene = MenuScene(
                self.screen,
                self.assets
            )

        elif scene_name == "selection":

            self.scene = SelectionScene(
                self.screen,
                self.assets
            )

        elif scene_name == "instructions":

            self.scene = InstructionsScene(
                self.screen,
                self.assets,
                self.test_type
            )

        elif scene_name == "loading":

            self.scene = LoadingScene(
                self.screen,
                self.assets,
                self.test_type
            )

        elif scene_name == "drawing":

            self.scene = DrawingScene(
                self.screen,
                self.assets,
                self.test_type
            )

        elif scene_name == "results":

            self.scene = ResultsScene(
                self.screen,
                self.assets,
                self.test_type,
                self.prediction,
                self.confidence
            )

    def handle_menu_action(self, action):

        if action == "start":
            self.change_scene("selection")

        elif action == "quit":
            self.running = False

    def handle_selection_action(self, action):

        if action == "spiral":
            self.test_type = "spiral"
            self.change_scene("instructions")

        elif action == "wave":
            self.test_type = "wave"
            self.change_scene("instructions")

        elif action == "back":
            self.change_scene("menu")

    def handle_instructions_action(self, action):

        if action == "start":
            self.change_scene("loading")

        elif action == "back":
            self.change_scene("selection")

    def handle_drawing_action(self, action):

        if not action:
            return

        if action["action"] == "results":

            self.audio.play_sound("submit")

            self.prediction = action["prediction"]
            self.confidence = action["confidence"]

            self.change_scene("results")

        elif action["action"] == "back":
            self.change_scene("instructions")

    def handle_results_action(self, action):

        if action == "retry":
            self.change_scene("instructions")

        elif action == "home":
            self.change_scene("menu")

    def run(self):

        while self.running:

            self.clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.running = False
                    continue

                if self.current_scene == "selection":
                    action = self.scene.handle_event(event)
                    self.handle_selection_action(action)

                elif self.current_scene == "instructions":
                    action = self.scene.handle_event(event)
                    self.handle_instructions_action(action)

                elif self.current_scene == "drawing":
                    action = self.scene.handle_event(event)
                    self.handle_drawing_action(action)

                elif self.current_scene == "results":
                    action = self.scene.handle_event(event)
                    self.handle_results_action(action)

            if not self.running:
                break

            action = self.scene.draw()

            if self.current_scene == "menu":
                self.handle_menu_action(action)

            elif self.current_scene == "loading":

                if self.scene.is_complete():
                    self.change_scene("drawing")

            pygame.display.flip()

        self.audio.stop_music()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":

    game = ParkinsonsGame()
    game.run()