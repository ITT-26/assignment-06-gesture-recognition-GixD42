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

SPELL_THRESHOLD = 0.8

STAR_COOLDOWN = 20
BEAM_COOLDOWN = 5
EARTH_COOLDOWN = 5

SPELL_DURATION = 1.5

COUNTDOWN_LABEL_X = 230
COUNTDOWN_LABEL_Y_START = 250
COUNTDOWN_LABEL_Y_STEP = 90
COUNTDOWN_LABEL_FONT_SIZE = 12
COUNTDOWN_LABEL_COLOR = (255, 255, 255)
