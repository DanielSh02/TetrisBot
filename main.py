import itertools

import pyglet
import classes
from pyglet import shapes
from pyglet.window import key

TIME_INCREMENT = 1 / 2

SCALE = 40
WHITE = 255, 255, 255

game_window = pyglet.window.Window(16 * SCALE, 24 * SCALE, caption='Tetris')
gamestate = classes.Tetris()

def update(dt):
    gamestate.down()

@game_window.event
def on_draw():
    batch = pyglet.graphics.Batch()
    game_window.clear()

    # Draw all the pieces in the board
    blocks = []
    for i in range(10):
        for j in range(24):
            if gamestate.board[i][j] is not None:
                block = shapes.Rectangle((2 + i - 0.05) * SCALE, (2 + j - 0.05) * SCALE, SCALE * 0.9, SCALE * 0.9,
                                         color=gamestate.board[i][j], batch=batch)
                blocks.append(block)
    # Draw the current piece
    for block in gamestate.current_piece.squares:
        i = block[0]
        j = block[1]
        if j < 20:
            square = shapes.Rectangle((2 + i - 0.05) * SCALE, (2 + j - 0.05) * SCALE, SCALE * 0.9, SCALE * 0.9,
                                  color=gamestate.current_piece.color, batch=batch)
            blocks.append(square)
    # Draw the edges of the game boarda
    borders = []
    xlist = [2 * SCALE, 12 * SCALE]
    ylist = [2 * SCALE, 22 * SCALE]
    for x in xlist:
        line = shapes.Line(x, ylist[0], x, ylist[1], color=WHITE, batch=batch)
        borders.append(line)
    for y in ylist:
        line = shapes.Line(xlist[0], y, xlist[1], y, color=WHITE, batch=batch)
        borders.append(line)

    batch.draw()

@game_window.event
def on_key_press(symbol, modifiers):
    if symbol in [key.SPACE]:
        gamestate.drop()
    if symbol in [key.S, key.DOWN]:
        gamestate.down()
    if symbol in [key.A, key.LEFT]:
        gamestate.side([-1, 0])
    if symbol in [key.D, key.RIGHT]:
        gamestate.side([1, 0])
    if symbol in [key.W, key.UP]:
        gamestate.rotate_clockwise()

if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, TIME_INCREMENT)
    pyglet.app.run()