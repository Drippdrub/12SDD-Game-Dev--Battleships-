import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGRAY = (50, 50, 50)
LIGHTGRAY = (175, 175, 175)

class Slider:
    def __init__(self, x, y, length, *args):
        self.x = x
        self.y = y
        self.length = length
        self.slider_width = 40
        try:
            self.slider_pos = x+length*args[0]
            self.default = x+length*args[0]
        except:
            self.slider_pos = x+length
            self.default = 1
        self.clicked = False

    def draw(self, screen):
        size_diff = self.slider_width/5
        pygame.draw.circle(screen, LIGHTGRAY, (self.x, self.y), self.slider_width/2-size_diff)
        pygame.draw.circle(screen, LIGHTGRAY, (self.x+self.length, self.y), self.slider_width/2-size_diff)
        pygame.draw.rect(screen, LIGHTGRAY, (self.x, self.y - self.slider_width/2+size_diff, self.length, self.slider_width-size_diff*2))
        # pygame.draw.line(screen, WHITE, (self.x-1, self.y-1), (self.x + self.length-1, self.y-1), 2)
        pygame.draw.circle(screen, DARKGRAY, (self.slider_pos, self.y), self.slider_width/2)
        value = self.default
        if pygame.mouse.get_pressed()[0] == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.slider_pos - self.slider_width // 2 <= mouse_pos[0] <= self.slider_pos + self.slider_width // 2 and self.y - self.slider_width // 2 <= mouse_pos[1] <= self.y + self.slider_width // 2:
                self.set_clicked(True)
        elif pygame.mouse.get_pressed()[0] == 0:
            self.set_clicked(False)

        if self.clicked:
            mouse_pos = pygame.mouse.get_pos()
            self.update(mouse_pos)
        value = self.get_value()
        return value

    def update(self, mouse_pos):
        if self.clicked:
            self.slider_pos = mouse_pos[0]
            if self.slider_pos < self.x:
                self.slider_pos = self.x
            elif self.slider_pos > self.x + self.length:
                self.slider_pos = self.x + self.length

    def set_clicked(self, clicked):
        self.clicked = clicked

    def get_value(self):
        return (self.slider_pos - self.x) / self.length
    
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

        # Draw the slider on the screen, update the display, and limit the frame rate to 120 frames per second
        slider.draw(screen)
        pygame.display.flip()
        clock.tick(120)

    pygame.quit()

if __name__ == "__main__":
    main()