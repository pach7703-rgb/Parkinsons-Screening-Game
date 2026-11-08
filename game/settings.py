from pathlib import Path

# Project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Game window settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
WINDOW_TITLE = "Parkinson's Screening Game"

# Colours
NAVY = (8, 15, 35)
DARK_BLUE = (12, 25, 55)
CYAN = (40, 190, 255)
BLUE = (50, 130, 255)
PURPLE = (155, 90, 255)
GREEN = (40, 220, 150)
AMBER = (255, 190, 50)
RED = (255, 75, 100)
WHITE = (255, 255, 255)
GREY = (150, 165, 185)

# Asset directories
ASSET_ROOT = (
    PROJECT_ROOT
    / "assets"
    / "Parkinsons_Game_Assets"
    / "Parkinsons_Game_Assets"
)

BACKGROUND_DIR = ASSET_ROOT / "backgrounds"
BUTTON_DIR = ASSET_ROOT / "buttons"
ICON_DIR = ASSET_ROOT / "icons"
REFERENCE_DIR = ASSET_ROOT / "references"

# Model directories
MODEL_DIR = PROJECT_ROOT / "models"

SPIRAL_MODEL = MODEL_DIR / "spiral_random_forest.joblib"
WAVE_MODEL = MODEL_DIR / "wave_random_forest.joblib"