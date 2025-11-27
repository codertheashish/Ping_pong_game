import pygame
import sys
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Color & Score Sync")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 120)
YELLOW = (255, 220, 0)
ORANGE = (255, 130, 40)
RED = (255, 70, 70)
PURPLE = (200, 60, 255)
BLUE = (50, 150, 255)
BLACK = (0, 0, 0)

# Ball color sequence list
ball_colors = [WHITE, GREEN, YELLOW, ORANGE, RED, PURPLE]

# ✅ GLOBAL current ball + score color
current_color = WHITE

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 32, bold=True)

# Paddle settings
paddle_width = 15
paddle_height = 90

player_x = 20
player_y = HEIGHT // 2 - paddle_height // 2

ai_x = WIDTH - 20 - paddle_width
ai_y = HEIGHT // 2 - paddle_height // 2

paddle_speed = 6

# Ball settings
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_radius = 12
ball_dx = 4
ball_dy = 4

player_score = 0
ai_score = 0
player_hits = 0  # ✅ Count only player returns


def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy, player_hits, current_color
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = random.choice([-4, 4])
    ball_dy = random.choice([-4, 4])
    player_hits = 0
    current_color = WHITE  # ✅ reset color for ball & score


def draw_objects():
    screen.fill(BLACK)

    pygame.draw.rect(screen, BLUE, (player_x, player_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, RED, (ai_x, ai_y, paddle_width, paddle_height))

    # ✅ Ball uses synced color
    pygame.draw.circle(screen, current_color, (ball_x, ball_y), ball_radius)

    # ✅ Score uses SAME color
    score_text = font.render(f"{player_score} : {ai_score}", True, current_color)
    screen.blit(score_text, (WIDTH//2 - 45, 20))


def game_over_screen():
    while True:
        screen.fill(BLACK)

        over = font.render("GAME OVER!", True, RED)
        restart = font.render("Press R to Restart", True, BLUE)
        exit_text = font.render("Press ESC to Exit", True, WHITE)

        screen.blit(over, (WIDTH//2 - 120, 180))
        screen.blit(restart, (WIDTH//2 - 160, 240))
        screen.blit(exit_text, (WIDTH//2 - 150, 290))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


# ==============================
#          MAIN LOOP
# ==============================
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player_y > 0:
        player_y -= paddle_speed
    if keys[pygame.K_DOWN] and player_y < HEIGHT - paddle_height:
        player_y += paddle_speed

    # AI movement
    if ai_y + paddle_height / 2 < ball_y:
        ai_y += paddle_speed - 2
    elif ai_y + paddle_height / 2 > ball_y:
        ai_y -= paddle_speed - 2

    # Move ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Bounce on top/bottom
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
        ball_dy *= -1

    # ✅ PLAYER paddle collision (color change + slow speed increase)
    if (player_x < ball_x - ball_radius < player_x + paddle_width and
        player_y < ball_y < player_y + paddle_height):
        ball_dx *= -1.05     # ✅ smaller speed increase
        ball_dy *= 1.03
        player_hits += 1
        current_color = ball_colors[player_hits % len(ball_colors)]  # ✅ update shared color

    # ✅ AI paddle collision (NO color change)
    if (ai_x < ball_x + ball_radius < ai_x + paddle_width and
        ai_y < ball_y < ai_y + paddle_height):
        ball_dx *= -1.05
        ball_dy *= 1.03

    # Scoring
    if ball_x < 0:
        ai_score += 1
        reset_ball()

    if ball_x > WIDTH:
        player_score += 1
        reset_ball()

    # Game end
    if player_score == 7 or ai_score == 7:
        game_over_screen()
        player_score = 0
        ai_score = 0
        reset_ball()

    draw_objects()
    pygame.display.update()
    clock.tick(60)
