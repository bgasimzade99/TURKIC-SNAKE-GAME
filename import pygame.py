import pygame
import cv2  # For handling the MP4 video
import random

# Initialize Pygame
pygame.init()

# Game Window Dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Create Window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock for controlling speed
clock = pygame.time.Clock()

# Difficulty Modes
DIFFICULTY = {
    "Easy": 10,
    "Medium": 15,
    "Hard": 20
}

# Load Music
pygame.mixer.init()
lobby_sound = pygame.mixer.Sound("turk.mp3")  # Lobby music
move_sound = pygame.mixer.Sound("music_move.mp3")  # Snake move sound
food_sound = pygame.mixer.Sound("music_food.mp3")  # Eating food sound
gameover_sound = pygame.mixer.Sound("music_gameover.mp3")  # Game Over sound

# Best Score Tracker
best_score = 0

# Load and resize the logos
logo = pygame.image.load("rtu1.png")  # Main logo
logo_width, logo_height = 80, 80
logo = pygame.transform.scale(logo, (logo_width, logo_height))

additional_logo = pygame.image.load("turkic1.png")  # Additional logo
additional_logo = pygame.transform.scale(additional_logo, (150, 150))


# Generate Obstacles (Walls)
def generate_obstacles(num_obstacles):
    obstacles = []
    for _ in range(num_obstacles):
        x = random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE
        y = random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE
        obstacles.append([x, y])
    return obstacles


# Main Game Function
def start_game(speed):
    global best_score

    while True:  # Allow restarting by looping
        snake_pos = [[100, 100], [90, 100], [80, 100]]  # Snake initial size
        food_pos = [random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
                    random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE]
        obstacles = generate_obstacles(10)  # Generate 10 obstacles
        direction = 'RIGHT'
        change_to = direction
        score = 0

        running = True
        while running:
            screen.fill(BLACK)

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != 'DOWN':
                        change_to = 'UP'
                    elif event.key == pygame.K_DOWN and direction != 'UP':
                        change_to = 'DOWN'
                    elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                        change_to = 'LEFT'
                    elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                        change_to = 'RIGHT'

            direction = change_to

            # Update Snake Position
            if direction == 'UP':
                snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] - CELL_SIZE])
            elif direction == 'DOWN':
                snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] + CELL_SIZE])
            elif direction == 'LEFT':
                snake_pos.insert(0, [snake_pos[0][0] - CELL_SIZE, snake_pos[0][1]])
            elif direction == 'RIGHT':
                snake_pos.insert(0, [snake_pos[0][0] + CELL_SIZE, snake_pos[0][1]])
                move_sound.play()

            # Check if Snake Ate Food
            if snake_pos[0] == food_pos:
                score += 1
                food_sound.play()
                food_pos = [random.randrange(1, WIDTH // CELL_SIZE) * CELL_SIZE,
                            random.randrange(1, HEIGHT // CELL_SIZE) * CELL_SIZE]
            else:
                snake_pos.pop()

            # Check Collision with Walls, Obstacles, or Itself
            if (snake_pos[0][0] < 0 or snake_pos[0][0] >= WIDTH or
                    snake_pos[0][1] < 0 or snake_pos[0][1] >= HEIGHT or
                    snake_pos[0] in snake_pos[1:] or
                    snake_pos[0] in obstacles):
                running = False
                gameover_sound.play()
                restart = game_over(score)
                if restart == "restart":
                    continue  # Restart the game
                elif restart == "menu":
                    return  # Return to the main menu
                else:
                    return  # Quit the game

            # Draw Obstacles
            for obstacle in obstacles:
                pygame.draw.rect(screen, WHITE, pygame.Rect(obstacle[0], obstacle[1], CELL_SIZE, CELL_SIZE))

            # Draw Snake and Food
            pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], CELL_SIZE, CELL_SIZE))
            for pos in snake_pos:
                pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

            # Display Score
            show_score(score)

            pygame.display.flip()
            clock.tick(speed)


# Display Score
def show_score(score):
    font = pygame.font.Font(None, 30)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, [10, 10])


# Game Over Screen with Restart/Quit/Menu Option
def game_over(score):
    global best_score
    if score > best_score:
        best_score = score

    screen.fill(BLACK)
    font = pygame.font.Font(None, 40)

    # Game Over text
    game_over_text = font.render(f"Game Over! Score: {score}", True, RED)
    screen.blit(game_over_text, [WIDTH // 4, HEIGHT // 3])

    # Best Score text
    best_score_text = font.render(f"Best Score: {best_score}", True, WHITE)
    screen.blit(best_score_text, [WIDTH // 4, HEIGHT // 3 + 50])

    # Restart, Quit, or Main Menu text
    restart_text = font.render("Press R to Restart, Q to Quit, or M for Menu", True, WHITE)
    screen.blit(restart_text, [WIDTH // 4 - 40, HEIGHT // 3 + 100])

    # Add logos
    screen.blit(logo, (10, HEIGHT - logo_height - 10))
    screen.blit(additional_logo, (WIDTH - 150, HEIGHT - 130))
    # Add "Created by TURKIC GROUP" text
    font_small = pygame.font.Font(None, 30)
    credit_text = font_small.render("Created by TURKIC GROUP", True, WHITE)
    screen.blit(credit_text, (logo_width + 20, HEIGHT - 30))

    pygame.display.flip()

    # Handle Restart, Quit, or Menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    return "restart"
                elif event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    exit()
                elif event.key == pygame.K_m:  # Return to Menu
                    return "menu"


# Difficulty Selection Menu
def menu():
    while True:
        # Play Lobby Music
        lobby_sound.play(-1)

        cap = cv2.VideoCapture("snak2.mp4")
        if not cap.isOpened():
            print("Error: Cannot open video file.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            screen.fill(BLACK)

            # Render Video
            frame = cv2.resize(frame, (300, 200))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            screen.blit(frame_surface, (250, 150))

            # Text and Design
            font = pygame.font.Font(None, 60)
            welcome_text = font.render("Welcome to the SNAKE GAME!", True, RED)
            screen.blit(welcome_text, (WIDTH // 6, HEIGHT // 9))

            small_font = pygame.font.Font(None, 30)
            text = small_font.render("Choose Difficulty: E (Easy) / M (Medium) / H (Hard)", True, WHITE)
            screen.blit(text, (200, 420))

            # Add logos
            screen.blit(logo, (10, HEIGHT - 90))
            credit_text = small_font.render("Created by TURKIC GROUP", True, WHITE)
            screen.blit(credit_text, (100, HEIGHT - 50))  # Make sure the text is positioned correctly
            screen.blit(additional_logo, (WIDTH - 160, HEIGHT - 160))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        lobby_sound.stop()
                        cap.release()
                        start_game(DIFFICULTY["Easy"])
                    elif event.key == pygame.K_m:
                        lobby_sound.stop()
                        cap.release()
                        start_game(DIFFICULTY["Medium"])
                    elif event.key == pygame.K_h:
                        lobby_sound.stop()
                        cap.release()
                        start_game(DIFFICULTY["Hard"])


# Run Game Menu
menu()
pygame.quit()
