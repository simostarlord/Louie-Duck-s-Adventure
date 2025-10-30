import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Louie Duck's Adventure")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# Colors
BLUE = (135, 206, 250)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)

# Load images
duck_img = pygame.image.load("duck.png")
duck_img = pygame.transform.scale(duck_img, (60, 60))

pad_img = pygame.image.load("lily_pad.png")
pad_img = pygame.transform.scale(pad_img, (100, 40))

# Game variables
def reset_game():
    global duck, y_velocity, is_jumping, on_tile, game_started, game_over, score, tiles
    duck = pygame.Rect(150, HEIGHT - 200, 60, 60)
    y_velocity = 0
    is_jumping = False
    on_tile = True
    game_started = False
    game_over = False
    score = 0

    tiles = []
    for i in range(5):
        x = 150 + i * tile_gap
        y = HEIGHT - 150
        tiles.append(pygame.Rect(x, y, tile_width, tile_height))

# Lily pad setup
tile_width = 100
tile_height = 20
tile_gap = 200
tile_speed = 5

reset_game()

def draw_tiles():
    for tile in tiles:
        screen.blit(pad_img, tile)

def check_collision():
    for tile in tiles:
        if duck.colliderect(tile) and y_velocity >= 0 and abs(duck.bottom - tile.top) < 20:
            return tile
    return None

def draw_button(rect, text):
    pygame.draw.rect(screen, GREEN, rect)
    pygame.draw.rect(screen, BLACK, rect, 3)
    txt = font.render(text, True, BLACK)
    screen.blit(txt, (rect.x + 20, rect.y + 10))

# Game loop
while True:
    screen.fill(BLUE)
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
            if not game_started:
                game_started = True
            if on_tile and not is_jumping:
                y_velocity = -18
                is_jumping = True
                on_tile = False

    if game_started and not game_over:
        # Move tiles
        for tile in tiles:
            tile.x -= tile_speed

        # Remove off-screen tiles
        tiles = [tile for tile in tiles if tile.right > 0]

        # Add new tiles
        if tiles[-1].x < WIDTH - tile_gap:
            new_x = tiles[-1].x + tile_gap
            tiles.append(pygame.Rect(new_x, HEIGHT - 150, tile_width, tile_height))

        # Gravity
        y_velocity += 1
        duck.y += y_velocity

        # Landing check
        landed_tile = check_collision()
        if landed_tile:
            duck.bottom = landed_tile.top
            y_velocity = 0
            is_jumping = False
            if not on_tile:
                score += 1
                on_tile = True
        else:
            on_tile = False

        # Fall check
        if duck.top > HEIGHT:
            game_over = True

    # Draw everything
    draw_tiles()
    screen.blit(duck_img, duck)

    if not game_started:
        screen.blit(font.render("Click to Start", True, BLACK), (WIDTH // 2 - 140, HEIGHT // 2))
    elif game_over:
        screen.blit(font.render("Game Over NOOOOOO ", True, BLACK), (WIDTH // 2 - 100, HEIGHT // 2 - 60))
        restart_btn = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 60)
        draw_button(restart_btn, "Restart")
        if restart_btn.collidepoint(mouse) and click[0]:
            reset_game()
            pygame.time.wait(200)
    else:
        screen.blit(font.render(f"Score: {score}", True, BLACK), (20, 20))

    pygame.display.flip()
    clock.tick(60)
