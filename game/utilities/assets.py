import pygame
from pathlib import Path

from settings import (
    BACKGROUND_DIR,
    BUTTON_DIR,
    ICON_DIR,
    REFERENCE_DIR,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)


def load_image(folder, filename, size=None):
    """
    Loads an image from the specified asset folder.
    Optionally resizes the image.
    """

    image_path = Path(folder) / filename

    if not image_path.exists():
        raise FileNotFoundError(
            f"Asset not found: {image_path}"
        )

    image = pygame.image.load(str(image_path)).convert_alpha()

    if size:
        image = pygame.transform.smoothscale(image, size)

    return image


def load_background(filename):
    """
    Loads and resizes a background to fit the game window.
    """

    return load_image(
        BACKGROUND_DIR,
        filename,
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )


def load_button(filename, size=None):
    """
    Loads button graphics.
    """

    return load_image(
        BUTTON_DIR,
        filename,
        size
    )


def load_icon(filename, size=None):
    """
    Loads interface icons.
    """

    return load_image(
        ICON_DIR,
        filename,
        size
    )


def load_reference(filename):
    """
    Loads spiral or wave reference drawings.
    """

    return load_image(
        REFERENCE_DIR,
        filename
    )


def load_all_assets():
    """
    Loads all game assets into dictionaries.
    """

    assets = {}

    # Backgrounds
    assets["backgrounds"] = {
        "menu": load_background("menu_bg.png"),
        "selection": load_background("selection_bg.png"),
        "instructions": load_background("instruction_bg.png"),
        "loading": load_background("loading_bg.png"),
        "drawing": load_background("drawing_bg.png"),
        "results": load_background("result_bg.png")
    }

    # Buttons
    button_names = [
        "start", "settings", "about", "exit",
        "spiral_test", "wave_test", "start_game",
        "submit", "clear", "back", "retry",
        "home", "continue"
    ]

    assets["buttons"] = {
        name: load_button(f"{name}.png")
        for name in button_names
    }

    # Icons
    icon_names = [
        "brain", "caution", "consult", "help",
        "home_icon", "info", "loading_spinner",
        "normal", "progress_bar_sample",
        "settings_icon", "sound_off", "sound_on"
    ]

    assets["icons"] = {
        name: load_icon(f"{name}.png")
        for name in icon_names
    }

    # Reference drawings
    assets["references"] = {
        "spiral": load_reference("spiral_reference.png"),
        "wave": load_reference("wave_reference.png")
    }

    print("All game assets loaded successfully!")

    return assets