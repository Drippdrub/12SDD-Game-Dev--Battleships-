import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hover Button Example")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.Font(None, 36)

class Button:
    def __init__(self, x, y, width, height, text, description):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.description = description
        self.hovered = False
        self.hover_timer = 0

    def draw(self):
        # Change button color if hovered
        color = GRAY if not self.hovered else WHITE
        pygame.draw.rect(screen, color, self.rect)
        
        # Render text on button
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
        
    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.hovered = True
            if self.hover_timer == 0:
                self.hover_timer = pygame.time.get_ticks()
        else:
            self.hovered = False
            self.hover_timer = 0

    def show_description(self):
        if self.hovered:
            current_time = pygame.time.get_ticks()
            if current_time - self.hover_timer >= 2000:  # 2 seconds delay
                desc_surf = font.render(self.description, True, BLACK)
                desc_rect = desc_surf.get_rect(x=self.rect.x, y=self.rect.y + self.rect.height + 10)
                pygame.draw.rect(screen, GRAY, desc_rect)
                screen.blit(desc_surf, desc_rect)

# Create a button
btn = Button(300, 200, 200, 50, "black people", "hate being slaves")

# Main loop
running = True
while running:
    screen.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update button
    btn.update(mouse_pos)
    
    # Draw button
    btn.draw()
    btn.show_description()
    
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
