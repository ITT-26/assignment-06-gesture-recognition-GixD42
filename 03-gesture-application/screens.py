from pathlib import Path
import pyglet
from gesture_classifier import GestureClassifier
from constants import *


# represents the top half of the screen
class StartScreen:

    def __init__(self, window):

        # base window
        self.window = window

        # initial image
        base_dir = Path(__file__).resolve().parent
        image_path = base_dir / "assets" / START_SCREEN_IMAGE

        # load image and create sprite
        self.image = pyglet.image.load(str(image_path))
        self.sprite = pyglet.sprite.Sprite(
            self.image, x=0, y=window.height // 2)

    # change displayed image
    def change_image(self, image_path):
        self.image = pyglet.image.load(str(image_path))
        self.sprite = pyglet.sprite.Sprite(
            self.image, x=0, y=self.window.height // 2)

    # show image based on spell -> scheduled to reset after some time
    def show_spell(self, spell_image_path):
        self.change_image(spell_image_path)
        pyglet.clock.schedule_once(self.reset_image, SPELL_DURATION)

    # show basic background
    def reset_image(self, dt):
        self.change_image(BACKGROUND_IMAGE)

    # draw the sprite
    def draw(self):
        self.sprite.draw()


# represents the bottom half of the screen
class BottomScreen:

    def __init__(self, window, on_recognized=None):

        # base window and callback for recognized gestures
        self.window = window
        self.on_recognized = on_recognized

        # load background image
        base_dir = Path(__file__).resolve().parent
        image_path = base_dir / "assets" / "spellbook.png"

        # load image and create sprite
        self.image = pyglet.image.load(str(image_path))
        self.sprite = pyglet.sprite.Sprite(self.image, x=0, y=0)

        # input box adjusted according to the image
        self.box_x = 450
        self.box_y = 25
        self.box_w = 275
        self.box_h = 350

        # points for gesture
        self.points = []
        # is drawing
        self.is_drawing = False

        # input lock
        self.locked = False

        # gesture classifier
        self.classifier = GestureClassifier()
        self.last_prediction = ""

        # fields for the countdown displays
        self.star_countdown_label = pyglet.text.Label(
            "",
            x=COUNTDOWN_LABEL_X,
            y=COUNTDOWN_LABEL_Y_START,
            font_size=COUNTDOWN_LABEL_FONT_SIZE,
            color=COUNTDOWN_LABEL_COLOR
        )

        self.earth_countdown_label = pyglet.text.Label(
            "",
            x=COUNTDOWN_LABEL_X,
            y=COUNTDOWN_LABEL_Y_START - COUNTDOWN_LABEL_Y_STEP,
            font_size=COUNTDOWN_LABEL_FONT_SIZE,
            color=COUNTDOWN_LABEL_COLOR
        )

        self.beam_countdown_label = pyglet.text.Label(
            "",
            x=COUNTDOWN_LABEL_X,
            y=COUNTDOWN_LABEL_Y_START - 2 * COUNTDOWN_LABEL_Y_STEP,
            font_size=COUNTDOWN_LABEL_FONT_SIZE,
            color=COUNTDOWN_LABEL_COLOR
        )

    # lock input when spell is active
    def set_locked(self, locked):
        self.locked = locked

    # check if (x ,y) is inside the input box
    def inside_box(self, x, y):
        if self.box_x <= x <= self.box_x + self.box_w and self.box_y <= y <= self.box_y + self.box_h:
            return True
        return False

    # mouse event handlers for drawing and gesture recognition
    def on_mouse_press(self, x, y):
        if self.inside_box(x, y):
            self.is_drawing = True
            self.points = [(x, y)]

    def on_mouse_drag(self, x, y):
        if self.is_drawing and self.inside_box(x, y):
            self.points.append((x, y))

    def on_mouse_release(self):
        if not self.is_drawing:
            return

        self.is_drawing = False

        label, conf = self.classifier.predict(self.points)

        if self.on_recognized:
            self.on_recognized(label, conf)

        self.points = []

    # draw the bottom screen
    def draw(self):

        # background
        self.sprite.draw()

        # input box
        pyglet.shapes.Box(
            self.box_x, self.box_y, self.box_w, self.box_h,
            thickness=5, color=(150, 0, 0)
        ).draw()

        # countdown text update
        self.star_countdown_label.text = f"{self.window.star_countdown:.1f}s"
        self.beam_countdown_label.text = f"{self.window.beam_countdown:.1f}s"
        self.earth_countdown_label.text = f"{self.window.earth_countdown:.1f}s"

        # draw countdowns
        self.star_countdown_label.draw()
        self.beam_countdown_label.draw()
        self.earth_countdown_label.draw()

        # if locked darken the input area
        if self.locked:
            overlay = pyglet.shapes.Rectangle(
                self.box_x, self.box_y, self.box_w, self.box_h,
                color=(120, 120, 120)
            )
            overlay.opacity = 160
            overlay.draw()
            return

        # drawn gesture
        for i in range(1, len(self.points)):
            x0, y0 = self.points[i - 1]
            x1, y1 = self.points[i]
            pyglet.shapes.Line(
                x0, y0, x1, y1, thickness=9, color=(150, 120, 80)
            ).draw()


if __name__ == "__main__":
    # Nur fuer Optik-Preview: Modell-Laden vermeiden
    class _DummyClassifier:
        def predict(self, points):
            return None, 0.0

    # Monkeypatch: BottomScreen.__init__ nutzt dann den Dummy statt echtem Modell
    GestureClassifier = _DummyClassifier

    class PreviewWindow(pyglet.window.Window):
        def __init__(self):
            super().__init__(800, 800, "Screens Preview", resizable=False)

            # fuer cooldown-text in BottomScreen.draw()
            self.star_countdown = 12.3
            self.beam_countdown = 4.8
            self.earth_countdown = 0.0

            self.top_screen = StartScreen(self)
            self.bottom_screen = BottomScreen(self)

        def on_draw(self):
            self.clear()
            self.bottom_screen.draw()
            self.top_screen.draw()

    win = PreviewWindow()

    pyglet.app.run()
