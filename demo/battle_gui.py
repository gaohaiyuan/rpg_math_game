import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 36)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle GUI")

# Character data
class Character:
    def __init__(self, name, x, y):
        self.name = name
        self.health = 100
        self.x = x
        self.y = y

left_char = Character("Warrior", 50, 200)
right_char = Character("Mage", 600, 200)

ATTACK_DAMAGE = 20
clock = pygame.time.Clock()

def draw_health_bar(screen, x, y, health, max_health):
    """Draw health bar for a character."""
    bar_length = 100
    bar_height = 10
    fill = (health / max_health) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(screen, GREEN, fill_rect)
    pygame.draw.rect(screen, RED, outline_rect, 2)

def draw_text(text, x, y):
    """Helper function to draw text."""
    text_surface = FONT.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))

def main():
    running = True
    winner = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    right_char.health -= ATTACK_DAMAGE
                if event.key == pygame.K_d:
                    left_char.health -= ATTACK_DAMAGE

        # Cap health between 0 and 100
        left_char.health = max(0, left_char.health)
        right_char.health = max(0, right_char.health)

        # Check for victory conditions
        if left_char.health <= 0 and right_char.health <= 0:
            winner = "TIE!"
            running = False
        elif left_char.health <= 0:
            winner = f"{right_char.name} WINS!"
            running = False
        elif right_char.health <= 0:
            winner = f"{left_char.name} WINS!"
            running = False

        # Draw everything
        screen.fill(WHITE)

        # Draw characters (rectangles)
        pygame.draw.rect(screen, BLACK, (left_char.x, left_char.y, 50, 50))
        pygame.draw.rect(screen, BLACK, (right_char.x, right_char.y, 50, 50))

        # Draw health bars
        draw_health_bar(screen, left_char.x, left_char.y - 40, left_char.health, 100)
        draw_health_bar(screen, right_char.x, right_char.y - 40, right_char.health, 100)

        # Draw text labels
        draw_text(f"{left_char.name} - {left_char.health} HP", left_char.x, left_char.y + 60)
        draw_text(f"{right_char.name} - {right_char.health} HP", right_char.x, right_char.y + 60)

        pygame.display.flip()
        clock.tick(30)

    # Show winner message
    if winner:
        screen.fill(WHITE)
        text = FONT.render(winner, True, BLACK)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(2000)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
