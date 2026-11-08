import pygame
import math

from game.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    CYAN
)


class LoadingScene:

    def __init__(self, screen, assets, test_type):

        self.screen = screen
        self.assets = assets
        self.test_type = test_type

        self.background = assets["backgrounds"]["loading"]

        self.title_font = pygame.font.SysFont(
            "Arial", 38, bold=True
        )

        self.text_font = pygame.font.SysFont(
            "Arial", 22
        )

        self.start_time = pygame.time.get_ticks()
        self.duration = 2500

    def draw_text(self, text, font, color, x, y):

        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def draw(self):

        self.screen.blit(self.background, (0, 0))

        elapsed = pygame.time.get_ticks() - self.start_time

        progress = min(elapsed / self.duration, 1)

        self.draw_text(
            "PREPARING YOUR TEST",
            self.title_font,
            WHITE,
            SCREEN_WIDTH // 2,
            260
        )

        self.draw_text(
            f"Preparing {self.test_type.capitalize()} Test...",
            self.text_font,
            CYAN,
            SCREEN_WIDTH // 2,
            320
        )

        # Progress bar
        bar_width = 500
        bar_height = 18

        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = 390

        pygame.draw.rect(
            self.screen,
            (55, 65, 85),
            (bar_x, bar_y, bar_width, bar_height),
            border_radius=9
        )

        pygame.draw.rect(
            self.screen,
            CYAN,
            (bar_x, bar_y, int(bar_width * progress), bar_height),
            border_radius=9
        )

        self.draw_text(
            f"{int(progress * 100)}%",
            self.text_font,
            WHITE,
            SCREEN_WIDTH // 2,
            435
        )

    def is_complete(self):

        elapsed = pygame.time.get_ticks() - self.start_time

        return elapsed >= self.duration