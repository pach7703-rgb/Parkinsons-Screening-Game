import pygame


class Button:

    # Shared audio manager for all buttons
    audio_manager = None

    @classmethod
    def set_audio_manager(cls, audio_manager):
        cls.audio_manager = audio_manager

    def __init__(self, x, y, image, scale=1):

        width = int(image.get_width() * scale)
        height = int(image.get_height() * scale)

        self.image = pygame.transform.smoothscale(
            image, (width, height)
        )

        self.rect = self.image.get_rect(topleft=(x, y))

        self.clicked = False
        self.hovered = False

        # Track whether the mouse was previously over the button
        self.was_hovered = False

    def draw(self, screen):

        action = False

        mouse_pos = pygame.mouse.get_pos()

        self.hovered = self.rect.collidepoint(mouse_pos)

        # Play hover sound only when mouse enters button
        if self.hovered and not self.was_hovered:

            if Button.audio_manager is not None:
                Button.audio_manager.play_sound("hover")

        self.was_hovered = self.hovered

        # Display button
        screen.blit(self.image, self.rect)

        # Mouse click detection
        if self.hovered:

            if pygame.mouse.get_pressed()[0] and not self.clicked:

                self.clicked = True
                action = True

                # Play click sound
                if Button.audio_manager is not None:
                    Button.audio_manager.play_sound("click")

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        return action