import pygame
import sys

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.Font(None, 30)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle GUI with Skills")


class Skill:
    def __init__(self, name, damage, mp_cost):
        self.name = name
        self.damage = damage
        self.mp_cost = mp_cost


class Character:
    def __init__(self, name, x, y):
        self.name = name
        self.health = 100
        self.mp = 50  # Max MP
        self.x = x
        self.y = y
        self.skills = []


# Initialize characters with different skills
left_char = Character("Warrior", 50, 200)
left_char.skills = [
    Skill("Slash", 15, 0),
    Skill("Heal", -20, 15),
    Skill("Defend", 0, 5)
]

right_char = Character("Mage", 600, 200)
right_char.skills = [
    Skill("Fireball", 25, 10),
    Skill("Ice Nova", 20, 12),
    Skill("Mana Shield", -10, 20)  # Heals MP
]

current_turn = 'left'
clock = pygame.time.Clock()


def draw_health_bar(screen, x, y, value, max_value, color):
    bar_length = 100
    bar_height = 10
    fill = (value / max_value) * bar_length
    outline_rect = pygame.Rect(x, y, bar_length, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(screen, color, fill_rect)
    pygame.draw.rect(screen, BLACK, outline_rect, 2)


def draw_text(text, x, y):
    surface = FONT.render(text, True, BLACK)
    screen.blit(surface, (x, y))


def draw_skill_menu(char_skills, x, y):
    for idx, skill in enumerate(char_skills):
        text = f"{idx + 1}. {skill.name} (MP:{skill.mp_cost})"
        draw_text(text, x, y + idx * 30)


def main():
    running = True
    winner = None
    global current_turn
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                current_char = left_char if current_turn == 'left' else right_char
                opponent = right_char if current_turn == 'left' else left_char

                # Handle skill selection
                for i in range(len(current_char.skills)):
                    key = getattr(pygame, f'K_{i + 1}', None)
                    if event.key == key:
                        skill = current_char.skills[i]
                        if current_char.mp >= skill.mp_cost:
                            # Apply skill effect
                            if skill.damage > 0:
                                opponent.health -= skill.damage
                            else:
                                current_char.health += -skill.damage  # Heal
                                if current_char.health > 100:
                                    current_char.health = 100

                            current_char.mp -= skill.mp_cost
                            # Switch turn
                            current_turn = 'right' if current_turn == 'left' else 'left'
                            break  # Exit after selection

        # Cap values
        left_char.health = max(0, left_char.health)
        right_char.health = max(0, right_char.health)
        left_char.mp = max(0, left_char.mp)
        right_char.mp = max(0, right_char.mp)

        # Check victory conditions
        if left_char.health <= 0 and right_char.health <= 0:
            winner = "TIE!"
        elif left_char.health <= 0:
            winner = "Mage Wins!"
        elif right_char.health <= 0:
            winner = "Warrior Wins!"

        if winner:
            running = False

        # Draw everything
        screen.fill(WHITE)

        # Draw characters
        pygame.draw.rect(screen, BLACK, (left_char.x, left_char.y, 50, 50))
        pygame.draw.rect(screen, BLACK, (right_char.x, right_char.y, 50, 50))

        # Draw health bars
        draw_health_bar(screen, left_char.x, left_char.y - 40, left_char.health, 100, GREEN)
        draw_health_bar(screen, right_char.x, right_char.y - 40, right_char.health, 100, GREEN)

        # Draw MP bars
        draw_health_bar(screen, left_char.x, left_char.y - 60, left_char.mp, 50, BLUE)
        draw_health_bar(screen, right_char.x, right_char.y - 60, right_char.mp, 50, BLUE)

        # Draw skill menu
        if current_turn == 'left':
            draw_skill_menu(left_char.skills, 50, 300)
        else:
            draw_skill_menu(right_char.skills, 500, 300)

        # Draw text labels
        draw_text(f"{left_char.name}", left_char.x, left_char.y + 60)
        draw_text(f"{right_char.name}", right_char.x, right_char.y + 60)
        draw_text(f"HP: {left_char.health}", left_char.x, left_char.y - 10)
        draw_text(f"HP: {right_char.health}", right_char.x, right_char.y - 10)
        draw_text(f"MP: {left_char.mp}", left_char.x, left_char.y - 30)
        draw_text(f"MP: {right_char.mp}", right_char.x, right_char.y - 30)

        pygame.display.flip()
        clock.tick(30)

    # Show winner message
    screen.fill(WHITE)
    text = FONT.render(winner, True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
