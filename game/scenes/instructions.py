import pygame

from game.settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    CYAN,
    GREY
)

from game.utilities.buttons import Button


class InstructionsScene:

    def __init__(self, screen, assets, test_type):

        self.screen = screen
        self.assets = assets

        self.test_type = test_type

        self.background = assets["backgrounds"]["instructions"]

        self.title_font = pygame.font.SysFont(
            "Arial", 45, bold=True
        )

        self.heading_font = pygame.font.SysFont(
            "Arial", 27, bold=True
        )

        self.text_font = pygame.font.SysFont(
            "Arial", 21
        )

        # Select reference image
        if self.test_type == "spiral":

            self.reference_image = assets["references"]["spiral"]

            self.instructions = [
                "Follow the spiral pattern shown on the screen.",
                "Use your mouse to draw the spiral.",
                "Try to keep your drawing as close to the reference as possible.",
                "Draw at a comfortable and natural pace.",
                "You can clear and redraw before submitting."
            ]

            self.title = "SPIRAL TEST"

        else:

            self.reference_image = assets["references"]["wave"]

            self.instructions = [
                "Follow the wave pattern shown on the screen.",
                "Use your mouse to draw the wave.",
                "Try to keep your drawing as close to the reference as possible.",
                "Draw at a comfortable and natural pace.",
                "You can clear and redraw before submitting."
            ]

            self.title = "WAVE TEST"

        self.start_button = Button(
            SCREEN_WIDTH - 330,
            620,
            assets["buttons"]["start_game"],
            scale=0.65
        )

        self.back_button = Button(
            55,
            620,
            assets["buttons"]["back"],
            scale=0.55
        )

    def draw_text(self, text, font, color, x, y):

        surface = font.render(text, True, color)

        rect = surface.get_rect(
            midleft=(x, y)
        )

        self.screen.blit(surface, rect)

    def draw(self):

        self.screen.blit(
            self.background,
            (0, 0)
        )

        self.draw_text(
            self.title,
            self.title_font,
            WHITE,
            100,
            90
        )

        self.draw_text(
            "TEST INSTRUCTIONS",
            self.heading_font,
            CYAN,
            100,
            165
        )

        # Display instructions
        for index, instruction in enumerate(self.instructions):

            y_position = 235 + index * 58

            self.draw_text(
                f"{index + 1}.",
                self.text_font,
                CYAN,
                105,
                y_position
            )

            self.draw_text(
                instruction,
                self.text_font,
                WHITE,
                145,
                y_position
            )

        # Reference drawing
        reference = pygame.transform.smoothscale(
            self.reference_image,
            (230, 230)
        )

        reference_rect = reference.get_rect(
            center=(SCREEN_WIDTH - 260, 340)
        )

        self.screen.blit(
            reference,
            reference_rect
        )

        self.draw_text(
            "REFERENCE PATTERN",
            self.text_font,
            CYAN,
            SCREEN_WIDTH - 260,
            485
        )

        # Buttons
        self.back_button.draw(self.screen)
        self.start_button.draw(self.screen)

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if self.start_button.rect.collidepoint(event.pos):
                    return "start"

                if self.back_button.rect.collidepoint(event.pos):
                    return "back"

        return None