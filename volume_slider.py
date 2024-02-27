import pygame
import sys

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Slider:
    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.length = length
        self.slider_width = 10
        self.slider_pos = x
        self.clicked = False
# draws the slider
    def draw(self, screen):
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x + self.length, self.y), 2)
        pygame.draw.rect(screen, RED, (self.slider_pos - self.slider_width // 2, self.y - self.slider_width // 2, self.slider_width, self.slider_width))
# adjusting the slider to the mouse position
# slider position
    def update(self, mouse_pos):
        if self.clicked:
            self.slider_pos = mouse_pos[0]
            if self.slider_pos < self.x:
                self.slider_pos = self.x
            elif self.slider_pos > self.x + self.length:
                self.slider_pos = self.x + self.length

    def set_clicked(self, clicked):
        self.clicked = clicked
# finds the value of slider position
    def get_value(self):
        return (self.slider_pos - self.x) / self.length
# black screen or window
def main():
    pygame.init()
    screen_width, screen_height = 400, 200
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Volume Slider")
    clock = pygame.time.Clock()

    slider = Slider(50, 100, 300)
    volume = 0.5  # Initial volume- middle position
     

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            # Check if the event is a QUIT event (user closing the window)
            if event.type == pygame.QUIT:
                running = False

            # Check if the event is a MOUSEBUTTONDOWN event
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the left mouse button is pressed
                if event.button == 1:
                    # Get the current mouse position
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if the mouse position is within the bounds of the slider button,
                    # and if so, set the slider to be clicked
                    if slider.slider_pos - slider.slider_width // 2 <= mouse_pos[0] <= slider.slider_pos + slider.slider_width // 2 and slider.y - slider.slider_width // 2 <= mouse_pos[1] <= slider.y + slider.slider_width // 2:
                        slider.set_clicked(True)

            # Check if the event is a MOUSEBUTTONUP event
            elif event.type == pygame.MOUSEBUTTONUP:
                # Check if the left mouse button is released
                if event.button == 1:
                    # Set the slider to be not clicked
                    slider.set_clicked(False)

            # Check if the event is a MOUSEMOTION event
            elif event.type == pygame.MOUSEMOTION:
                # Check if the slider is currently clicked
                if slider.clicked:
                    # Get the current mouse position
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Update the slider position based on the mouse movement
                    slider.update(mouse_pos)
                    
                    # Update the volume based on the new slider position
                    volume = slider.get_value()

        # Draw the slider on the screen, update the display, and limit the frame rate to 120 frames per second
        slider.draw(screen)
        pygame.display.flip()
        clock.tick(120)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
