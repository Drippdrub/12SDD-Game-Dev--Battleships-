import pygame

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

    def draw(self, screen):
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x + self.length, self.y), 2)
        pygame.draw.rect(screen, RED, (self.slider_pos - self.slider_width // 2, self.y - self.slider_width // 2.3, self.slider_width, self.slider_width))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.slider_pos - self.slider_width // 2 <= mouse_pos[0] <= self.slider_pos + self.slider_width // 2 and self.y - self.slider_width // 2 <= mouse_pos[1] <= self.y + self.slider_width // 2:
                        self.set_clicked(True)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.set_clicked(False)
            elif event.type == pygame.MOUSEMOTION:
                if self.clicked:
                    mouse_pos = pygame.mouse.get_pos()
                    self.update(mouse_pos)
                    volume = self.get_value()

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

    slider = Slider(50, 100, 100)
    volume = 0.5  # Initial volume- middle position
    

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        slider.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
