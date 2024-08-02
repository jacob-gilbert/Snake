import tkinter # graphical user interface library
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

COLOR_LIST = ["lime green", "blue", "yellow", "orange", "white", "purple"]

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def new_game():
    global snake, food, snake_body, velocityX, velocityY, game_over, score, highscore, num_games

    snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) # single tile for snake's head
    food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
    snake_body = [] # list of tile objects
    velocityX = 0
    velocityY = 0
    game_over = False
    if score > highscore:
        highscore = score
    score = 0
    num_games += 1
    games_played.config(text=f"Game {num_games}")


def update_high_score():
    global score, highscore

    if score > highscore:
        high_score.config(text=f"Highscore\n{score}")
        return 1
    elif score == highscore:
        return 0
    

def change_color():
    global color_index

    color_index = (color_index + 1) % len(COLOR_LIST)


def change_direction(keystroke):
    global velocityX, velocityY, game_over

    if(game_over):
        return

    if (keystroke.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1
    elif (keystroke.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    elif (keystroke.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0
    elif (keystroke.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0

def move():
    global snake, food, snake_body, game_over, score

    if(game_over):
        return
    
    if (snake.x < 0 or snake. x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return
    
    # check food collision
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0,COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    # update snake body
    for i in range(len(snake_body)-1, -1, -1):
        tile = snake_body[i]
        if (i == 0): # start of snake's body
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[i-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")

    # draw tile
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill="red")

    # draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill=COLOR_LIST[color_index])

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill=COLOR_LIST[color_index])

    window.after(100, draw) # after 100ms we call draw again which is 10 frames/sec

    if (game_over):
        highscore_outcome = update_high_score()
        if highscore_outcome == 1:
            canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20",
                           text=f"Game Over: {score}\nNew Highscore Achieved!\nYou beat your previous\nhighscore by {score - highscore}",
                           fill="red")
        elif highscore_outcome == 0:
            canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20",
                           text=f"Game Over: {score}\nYou Matched Your Previous Highscore!", fill="red")
        else:
            canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font="Arial 20",
                           text=f"Game Over: {score}", fill="red")
    else:
        canvas.create_text(30, 20, font="Arial 10", text=f"Score: {score}", fill="white")


# initialize game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) # single tile for snake's head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
snake_body = [] # list of tile objects
velocityX = 0
velocityY = 0
game_over = False
score = 0
num_games = 1
highscore = 0
color_index = 0 # the index number relates to the color of the snake

# game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False) # user cannot change the size of the window

frame = tkinter.Frame(window)
frame.pack()

canvas = tkinter.Canvas(frame, bg="black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth=0, highlightthickness=0)
canvas.pack(side=tkinter.LEFT)

# creating a tracker for the number of games played
games_played = tkinter.Label(frame, text=f"Game {num_games}", font=("Consolas", 20),
                      background="black", foreground="white")
games_played.pack(fill = "x")

# creating a high score tracker of all the games played
high_score = tkinter.Label(frame, text=f"Highscore\n{highscore}", font=("Consolas", 20),
                      background="black", foreground="white")
high_score.pack(fill = "x")

# creating a restart button
restart_button = tkinter.Button(frame, text="Restart", font=("Consolas", 16), background="red",
                        foreground="white", command=new_game)
restart_button.pack(fill = "x")

# creating a color change button
color_change = tkinter.Button(frame, text="Change\nColor", font=("Consolas", 16), background="lime green",
                        foreground="white", command=change_color)
color_change.pack(fill = "x")

window.update()

# center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight() - 75 # the -75 is specific to my screen

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

# format "(w)x(h)+(x)+(y)"
window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

draw()

window.bind("<KeyRelease>", change_direction) # when you release a key call the change direction function
window.mainloop()