%pip install ipycanvas ipywidgets
import ipywidgets as widgets
from ipycanvas import Canvas
import random
import asyncio


from ipycanvas import Canvas
import ipywidgets as widgets
import random
import asyncio

# Game dimensions
WIDTH, HEIGHT = 800, 600

# Colors
BLACK = "#000000"
WHITE = "#FFFFFF"
YELLOW = "#FFFF00"

# Player spaceship
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# Cosmic Coins
coin_size = 20
coins = []
for _ in range(5):
    coin_x = random.randint(0, WIDTH - coin_size)
    coin_y = random.randint(-100, -coin_size)
    coins.append([coin_x, coin_y])

# Game variables
score = 0

# Create canvas
canvas = Canvas(width=WIDTH, height=HEIGHT)
canvas.layout.width = f"{WIDTH}px"
canvas.layout.height = f"{HEIGHT}px"

# Create score label
score_label = widgets.Label(value="Cosmic Coins: 0")

# Create game container
game_container = widgets.VBox([canvas, score_label])

def draw_player():
    canvas.fill_style = WHITE
    canvas.fill_rect(player_x, player_y, player_width, player_height)

def draw_coins():
    canvas.fill_style = YELLOW
    for coin in coins:
        canvas.fill_circle(coin[0] + coin_size // 2, coin[1] + coin_size // 2, coin_size // 2)

def update_coins():
    global score
    for coin in coins:
        coin[1] += 2  # Move coin down

        # Check collision
        if player_y < coin[1] + coin_size and player_y + player_height > coin[1]:
            if player_x < coin[0] + coin_size and player_x + player_width > coin[0]:
                score += 1
                score_label.value = f"Cosmic Coins: {score}"
                coin[1] = random.randint(-100, -coin_size)
                coin[0] = random.randint(0, WIDTH - coin_size)

        # Reset coin if it goes off screen
        if coin[1] > HEIGHT:
            coin[1] = random.randint(-100, -coin_size)
            coin[0] = random.randint(0, WIDTH - coin_size)

async def game_loop():
    global player_x
    while True:
        canvas.fill_style = BLACK
        canvas.fill_rect(0, 0, WIDTH, HEIGHT)

        # Player movement (simplified for demo)
        player_x += random.randint(-player_speed, player_speed)
        player_x = max(0, min(WIDTH - player_width, player_x))

        draw_player()
        update_coins()
        draw_coins()

        canvas.flush()
        await asyncio.sleep(0.03)  # Approximately 30 FPS

# Display the game
display(game_container)

# Start the game loop
asyncio.ensure_future(game_loop())
