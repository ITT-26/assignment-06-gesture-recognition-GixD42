# gesture input program for first task

import pyglet
from recognizer_helper import Point
from recognizer import DollarRecognizer


class GestureInputWindow(pyglet.window.Window):
    def __init__(self, width=600, height=600):
        # input field
        super().__init__(width, height)
        pyglet.gl.glClearColor(1, 1, 1, 1)

        # points and lines are stored here
        self.points = []
        self.lines = []

        # recognizer
        self.recognizer = DollarRecognizer()

        # check if user is drawing
        self.drawing = False

        # drawing batch
        self.batch = pyglet.graphics.Batch()

        # result display
        self.result_text = "Draw a gesture"
        self.result_label = pyglet.text.Label(
            self.result_text,
            x=15,
            y=height - 25,
            font_size=14,
            color=(20, 20, 20, 255),
            batch=self.batch
        )

    # clears everything
    def clear_batch(self):
        for line in self.lines:
            line.delete()
        self.points = []
        self.lines = []

    # draw event
    def on_draw(self):
        # clear the window and redraw the batch
        super().clear()
        self.batch.draw()

    # left mouse press starts drawing
    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            # clear previous drawing
            self.clear_batch()
            # start drawing and add first point
            self.drawing = True
            self.points = [(x, y)]

    # mouse drag
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        # doesn't do anything if not drawing
        if not self.drawing:
            return

        # previous point
        px, py = self.points[-1]
        # add new point
        self.points.append((x, y))
        # line from previous point to new point
        self.lines.append(
            pyglet.shapes.Line(
                px, py, x, y,
                thickness=5,
                color=(0, 0, 0),
                batch=self.batch
            )
        )

    # left mouse release stops drawing
    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.drawing = False

            if self.recognizer and len(self.points) > 1:
                candidate = [Point(px, self.height - py)
                             for px, py in self.points]
                result = self.recognizer.recognize(candidate)
                self.result_text = f"Erkannt: {result.name} | Score: {result.score:.3f}"
                self.result_label.text = self.result_text

    # C key clears the drawing
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.C:
            self.clear_batch()
            self.result_text = "Draw a gesture"
            self.result_label.text = self.result_text


# for testing
def main():
    GestureInputWindow()
    pyglet.app.run()


if __name__ == "__main__":
    main()
