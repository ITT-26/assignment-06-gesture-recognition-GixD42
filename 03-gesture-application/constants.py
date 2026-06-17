# Constants for gesture application

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# list of gesture classes that can trigger a spell
SPELLS = ['star', 'delete_mark', 'pigtail']

# list of pictures corresponding to the spells
SPELL_TO_PICTURE = {
    'star': BASE_DIR / 'assets' / 'background_player_starfall.png',
    'delete_mark': BASE_DIR / 'assets' / 'background_player_earthshaker.png',
    'pigtail': BASE_DIR / 'assets' / 'background_player_skybeam.png'
}

START_SCREEN_IMAGE = BASE_DIR / 'assets' / 'startscreen_top.png'

BACKGROUND_IMAGE = BASE_DIR / 'assets' / 'background_player_blank.png'

GAME_OVER_IMAGE = BASE_DIR / 'assets' / 'game_over.png'

SPELL_THRESHOLD = 0.8

STAR_COOLDOWN = 20
BEAM_COOLDOWN = 5
EARTH_COOLDOWN = 5

SPELL_DURATION = 0.7

COUNTDOWN_LABEL_X = 230
COUNTDOWN_LABEL_Y_START = 250
COUNTDOWN_LABEL_Y_STEP = 90
COUNTDOWN_LABEL_FONT_SIZE = 12
COUNTDOWN_LABEL_COLOR = (255, 255, 255)

ENEMY_SPAWN_X = 800
ENEMY_FLY_Y = 550
ENEMY_GROUND_Y = 500
ENEMY_SPEED_MIN = 60
ENEMY_SPEED_MAX = 100

ENEMY_FLY_PATH = BASE_DIR / 'assets' / 'enemy1.png'
ENEMY_GROUND_PATH = BASE_DIR / 'assets' / 'enemy2.png'

ENEMY_SPAWN_TIME_MIN = 0.7
ENEMY_SPAWN_TIME_MAX = 1.3

ENEMY_X_LOST = 100

RIGHT_BORDER_X = 770
BORDER_WIDTH = 30
BORDER_COLOR = (0, 0, 0)

SCORE_Y = 550
SCORE_FONT_SIZE = 24
SCORE_COLOR = (0, 0, 0)