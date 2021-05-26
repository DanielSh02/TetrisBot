import pyglet
import classes
from pyglet import shapes
from pyglet.window import key

TIME_INCREMENT = 1 / 2

SCALE = 40
WHITE = 255, 255, 255

game_window = pyglet.window.Window(10 * SCALE, 24 * SCALE, caption='Tetris')
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
                block = shapes.Rectangle((i - 0.05) * SCALE, (j - 0.05) * SCALE, SCALE * 0.9, SCALE * 0.9,
                                         color=gamestate.board[i][j], batch=batch)
                blocks.append(block)
    # Draw the current piece
    for block in gamestate.current_piece.squares:
        i = block[0]
        j = block[1]
        square = shapes.Rectangle((i - 0.05) * SCALE, (j - 0.05) * SCALE, SCALE * 0.9, SCALE * 0.9,
                                  color=gamestate.current_piece.color, batch=batch)
        blocks.append(square)

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