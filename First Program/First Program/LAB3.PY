import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SHOOTER_RADIUS = 20
CIRCLE_RADIUS = 15
PROJECTILE_RADIUS = 5
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FPS = 60

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shoot The Circles!")

# Game variables
shooter_x = SCREEN_WIDTH // 2
shooter_y = SCREEN_HEIGHT - SHOOTER_RADIUS
circles = []
projectiles = []
score = 0
missed = 0
misfires = 0
game_over = False
paused = False

# Create shooter
def draw_shooter(x, y):
    pygame.draw.circle(screen, GREEN, (x, y), SHOOTER_RADIUS)

# Create falling circles
def create_circle():
    x = random.randint(CIRCLE_RADIUS, SCREEN_WIDTH - CIRCLE_RADIUS)
    y = CIRCLE_RADIUS
    return {'x': x, 'y': y}

def draw_circle(x, y):
    pygame.draw.circle(screen, RED, (x, y), CIRCLE_RADIUS)

# Create projectile
def draw_projectile(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), PROJECTILE_RADIUS)

def main():
    global shooter_x, shooter_y, circles, projectiles, score, missed, misfires, game_over, paused

    clock = pygame.time.Clock()

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    shooter_x -= 10
                elif event.key == pygame.K_d:
                    shooter_x += 10
                elif event.key == pygame.K_SPACE:
                    if not paused and not game_over:
                        projectiles.append({'x': shooter_x, 'y': shooter_y})

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                shooter_x -= 5
            if keys[pygame.K_d]:
                shooter_x += 5

            # Game logic
            if random.randint(0, 20) == 0:  # Randomly create circles
                circles.append(create_circle())

            for circle in circles:
                circle['y'] += 5
                if circle['y'] >= SCREEN_HEIGHT - SHOOTER_RADIUS:
                    missed += 1
                    circles.remove(circle)
                    if missed >= 3:
                        game_over = True

            for projectile in projectiles:
                projectile['y'] -= 10
                if projectile['y'] < 0:
                    projectiles.remove(projectile)
                    misfires += 1
                    if misfires >= 3:
                        game_over = True

            # Collision detection
            for circle in circles:
                for projectile in projectiles:
                    dist = ((circle['x'] - projectile['x'])**2 + (circle['y'] - projectile['y'])**2)**0.5
                    if dist < CIRCLE_RADIUS + PROJECTILE_RADIUS:
                        score += 1
                        circles.remove(circle)
                        projectiles.remove(projectile)
                        break

            for circle in circles:
                if ((shooter_x - circle['x'])**2 + (shooter_y - circle['y'])**2)**0.5 < SHOOTER_RADIUS + CIRCLE_RADIUS:
                    game_over = True

            # Drawing
            screen.fill((0, 0, 0))
            draw_shooter(shooter_x, shooter_y)
            for circle in circles:
                draw_circle(circle['x'], circle['y'])
            for projectile in projectiles:
                draw_projectile(projectile['x'], projectile['y'])

            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()
