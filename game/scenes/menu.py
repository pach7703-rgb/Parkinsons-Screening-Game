import pygame

from game.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    WHITE, CYAN, BLUE, GREY, GREEN
)

from game.utilities.buttons import Button


class MenuScene:

    def __init__(self, screen, assets):

        self.screen = screen
        self.assets = assets
        self.background = assets["backgrounds"]["menu"]
        self.audio = Button.audio_manager

        self.title_font = pygame.font.SysFont("Arial", 58, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 23)
        self.heading_font = pygame.font.SysFont("Arial", 34, bold=True)
        self.text_font = pygame.font.SysFont("Arial", 22)
        self.small_font = pygame.font.SysFont("Arial", 17)

        button_width = 273
        center_x = (SCREEN_WIDTH - button_width) // 2

        self.start_button = Button(
            center_x, 330, assets["buttons"]["start"], scale=0.65
        )

        self.settings_button = Button(
            center_x, 420, assets["buttons"]["settings"], scale=0.65
        )

        self.about_button = Button(
            center_x, 510, assets["buttons"]["about"], scale=0.65
        )

        self.exit_button = Button(
            center_x, 600, assets["buttons"]["exit"], scale=0.65
        )

        self.back_button = Button(
            530, 520, assets["buttons"]["back"], scale=0.55
        )

        self.show_about = False
        self.show_settings = False

        self.previous_mouse_down = False
        self.dragging_slider = None

        self.panel_rect = pygame.Rect(300, 145, 680, 440)

        self.music_toggle_rect = pygame.Rect(750, 270, 90, 38)
        self.sound_toggle_rect = pygame.Rect(750, 345, 90, 38)

        self.music_slider_rect = pygame.Rect(490, 425, 350, 8)
        self.sound_slider_rect = pygame.Rect(490, 495, 350, 8)

    def draw_text(self, text, font, color, x, y):

        surface = font.render(text, True, color)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)

    def draw_panel_background(self):

        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA
        )
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (0, 0))

        pygame.draw.rect(
            self.screen, (15, 29, 55),
            self.panel_rect, border_radius=18
        )

        pygame.draw.rect(
            self.screen, CYAN,
            self.panel_rect, width=2, border_radius=18
        )

    def draw_slider(self, rect, value):

        pygame.draw.rect(
            self.screen, (65, 80, 105), rect, border_radius=5
        )

        fill_width = int(rect.width * value)

        pygame.draw.rect(
            self.screen, CYAN,
            (rect.x, rect.y, fill_width, rect.height),
            border_radius=5
        )

        pygame.draw.circle(
            self.screen, WHITE,
            (rect.x + fill_width, rect.centery), 11
        )

    def draw_toggle(self, rect, enabled):

        color = GREEN if enabled else (100, 110, 125)

        pygame.draw.rect(
            self.screen, color, rect, border_radius=18
        )

        knob_x = rect.right - 19 if enabled else rect.left + 19

        pygame.draw.circle(
            self.screen, WHITE, (knob_x, rect.centery), 14
        )

        self.draw_text(
            "ON" if enabled else "OFF",
            self.small_font, WHITE,
            rect.centerx, rect.centery
        )

    def update_slider(self, rect, mouse_x):

        value = (mouse_x - rect.x) / rect.width
        return max(0.0, min(1.0, value))

    def handle_panel_interaction(self):

        mouse_pos = pygame.mouse.get_pos()
        mouse_down = pygame.mouse.get_pressed()[0]

        just_pressed = mouse_down and not self.previous_mouse_down

        if self.show_settings:

            if just_pressed:

                if self.music_toggle_rect.collidepoint(mouse_pos):
                    self.audio.toggle_music()

                elif self.sound_toggle_rect.collidepoint(mouse_pos):
                    self.audio.toggle_sound()

                elif self.music_slider_rect.inflate(0, 25).collidepoint(mouse_pos):
                    self.dragging_slider = "music"

                elif self.sound_slider_rect.inflate(0, 25).collidepoint(mouse_pos):
                    self.dragging_slider = "sound"

            if mouse_down and self.dragging_slider == "music":
                value = self.update_slider(
                    self.music_slider_rect, mouse_pos[0]
                )
                self.audio.set_music_volume(value)

            elif mouse_down and self.dragging_slider == "sound":
                value = self.update_slider(
                    self.sound_slider_rect, mouse_pos[0]
                )
                self.audio.set_sound_volume(value)

            if not mouse_down:
                self.dragging_slider = None

        self.previous_mouse_down = mouse_down

    def draw_settings_panel(self):

        self.draw_panel_background()

        self.draw_text(
            "SETTINGS", self.heading_font, WHITE,
            SCREEN_WIDTH // 2, 190
        )

        self.draw_text(
            "Background Music", self.text_font, WHITE, 430, 288
        )

        self.draw_text(
            "Sound Effects", self.text_font, WHITE, 430, 363
        )

        self.draw_text(
            "Music Volume", self.text_font, WHITE, 390, 425
        )

        self.draw_text(
            "Sound Volume", self.text_font, WHITE, 390, 495
        )

        self.draw_toggle(
            self.music_toggle_rect, self.audio.music_enabled
        )

        self.draw_toggle(
            self.sound_toggle_rect, self.audio.sound_enabled
        )

        self.draw_slider(
            self.music_slider_rect, self.audio.music_volume
        )

        self.draw_slider(
            self.sound_slider_rect, self.audio.sound_volume
        )

        # Back button click is handled directly here
        return self.back_button.draw(self.screen)

    def draw_about_panel(self):

        self.draw_panel_background()

        self.draw_text(
            "ABOUT THE PROJECT", self.heading_font, WHITE,
            SCREEN_WIDTH // 2, 195
        )

        information = [
            "An AI-assisted drawing-based screening prototype.",
            "Designed to explore motor patterns associated with",
            "Parkinson's disease using spiral and wave drawings.",
            "",
            "Technologies Used",
            "Python  |  Pygame  |  Machine Learning",
            "Random Forest  |  HOG Feature Extraction",
            "",
            "This project is an educational research prototype.",
            "It is not a medical diagnostic tool."
        ]

        for index, line in enumerate(information):

            color = CYAN if line == "Technologies Used" else WHITE

            self.draw_text(
                line, self.small_font, color,
                SCREEN_WIDTH // 2, 265 + index * 27
            )

        return self.back_button.draw(self.screen)

    def draw(self):

        self.screen.blit(self.background, (0, 0))

        self.draw_text(
            "PARKINSON'S SCREENING",
            self.title_font, WHITE,
            SCREEN_WIDTH // 2, 145
        )

        self.draw_text(
            "An Interactive AI-Assisted Screening Experience",
            self.subtitle_font, CYAN,
            SCREEN_WIDTH // 2, 205
        )

        self.draw_text(
            "DRAW  •  EXPLORE  •  ANALYSE",
            self.subtitle_font, BLUE,
            SCREEN_WIDTH // 2, 260
        )

        if self.show_settings:

            if self.draw_settings_panel():
                self.show_settings = False
                self.dragging_slider = None
                self.previous_mouse_down = True

            else:
                self.handle_panel_interaction()

        elif self.show_about:

            if self.draw_about_panel():
                self.show_about = False
                self.previous_mouse_down = True

        else:

            self.previous_mouse_down = False

            if self.start_button.draw(self.screen):
                return "start"

            if self.settings_button.draw(self.screen):
                self.show_settings = True

            if self.about_button.draw(self.screen):
                self.show_about = True

            if self.exit_button.draw(self.screen):
                return "quit"

        return None