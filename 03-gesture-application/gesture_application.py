# application for task 3

import pyglet
from screens import StartScreen, BottomScreen
from pyglet.window import mouse
from constants import *
from enemies import EnemyManager
import warnings
import logging
import os
print("loading application...")


os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

warnings.filterwarnings("ignore")
logging.getLogger("tensorflow").setLevel(logging.ERROR)


class GameWindow(pyglet.window.Window):

    def __init__(self):

        # window setup
        super().__init__(800, 800, "Gesture Magic", resizable=False)

        # screens
        self.top_screen = StartScreen(self)
        self.bottom_screen = BottomScreen(
            self, on_recognized=self.gesture_recognized)

        # did the game start
        self.started = False

        # is a spell active
        self.spell_active = False

        # cooldowns for spells
        self.star_countdown = 0
        self.beam_countdown = 0
        self.earth_countdown = 0

        # enemy manager
        self.enemy_manager = EnemyManager()

        # timer for score in game over screen
        self.timer = 0.0

        # update cooldowns every 0.1 seconds
        pyglet.clock.schedule_interval(self.update_countdowns, 0.1)

        # right border to let enemies spawn outside of the screen
        self.right_border = pyglet.shapes.Rectangle(
            RIGHT_BORDER_X, 0, BORDER_WIDTH, self.height, color=BORDER_COLOR
        )

    # update game
    def update_game(self, dt):

        # if it hasn't started don't update enemies
        if not self.started:
            return

        self.enemy_manager.update(dt, spell_active=self.spell_active)

        self.timer += dt

        for enemy in self.enemy_manager.enemies:
            if enemy.x < ENEMY_X_LOST:
                self.top_screen.show_game_over(self.timer)
                self.started = False
                self.spell_active = False
                self.enemy_manager.kill_all()
                pyglet.clock.unschedule(self.update_game)
                break

    # update cooldown timers
    def update_countdowns(self, dt):
        self.star_countdown = max(0, self.star_countdown - dt)
        self.beam_countdown = max(0, self.beam_countdown - dt)
        self.earth_countdown = max(0, self.earth_countdown - dt)

    # draw the window
    def on_draw(self):
        self.clear()
        self.bottom_screen.draw()
        self.top_screen.draw()

        # draw enemies before border
        self.enemy_manager.draw()
        self.right_border.draw()

    # mouse events are given to bottom screen if no spell active
    def on_mouse_press(self, x, y, button, modifiers):

        if self.spell_active:
            return

        if button == mouse.LEFT:
            self.bottom_screen.on_mouse_press(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):

        if self.spell_active:
            return

        if buttons & mouse.LEFT:
            self.bottom_screen.on_mouse_drag(x, y)

    def on_mouse_release(self, x, y, button, modifiers):

        if self.spell_active:
            return

        if button == mouse.LEFT:
            self.bottom_screen.on_mouse_release()

    # callback for when a gesture is recognized
    def gesture_recognized(self, label, conf):

        # only allow if game started
        if not self.started:
            return

        # only if a spell was recognized
        if label is None:
            return

        # only if confidence above threshold
        if conf < SPELL_THRESHOLD:
            return

        # check cooldowns
        if label == "star" and self.star_countdown > 0:
            return
        if label == "pigtail" and self.beam_countdown > 0:
            return
        if label == "delete_mark" and self.earth_countdown > 0:
            return

        # activate spell
        self.top_screen.show_spell(SPELL_TO_PICTURE.get(label))
        self.spell_active = True
        self.bottom_screen.set_locked(True)

        # schedule spell unlock
        pyglet.clock.schedule_once(self.unlock_spells, SPELL_DURATION)

        # set cooldowns and trigger spell effects
        if label == "star":
            self.star_countdown = STAR_COOLDOWN
            self.enemy_manager.kill_all()
        elif label == "pigtail":
            self.beam_countdown = BEAM_COOLDOWN
            self.enemy_manager.kill_all_flying()
        elif label == "delete_mark":
            self.earth_countdown = EARTH_COOLDOWN
            self.enemy_manager.kill_all_ground()

    # unlock spell and input after duration
    def unlock_spells(self, dt):
        self.spell_active = False
        self.bottom_screen.set_locked(False)

    # start the game on space press
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            if not self.started:
                self.started = True
                self.top_screen.change_image(BACKGROUND_IMAGE)
                self.timer = 0.0
                pyglet.clock.schedule_interval(self.update_game, 1 / 60)


# run the application
if __name__ == "__main__":
    window = GameWindow()
    pyglet.app.run()
