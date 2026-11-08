import pygame
import numpy as np
import joblib

from PIL import Image
from skimage.feature import hog

from game.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    CYAN,
    GREY,
    GREEN,
    RED,
    SPIRAL_MODEL,
    WAVE_MODEL
)

from game.utilities.buttons import Button


class DrawingScene:

    def __init__(self, screen, assets, test_type):

        self.screen = screen
        self.assets = assets
        self.test_type = test_type

        self.background = assets["backgrounds"]["drawing"]

        self.title_font = pygame.font.SysFont(
            "Arial", 34, bold=True
        )

        self.text_font = pygame.font.SysFont(
            "Arial", 20
        )

        self.small_font = pygame.font.SysFont(
            "Arial", 17
        )

        # Drawing canvas
        self.canvas_rect = pygame.Rect(
            100, 175, 760, 440
        )

        self.canvas = pygame.Surface(
            self.canvas_rect.size
        )

        self.canvas.fill(WHITE)

        self.drawing = False
        self.last_position = None
        self.has_drawing = False

        self.line_color = (15, 25, 45)
        self.line_width = 4

        # Reference pattern and model
        if test_type == "spiral":

            self.reference = assets["references"]["spiral"]
            model_path = SPIRAL_MODEL

        else:

            self.reference = assets["references"]["wave"]
            model_path = WAVE_MODEL

        self.reference = pygame.transform.smoothscale(
            self.reference,
            (180, 180)
        )

        model_bundle = joblib.load(str(model_path))
        self.model = model_bundle["model"]

        # Buttons
        self.clear_button = Button(
            900, 480,
            assets["buttons"]["clear"],
            scale=0.55
        )

        self.submit_button = Button(
            1060, 480,
            assets["buttons"]["submit"],
            scale=0.55
        )

        self.back_button = Button(
            55, 650,
            assets["buttons"]["back"],
            scale=0.45
        )

    def draw_text(self, text, font, color, x, y):

        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))

        self.screen.blit(surface, rect)

    def clear_canvas(self):

        self.canvas.fill(WHITE)

        self.drawing = False
        self.last_position = None
        self.has_drawing = False

    def get_features(self):

        # Convert Pygame canvas into a NumPy array
        image = pygame.surfarray.array3d(self.canvas)

        # Convert width x height x channels to height x width x channels
        image = np.transpose(image, (1, 0, 2))

        # Convert to grayscale
        image = Image.fromarray(image.astype(np.uint8))
        image = image.convert("L")

        # Resize exactly as during model training
        image = image.resize(
            (200, 200),
            Image.Resampling.LANCZOS
        )

        # Normalize pixel values
        pixels = np.asarray(image, dtype=np.float32) / 255.0

        # Extract HOG features
        features = hog(
            pixels,
            orientations=9,
            pixels_per_cell=(16, 16),
            cells_per_block=(2, 2),
            block_norm="L2-Hys",
            transform_sqrt=True,
            feature_vector=True
        )

        return features.reshape(1, -1)

    def analyse_drawing(self):

        features = self.get_features()

        prediction = self.model.predict(features)[0]

        probabilities = self.model.predict_proba(features)[0]

        confidence = float(np.max(probabilities))

        return prediction, confidence

    def draw(self):

        self.screen.blit(self.background, (0, 0))

        # Title
        self.draw_text(
            f"{self.test_type.upper()} DRAWING TEST",
            self.title_font,
            WHITE,
            SCREEN_WIDTH // 2,
            65
        )

        self.draw_text(
            "Draw the pattern inside the white area",
            self.text_font,
            CYAN,
            self.canvas_rect.centerx,
            125
        )

        # Canvas shadow
        shadow_rect = self.canvas_rect.copy()
        shadow_rect.move_ip(6, 6)

        pygame.draw.rect(
            self.screen,
            (15, 20, 35),
            shadow_rect,
            border_radius=10
        )

        # Canvas background
        pygame.draw.rect(
            self.screen,
            WHITE,
            self.canvas_rect,
            border_radius=8
        )

        self.screen.blit(
            self.canvas,
            self.canvas_rect.topleft
        )

        # Canvas border
        pygame.draw.rect(
            self.screen,
            CYAN,
            self.canvas_rect,
            3,
            border_radius=8
        )

        # Reference section
        self.draw_text(
            "REFERENCE PATTERN",
            self.text_font,
            WHITE,
            1060,
            175
        )

        reference_rect = self.reference.get_rect(
            center=(1060, 300)
        )

        pygame.draw.rect(
            self.screen,
            WHITE,
            reference_rect.inflate(12, 12),
            border_radius=8
        )

        self.screen.blit(
            self.reference,
            reference_rect
        )

        self.draw_text(
            "Follow the pattern as closely",
            self.small_font,
            WHITE,
            1060,
            420
        )

        self.draw_text(
            "as you comfortably can.",
            self.small_font,
            WHITE,
            1060,
            445
        )

        # Buttons
        self.clear_button.draw(self.screen)
        self.submit_button.draw(self.screen)
        self.back_button.draw(self.screen)

        self.draw_text(
            "Clear your drawing and try again if needed.",
            self.small_font,
            GREY,
            SCREEN_WIDTH // 2,
            650
        )

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if self.canvas_rect.collidepoint(event.pos):

                    self.drawing = True

                    self.last_position = (
                        event.pos[0] - self.canvas_rect.x,
                        event.pos[1] - self.canvas_rect.y
                    )

                    self.has_drawing = True

                elif self.clear_button.rect.collidepoint(event.pos):

                    self.clear_canvas()

                elif self.submit_button.rect.collidepoint(event.pos):

                    if self.has_drawing:

                        prediction, confidence = self.analyse_drawing()

                        return {
                            "action": "results",
                            "prediction": str(prediction),
                            "confidence": confidence
                        }

                elif self.back_button.rect.collidepoint(event.pos):

                    return {"action": "back"}

        elif event.type == pygame.MOUSEMOTION:

            if self.drawing:

                if self.canvas_rect.collidepoint(event.pos):

                    current_position = (
                        event.pos[0] - self.canvas_rect.x,
                        event.pos[1] - self.canvas_rect.y
                    )

                    if self.last_position is not None:

                        pygame.draw.line(
                            self.canvas,
                            self.line_color,
                            self.last_position,
                            current_position,
                            self.line_width
                        )

                        pygame.draw.circle(
                            self.canvas,
                            self.line_color,
                            current_position,
                            self.line_width // 2
                        )

                    self.last_position = current_position

                else:

                    self.last_position = None

        elif event.type == pygame.MOUSEBUTTONUP:

            if event.button == 1:

                self.drawing = False
                self.last_position = None

        return None