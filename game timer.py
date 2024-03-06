import pygame
import sys

# Initialise Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Timer")

# Fonts
font = pygame.font.Font("fonts/Crang.ttf", 36)  
# Load the font with a specific size
timer_font = pygame.font.Font("fonts/Crang.ttf", 72)  
# Font for the timer

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Function to display input box for entering timer value
def display_input_box():
    input_box_minutes = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 25, 100, 50)
    input_box_seconds = pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2 - 25, 100, 50)
    input_text_minutes = ""
    input_text_seconds = ""
    active = True

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    try:
                        minutes = int(input_text_minutes)
                        seconds = int(input_text_seconds)
                        return minutes, seconds
                    except ValueError:
                        print("Invalid input! Please enter valid integers.")
                        return None, None
                elif event.key == pygame.K_BACKSPACE:
                    if input_box_minutes.collidepoint(pygame.mouse.get_pos()):
                        input_text_minutes = input_text_minutes[:-1]
                    elif input_box_seconds.collidepoint(pygame.mouse.get_pos()):
                        input_text_seconds = input_text_seconds[:-1]
                else:
                    if input_box_minutes.collidepoint(pygame.mouse.get_pos()):
                        input_text_minutes += event.unicode 
                    elif input_box_seconds.collidepoint(pygame.mouse.get_pos()):
                        input_text_seconds += event.unicode 

        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, input_box_minutes, 2)
        pygame.draw.rect(screen, BLACK, input_box_seconds, 2)
        font_surface_minutes = font.render("Minutes:", True, BLACK)
        font_surface_seconds = font.render("Seconds:", True, BLACK)
        screen.blit(font_surface_minutes, (WIDTH // 2 - 200, HEIGHT // 2 - 100))
        screen.blit(font_surface_seconds, (WIDTH // 2 + 0, HEIGHT // 2 - 100))
        text_surface_minutes = font.render(input_text_minutes, True, BLACK)
        text_surface_seconds = font.render(input_text_seconds, True, BLACK)
        screen.blit(text_surface_minutes, (input_box_minutes.x + 5, input_box_minutes.y + 5))
        screen.blit(text_surface_seconds, (input_box_seconds.x + 5, input_box_seconds.y + 5))
        pygame.display.flip()

# Function to run the game
# Function to run the game
# Function to run the game
def run_game(minutes, seconds):
    total_seconds = minutes * 60 + seconds
    clock = pygame.time.Clock()
    running = True

    while running and total_seconds > 0:  # Stop the timer when it reaches zero or below
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if running:  # Only update the timer if the game is still running
            # Update timer
            total_seconds -= clock.get_rawtime() / 1000  # Subtract time since last frame
            clock.tick()  # Update the clock

            # Calculate minutes and seconds
            minutes = max(total_seconds // 60, 0)  # Ensure minutes are not negative
            seconds = max(total_seconds % 60, 0)  # Ensure seconds are not negative

            # Draw timer using the custom font
            timer_text = timer_font.render(f"{int(minutes):02d}:{int(seconds):02d}", True, BLACK)
            screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, HEIGHT // 2 - timer_text.get_height() // 2))

        pygame.display.flip()

    # If timer reaches zero, end the game
    if total_seconds <= 0:
        print("Game Over!")

    # Quit Pygame
    pygame.quit()
    sys.exit()


# Main function
def main():
    minutes, seconds = display_input_box()
    if minutes is not None and seconds is not None:
        run_game(minutes, seconds)
    else:
        main()

if __name__ == "__main__":
    main()
