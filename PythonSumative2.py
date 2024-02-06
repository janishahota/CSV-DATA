import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Game")

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)  # Larger font for the congratulations message

# Load and scale down the person sprite
person_img = pygame.image.load("/Users/hota/Downloads/Person.png")  # Replace with the path to your person sprite
person_img = pygame.transform.scale(person_img, (50, 50))
person_rect = person_img.get_rect()
person_rect.bottom = HEIGHT - 10
person_speed = 1

# Load and scale down the finish line sprite
finish_line_img = pygame.image.load("/Users/hota/Downloads/finish.png")  # Replace with the path to your finish line sprite
finish_line_img = pygame.transform.scale(finish_line_img, (50, 50))
finish_line_rect = finish_line_img.get_rect()
finish_line_rect.x = WIDTH - 10 - finish_line_rect.width
finish_line_rect.bottom = HEIGHT - 10

# Math game variables
score = 0
question_count = 0
current_question = None
timer = 7 * 60  # 7 seconds in frames (assuming 60 frames per second)
option_rects = []  # Initialize option_rects list


# Function to generate a random math question
def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    operator = random.choice(["+", "-", "*"])
    question = f"{num1} {operator} {num2}"
    answer = eval(question)
    return question, answer


    # Function to display text on the screen
def display_text(text, x, y, font_used=font, color=BLACK):
    text_surface = font_used.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)
    return text_rect


# Main game loop
clock = pygame.time.Clock()
running = True
celebration_message = None

while running:
    screen.fill(WHITE)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

            # Check for mouse click events
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_question is not None:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, option_rect in enumerate(option_rects):
                    if option_rect.collidepoint(mouse_x, mouse_y):
                        if i < len(options):  # Check if i is a valid index in options list
                            selected_option = i
                            if options[selected_option] == current_question[1]:
                                score += 1
                                person_rect.x +=75+ person_speed
                                pygame.mixer.music.load(
                                        "/Users/hota/Downloads/Correct Answer sound effect.mp3")  # Replace with the path to your happy sound file
                                pygame.mixer.music.play(0)
                            else:
                                person_rect.x -=75- person_speed
                                score-=1
                                pygame.mixer.music.load(
                                        "/Users/hota/Downloads/Wrong Answer sound effect.mp3")  # Replace with the path to your happy sound file
                                pygame.mixer.music.play(0)

                            question_count += 1
                            current_question = None
                            timer = 7 * 60  # Reset the timer

    # Display person sprite
    screen.blit(person_img, person_rect)

    # Display finish line sprite
    screen.blit(finish_line_img, finish_line_rect)

    # Display score and question count
    display_text(f"Score: {score}", 10, 10)
    display_text(f"Questions Asked: {question_count}", 10, 50)

    # Generate and display a random math question
    if current_question is None:
        current_question = generate_question()
        options = [current_question[1], current_question[1] + random.randint(1, 5),
                       current_question[1] - random.randint(1, 5)]
        random.shuffle(options)
        option_rects = []  # Reset option_rects

    display_text(current_question[0], WIDTH // 2 - 50, HEIGHT // 2 - 50)

    # Display three answer options
    for i, option in enumerate(options):
        option_text = f"{chr(65 + i)}. {option}"
        option_rect = display_text(option_text, WIDTH // 2 - 50, HEIGHT // 2 + i * 30)
        option_rects.append(option_rect)

    # Display the timer
    display_text(f"Time Left: {timer // 60} seconds", WIDTH - 250, 10)

    # Update the display
    pygame.display.flip()

    # Update the timer
    if current_question is not None:
        timer -= 1
        if timer == 0:
            question_count += 1
            current_question = None
            timer = 7 * 60  # Reset the timer

    # Check if the person reached the finish line
    if person_rect.x >= finish_line_rect.x:
        if celebration_message is None:
            celebration_message = "Hooray! You reached the finish line!"
            pygame.mixer.music.load("/Users/hota/Downloads/tomp3.cc - Celebration Sound Effect.mp3")  # Replace with the path to your happy sound file
            pygame.mixer.music.play(0)

    # Display celebration message with larger font and colors
    if celebration_message is not None:
        big_font = pygame.font.Font(None, 60)
        big_font_surface = big_font.render(celebration_message, True, RED)
        big_font_rect = big_font_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(big_font_surface, big_font_rect)
        pygame.display.flip()  # Update the display to ensure the message is rendered

        # Check if the person reached the finish line
    if person_rect.x >= finish_line_rect.x and celebration_message is not None:
        pygame.time.delay(5000)  # Display celebration for 5 seconds
        running = False

    clock.tick(60)  # Cap the frame rate to 60 frames per second


pygame.quit()
sys.exit()
