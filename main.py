from tkinter import *
import random

GAME_WIDTH = 750
GAME_HEIGHT = 550
SPEED = 170
SPACE_SIZE = 35
BODY_PARTS = 3
SNAKE_COLOR = '#0000ff'
FOOD_COLOR = '#FF0000'
BACKGROUND_COLOR = '#000000'


class Snake:
    def __init__(self) -> None:
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])
            
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE,y + SPACE_SIZE, fill=SNAKE_COLOR, tag="string of snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        num_spaces_x = GAME_WIDTH // SPACE_SIZE
        num_spaces_y = GAME_HEIGHT // SPACE_SIZE
        
        x = random.randint(0, num_spaces_x - 1) * SPACE_SIZE
        y = random.randint(0, num_spaces_y - 1) * SPACE_SIZE
        
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    #global SPEED
    
    x , y = snake.coordinates[0]
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction =="right":
        x += SPACE_SIZE
    
    snake.coordinates.insert(0, (x, y))
    
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y+ SPACE_SIZE, fill=SNAKE_COLOR)
    
    snake.squares.insert(0, square)
        
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        global SPEED
    
        score += 1
        if SPEED > 40: SPEED -= 10
        label.config(text="Score: {}".format(score))
        
        canvas.delete("food")
        
        food = Food()
    
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
        
    
    if check_collisions(snake):
        label.config(text="Game Over!")
        canvas.delete("snake")
        canvas.delete("food")
        window.bind('<space>', restart_game)
        
        return False
    else:
        window.after(SPEED, next_turn, snake, food)
    
    
def change_direction(new_direction):
    global direction
    
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    
    if x < 0 or x >= GAME_WIDTH:
        print("GAME OVER!")
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print("GAME OVER!")
        return True
        
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
        
    return False

#def click():
    myLabel = Label(window, text="Do you want to continue?")
    myLabel.pack()
    

def game_over():
    global game_over
    
    display_restart = canvas.render("press space to restart", True)
    canvas.blit(display_restart, (170, 450))
    game_over = True

def restart_game():
    global snake, food, score, direction

    # Reset game variables to initial values
    canvas.delete(ALL)
    snake = Snake()
    food = Food()
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    next_turn(snake, food)


window = Tk()
window.title('Snake Game')
window.resizable(True, True)

score = 0
direction = 'down'

restart_button = Button(window, text="Restart", command=restart_game, font=('consolas', 20))
restart_button.place(x=0, y=0)

game_over = False


label = Label(window, text="Score:{}".format(score), font=('consoles', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

#myButton = Button(window, text="Do you want to continue?", command=click)
#myButton.pack()

window_width = window.winfo_height()
window_height = window.winfo_width()
screen_width = window.winfo_screenwidth()
screen_height =window.winfo_screenheight()

x = int((screen_width/5) - (window_width/5))
y = int((screen_height/5) - (window_height/5))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<space>', restart_game)

snake =Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
