# file for recording unistroke gestures, ai was used here to autocomplete code and make the progress go faster and code from task 1 was used as a base

import os
import time
import xml.etree.ElementTree as ET

import pyglet

CATEGORIES = [
    "arrow",
    "caret",
    "check",
    "circle",
    "delete_mark",
    "left_curly_brace",
    "left_sq_bracket",
    "pigtail",
    "rectangle",
    "right_curly_brace",
    "right_sq_bracket",
    "star",
    "triangle",
    "v",
    "x",
]


# path to save the dataset
OUT_DIR = os.path.join("datasets", "mylogs")
# repetitions per gesture
REPS = 10


# recorder window similar to gesture_input.py
class Recorder(pyglet.window.Window):
    def __init__(self):

        # window with background color
        super().__init__(600, 600, caption="Unistroke Recorder")
        pyglet.gl.glClearColor(1, 1, 1, 1)

        # tasks
        self.tasks = [(cat, i)
                      for cat in CATEGORIES for i in range(1, REPS + 1)]

        # index of current task
        self.idx = 0

        # points and lines
        self.points = []
        self.lines = []

        # check if user is drawing
        self.drawing = False

        # time
        self.t0 = 0.0

        # create output directory if it doesn't exist
        os.makedirs(OUT_DIR, exist_ok=True)

        # drawing batch and status label
        self.batch = pyglet.graphics.Batch()

        # feedback label
        self.label = pyglet.text.Label(
            "",
            x=10,
            y=575,
            font_size=12,
            color=(0, 0, 0),
            batch=self.batch,
        )

        # update feedback label
        self.update_status()

    # get current task
    def current(self):
        if self.idx >= len(self.tasks):
            return None
        return self.tasks[self.idx]

    # update feedback label
    def update_status(self):

        # get current task
        task = self.current()
        if task is None:
            self.label.text = "Done. ESC to exit."
            return

        # update label text with current task and controls
        name, rep = task
        self.label.text = (
            f"{name} ({rep}/{REPS}) | {self.idx + 1}/{len(self.tasks)} | "
            "ENTER to save, C to delete"
        )

    # clears batch and points
    def clear_batch(self):
        for line in self.lines:
            line.delete()
        self.lines = []
        self.points = []

    # save current gesture to xml
    def save(self):

        # get current task
        task = self.current()
        if task is None:
            return

        # too few points -> user has to do it again
        if len(self.points) < 2:
            self.clear_batch()
            return

        # save gesture to xml file
        gesture, rep = task
        name = f"{gesture}{rep:02d}"
        path = os.path.join(OUT_DIR, f"{name}.xml")
        duration = int(self.points[-1][2])

        # AI used for making xml write logic
        # gesture xml element
        root = ET.Element(
            "Gesture",
            {
                "Name": name,
                "Number": str(rep),
                "NumPts": str(len(self.points)),
                "Millseconds": str(duration),
            },
        )

        # point xml elements
        for x, y, t in self.points:
            ET.SubElement(
                root,
                "Point",
                {
                    "X": str(int(round(x))),
                    "Y": str(int(round(self.height - y))),
                    "T": str(int(t)),
                },
            )

        # xml to file
        tree = ET.ElementTree(root)
        try:
            ET.indent(tree, space="  ")
        except Exception:
            pass
        tree.write(path, encoding="utf-8", xml_declaration=True)

        # clear batch and points, move to next task
        self.clear_batch()
        self.idx += 1
        self.update_status()

    # draw event
    def on_draw(self):
        self.clear()
        self.batch.draw()

    # left mouse press starts drawing
    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT and self.current() is not None:
            self.clear_batch()
            self.drawing = True
            self.t0 = time.perf_counter()
            self.points.append((x, y, 0))

    # mouse drag adds points and lines
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if not self.drawing:
            return

        t = int((time.perf_counter() - self.t0) * 1000)
        px, py, _ = self.points[-1]
        self.points.append((x, y, t))
        self.lines.append(
            pyglet.shapes.Line(
                px,
                py,
                x,
                y,
                thickness=4,
                color=(0, 0, 0),
                batch=self.batch,
            )
        )

    # left mouse release ends drawing
    def on_mouse_release(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT and self.drawing:
            self.drawing = False
            t = int((time.perf_counter() - self.t0) * 1000)
            self.points.append((x, y, t))
            self.update_status()

    # key press for saving, deleting, or exiting
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.ENTER:
            self.save()
        elif symbol == pyglet.window.key.C:
            self.clear_batch()
            self.update_status()
        elif symbol == pyglet.window.key.ESCAPE:
            self.close()


if __name__ == "__main__":
    Recorder()
    pyglet.app.run()
