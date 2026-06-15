# gesture input program for first task

import pyglet


# points and lines are stored here
points = []
lines = []

# check if user is drawing
drawing = False

# input field
window = pyglet.window.Window(900, 600)
pyglet.gl.glClearColor(1, 1, 1, 1)

# drawing batch
batch = pyglet.graphics.Batch()


# clears everything
def clear():
    global points, lines
    for line in lines:
        line.delete()
    points = []
    lines = []


# draw event
@window.event
def on_draw():
    # clear the window and redraw the batch
    window.clear()
    batch.draw()


# left mouse press starts drawing
@window.event
def on_mouse_press(x, y, button, modifiers):
    global drawing, points
    if button == pyglet.window.mouse.LEFT:
        # clear previous drawing
        clear()
        # start drawing and add first point
        drawing = True
        points = [(x, y)]


# mouse drag
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):

    # doesn't do anything if not drawing
    if not drawing:
        return

    # previous point
    px, py = points[-1]
    # add new point
    points.append((x, y))
    # line from previous point to new point
    lines.append(
        pyglet.shapes.Line(
            px, py, x, y,
            thickness=5,
            color=(0, 0, 0),
            batch=batch
        )
    )


# left mouse release stops drawing
@window.event
def on_mouse_release(x, y, button, modifiers):
    global drawing
    if button == pyglet.window.mouse.LEFT:
        drawing = False


# C key clears the drawing
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.C:
        clear()


pyglet.app.run()
