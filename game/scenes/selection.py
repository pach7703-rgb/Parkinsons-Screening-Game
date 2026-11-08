import pygame

from game.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    CYAN,
    GREY
)

from game.utilities.buttons import Button


class SelectionScene:

    def __init__(self, screen, assets):

        self.screen = screen
        self.assets = assets

        self.background = assets["backgrounds"]["selection"]

        self.title_font = pygame.font.SysFont(
            "Arial", 48, bold=True
        )

        self.description_font = pygame.font.SysFont(
            "Arial", 21
        )

        self.card_description_font = pygame.font.SysFont(
            "Arial", 19
        )

        # Test cards
        self.spiral_image = assets["buttons"]["spiral_test"]
        self.wave_image = assets["buttons"]["wave_test"]

        self.spiral_rect = self.spiral_image.get_rect(
            center=(SCREEN_WIDTH // 2 - 230, 350)
        )

        self.wave_rect = self.wave_image.get_rect(
            center=(SCREEN_WIDTH // 2 + 230, 350)
        )

        self.spiral_was_hovered = False
        self.wave_was_hovered = False

        self.audio = Button.audio_manager

        self.back_button = Button(
            55, 625,
            assets["buttons"]["back"],
            scale=0.55
        )

    def draw_text(self, text, font, color, x, y):

        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def draw_card(self, image, rect, mouse_pos, was_hovered):

        hovered = rect.collidepoint(mouse_pos)

        if hovered and not was_hovered and self.audio:
            self.audio.play_sound("hover")

        if hovered:
            scale = 1.08
        else:
            scale = 1.0

        width = int(rect.width * scale)
        height = int(rect.height * scale)

        scaled_image = pygame.transform.smoothscale(
            image,
            (width, height)
        )

        new_rect = scaled_image.get_rect(center=rect.center)
        self.screen.blit(scaled_image, new_rect)

        return hovered

    def draw(self):

        self.screen.blit(self.background, (0, 0))

        self.draw_text(
            "CHOOSE YOUR TEST",
            self.title_font,
            WHITE,
            SCREEN_WIDTH // 2,
            120
        )

        self.draw_text(
            "Select the drawing test you would like to perform",
            self.description_font,
            CYAN,
            SCREEN_WIDTH // 2,
            180
        )

        mouse_pos = pygame.mouse.get_pos()

        self.spiral_hovered = self.draw_card(
            self.spiral_image,
            self.spiral_rect,
            mouse_pos,
            self.spiral_was_hovered
        )

        self.wave_hovered = self.draw_card(
            self.wave_image,
            self.wave_rect,
            mouse_pos,
            self.wave_was_hovered
        )

        self.spiral_was_hovered = self.spiral_hovered
        self.wave_was_hovered = self.wave_hovered

        self.draw_text(
            "Draw a spiral pattern",
            self.card_description_font,
            WHITE,
            self.spiral_rect.centerx,
            self.spiral_rect.bottom + 45
        )

        self.draw_text(
            "Draw a wave pattern",
            self.card_description_font,
            WHITE,
            self.wave_rect.centerx,
            self.wave_rect.bottom + 45
        )

        self.back_button.draw(self.screen)

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if self.spiral_rect.collidepoint(event.pos):
                    return "spiral"

                if self.wave_rect.collidepoint(event.pos):
                    return "wave"

                if self.back_button.rect.collidepoint(event.pos):
                    return "back"

        return None