import numpy as np
import time
import pygame, sys

t = 0.1  # update time interval


class TestBoat():
    """ This is just a boat object used for testing"""

    def __init__(self):
        self.x_position = 0
        self.y_position = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.heading = 0  # degrees counterclockwise from north
        # variables for plotting
        self.color = (180, 50, 50)  # this is red
        self.width = 15
        self.height = 40

        # This creates the surface which holds the ellipse and draws it"
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # takes dimensions and transparent
        self.ellipse = pygame.draw.ellipse(self.surface, self.color, (0, 0, self.width, self.height))

    def plot(self, x, y, heading):
        # use the pygame.transform module to rotate the original surface by 45°
        surface2 = pygame.transform.rotate(self.surface, heading)
        screen.blit(surface2, (x, y))

    def update_boat_position(self):
        self.x_position += self.x_velocity * t
        self.y_position += self.y_velocity * t


class TestBuoy():
    """Bouy object used for testing"""

    def __init__(self):
        self.x_position = 0
        self.y_position = 0
        self.rel_polar_angle = 0  # degrees clockwise from north
        self.rel_polar_distance = 0  # polar coordinates with respect to the boat


grid_distance = 25


def draw_grid():
    for i in range(grid_distance, screen.get_width(), grid_distance):
        pygame.draw.line(screen, (0, 0, 0), (i, 0), (i, screen.get_height() - 40), 1)
    for i in range(grid_distance, screen.get_height() -40 , grid_distance):
        pygame.draw.line(screen, (0, 0, 0), (0, i), (screen.get_width(), i))

pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 20)

def print_text(string, location):
    """prints the string in the pygame window at the selected location"""
    text_surface = myfont.render(string, False, (0,0,0))
    screen.blit(text_surface, location)

# setup of the base screen and objects

screen = pygame.display.set_mode((900, 900))
screen.fill((255, 250, 200))

boat = TestBoat()
bouy1 = TestBuoy()
bouy2 = TestBuoy()
bouy3 = TestBuoy()

# this is in place of input data
########################################
boat.x_position = 100
boat.y_position = 100
boat.y_velocity = 30
boat.x_velocity = 70
boat.heading = 45

bouy1.x_position = 800
bouy1.y_position = 500
bouy2.x_position = 50
bouy2.y_position = 50
bouy3.x_position = 150
bouy3.y_position = 70
########################################


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    boat.update_boat_position()
    screen.fill((173, 216, 230))
    draw_grid()
    boat.plot(boat.x_position, boat.y_position, boat.heading)  # drawing the boat

    # drawing buoys
    pygame.draw.circle(screen, (0, 0, 0), (bouy1.x_position, bouy1.y_position), 5)
    pygame.draw.circle(screen, (0, 0, 0), (bouy2.x_position, bouy2.y_position), 5)
    pygame.draw.circle(screen, (0, 0, 0), (bouy3.x_position, bouy3.y_position), 5)

    a = (f"boat position: ({boat.x_position}, {boat.y_position})")
    print_text(a, (10, screen.get_height() -40))


    pygame.display.update()
    time.sleep(t)