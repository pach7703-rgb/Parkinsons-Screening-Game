import pygame

from game.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    CYAN,
    GREEN,
    AMBER,
    RED
)

from game.utilities.buttons import Button


class ResultsScene:

    def __init__(self, screen, assets, test_type, prediction, confidence):

        self.screen = screen
        self.assets = assets

        self.test_type = test_type.capitalize()
        self.prediction = prediction.lower()
        self.confidence = max(0, min(1, confidence))

        self.background = assets["backgrounds"]["results"]

        self.title_font = pygame.font.SysFont("Arial", 46, bold=True)
        self.heading_font = pygame.font.SysFont("Arial", 30, bold=True)
        self.result_font = pygame.font.SysFont("Arial", 27, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 21)
        self.small_font = pygame.font.SysFont("Arial", 17)

        self.retry_button = Button(
            370, 570,
            assets["buttons"]["retry"],
            scale=0.65
        )

        self.home_button = Button(
            700, 570,
            assets["buttons"]["home"],
            scale=0.65
        )

        if "parkinson" in self.prediction:
            self.result_text = "Parkinson's-associated pattern"
            self.result_color = AMBER
            self.result_label = "PATTERN DETECTED"

        else:
            self.result_text = "Healthy-associated pattern"
            self.result_color = GREEN
            self.result_label = "PATTERN DETECTED"

    def draw_text(self, text, font, color, x, y):

        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def draw_panel(self):

        panel = pygame.Surface((940, 390), pygame.SRCALPHA)

        pygame.draw.rect(
            panel,
            (8, 20, 42, 225),
            panel.get_rect(),
            border_radius=25
        )

        pygame.draw.rect(
            panel,
            (70, 190, 220, 150),
            panel.get_rect(),
            width=2,
            border_radius=25
        )

        self.screen.blit(panel, (170, 145))

    def draw_confidence_bar(self):

        bar_x = 390
        bar_y = 430
        bar_width = 500
        bar_height = 16

        pygame.draw.rect(
            self.screen,
            (65, 75, 95),
            (bar_x, bar_y, bar_width, bar_height),
            border_radius=8
        )

        fill_width = int(bar_width * self.confidence)

        if fill_width > 0:
            pygame.draw.rect(
                self.screen,
                CYAN,
                (bar_x, bar_y, fill_width, bar_height),
                border_radius=8
            )

    def draw(self):

        self.screen.blit(self.background, (0, 0))

        self.draw_text(
            "TEST RESULTS",
            self.title_font,
            WHITE,
            SCREEN_WIDTH // 2,
            90
        )

        self.draw_panel()

        self.draw_text(
            f"{self.test_type} TEST",
            self.heading_font,
            CYAN,
            SCREEN_WIDTH // 2,
            195
        )

        self.draw_text(
            "MODEL OUTPUT",
            self.small_font,
            WHITE,
            SCREEN_WIDTH // 2,
            255
        )

        self.draw_text(
            self.result_label,
            self.small_font,
            self.result_color,
            SCREEN_WIDTH // 2,
            300
        )

        self.draw_text(
            self.result_text,
            self.result_font,
            self.result_color,
            SCREEN_WIDTH // 2,
            345
        )

        self.draw_text(
            f"Model score: {self.confidence * 100:.1f}%",
            self.text_font,
            WHITE,
            SCREEN_WIDTH // 2,
            405
        )

        self.draw_confidence_bar()

        self.draw_text(
            "This is an experimental screening prototype, not a medical diagnosis.",
            self.small_font,
            AMBER,
            SCREEN_WIDTH // 2,
            475
        )

        self.draw_text(
            "The model score is not a clinical probability.",
            self.small_font,
            WHITE,
            SCREEN_WIDTH // 2,
            505
        )

        self.retry_button.draw(self.screen)
        self.home_button.draw(self.screen)

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.retry_button.rect.collidepoint(event.pos):
                return "retry"

            if self.home_button.rect.collidepoint(event.pos):
                return "home"

        return None