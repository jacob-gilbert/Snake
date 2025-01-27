import tkinter # graphical user interface library
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

COLOR_LIST_SNAKE = ["lime green", "blue", "maroon", "orange", "white", "purple"]
COLOR_LIST_FOOD = ["red", "light salmon", "coral", "light coral", "tomato", "hot pink",
                   "light pink", "pale violet red", "violet red", "dark orchid", "blue violet", "teal"]

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
    

def change_color_snake():
    global color_index_snake

    color_index_snake = (color_index_snake + 1) % len(COLOR_LIST_SNAKE)


def change_color_food():
    global color_index_food

    color_index_food = (color_index_food + 1) % len(COLOR_LIST_FOOD)


def gamemode_change():
    global gamemode

    gamemode = (gamemode + 1) % 2


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

        food.x = random.randint(0,COLS-1) * TILE_SIZE # change the food's location
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        while (food.x == poison1.x and food.y == poison1.y): # make sure the food is not in the same place as the poison
            food.x = random.randint(0,COLS-1) * TILE_SIZE
            food.y = random.randint(0, ROWS-1) * TILE_SIZE

        score += 1

    # check poison collision
    if gamemode == 1:
        if (snake.x == poison1.x and snake.y == poison1.y):
            if len(snake_body) + 1 - 3 > 0: # snake can survive the poison
                snake_body = snake_body[:len(snake_body) - 3] # loses 3 cubes

                poison1.x = random.randint(0,COLS-1) * TILE_SIZE # change the poison's location
                poison1.y = random.randint(0, ROWS-1) * TILE_SIZE
                while (food.x == poison1.x and food.y == poison1.y): # make sure the poison is not in the same place as the food
                    poison1.x = random.randint(0,COLS-1) * TILE_SIZE
                    poison1.y = random.randint(0, ROWS-1) * TILE_SIZE

                score -= 3
            else:
                game_over = True
                return
            
        elif score >= 15:
            if (snake.x == poison2.x and snake.y == poison2.y):
                if len(snake_body) + 1 - 3 > 0: # snake can survive the poison
                    snake_body = snake_body[:len(snake_body) - 3] # loses 3 cubes

                    poison2.x = random.randint(0,COLS-1) * TILE_SIZE # change the poison's location
                    poison2.y = random.randint(0, ROWS-1) * TILE_SIZE
                    while ((food.x == poison2.x and food.y == poison2.y) or (poison2.x == poison1.x and poison2.y == poison1.y)): # make sure the poison is not in the same place as the food
                        poison2.x = random.randint(0,COLS-1) * TILE_SIZE
                        poison2.y = random.randint(0, ROWS-1) * TILE_SIZE

                    score -= 3
                else:
                    game_over = True
                    return
                
            elif score >= 35:
                if (snake.x == poison3.x and snake.y == poison3.y):
                    if len(snake_body) + 1 - 3 > 0: # snake can survive the poison
                        snake_body = snake_body[:len(snake_body) - 3] # loses 3 cubes

                        poison2.x = random.randint(0,COLS-1) * TILE_SIZE # change the poison's location
                        poison2.y = random.randint(0, ROWS-1) * TILE_SIZE
                        while ((food.x == poison3.x and food.y == poison3.y) or (poison3.x == poison1.x and poison3.y == poison1.y) or (poison3.x == poison2.x and poison3.y == poison2.y)): # make sure the poison is not in the same place as the food
                            poison2.x = random.randint(0,COLS-1) * TILE_SIZE
                            poison2.y = random.randint(0, ROWS-1) * TILE_SIZE

                        score -= 3
                    else:
                        game_over = True
                        return


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
    global snake, food, snake_body, game_over, score, gamemode, poison1
    move()

    canvas.delete("all")

    # draw tile
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill=COLOR_LIST_FOOD[color_index_food])

    # draw poison
    if gamemode == 1 and score < 100:
        canvas.create_rectangle(poison1.x, poison1.y, poison1.x + TILE_SIZE, poison1.y + TILE_SIZE, fill="yellow")

        if score >= 15:
            canvas.create_rectangle(poison2.x, poison2.y, poison2.x + TILE_SIZE, poison2.y + TILE_SIZE, fill="yellow")

            if score >= 35:
                canvas.create_rectangle(poison3.x, poison3.y, poison3.x + TILE_SIZE, poison3.y + TILE_SIZE, fill="yellow")

    # draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill=COLOR_LIST_SNAKE[color_index_snake])

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill=COLOR_LIST_SNAKE[color_index_snake])

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
poison1 = Tile(15*TILE_SIZE,15*TILE_SIZE)
poison2 = Tile(3*TILE_SIZE,16*TILE_SIZE)
poison3 = Tile(8*TILE_SIZE,13*TILE_SIZE)
snake_body = [] # list of tile objects
velocityX = 0
velocityY = 0
game_over = False
score = 0
num_games = 1
highscore = 0
color_index_snake = 0 # the index number relates to the color of the snake
color_index_food = 0
gamemode = 0

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
                      background="gold", foreground="white")
games_played.pack(fill = "x")

# creating a high score tracker of all the games played
high_score = tkinter.Label(frame, text=f"Highscore\n{highscore}", font=("Consolas", 20),
                      background="silver", foreground="white")
high_score.pack(fill = "x")

# creating a restart button
restart_button = tkinter.Button(frame, text="Restart", font=("Consolas", 16), background="red",
                        foreground="white", command=new_game)
restart_button.pack(fill = "x")

# creating a color change button for the snake
color_change_s = tkinter.Button(frame, text="Change\nSnake", font=("Consolas", 16), background="lime green",
                        foreground="white", command=change_color_snake)
color_change_s.pack(fill = "x")

# creating a color change button for the food
color_change_b = tkinter.Button(frame, text="Change\nFood", font=("Consolas", 16), background="blue violet",
                        foreground="white", command=change_color_food)
color_change_b.pack(fill = "x")

# creating a button to activate the second gamemode
change_gamemode = tkinter.Button(frame, text="Change\nMode", font=("Consolas", 16), background="navy",
                        foreground="white", command=gamemode_change)
change_gamemode.pack(fill = "x")

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