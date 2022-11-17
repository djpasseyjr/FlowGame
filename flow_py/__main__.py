# Main file for game
import pygame
import pathlib

from pygame import QUIT, KEYUP, KEYDOWN
from .dynamics import FlowDynamics
import sys

SCREEN_SIZE = (640, 640)
FLOW_TIMESTEP = 1.0
IMAGE_PATH = (pathlib.Path(__file__).parents[1] / "images").resolve()

pygame.init()
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])
screen = pygame.display.set_mode(SCREEN_SIZE)

grass_img = pygame.image.load(IMAGE_PATH / "grass.png")
grass_img = pygame.transform.scale(grass_img, SCREEN_SIZE)
screen.blit(grass_img, (0, 0))

fd = FlowDynamics()
print(" vegitation_level  water_level")
i = 0
update_rate = 10

while True:
    i += 1
    print(i, "\t", fd.state[0], "\t", fd.state[1], "\t")
    # Check for exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    # Check for pressed keys
    inp = pygame.key.get_pressed()[pygame.K_SPACE]

    if i % update_rate == 0:
        fd.step(inp, FLOW_TIMESTEP)
        for se in fd.sprite_events:
            se(fd, screen)

    pygame.display.update()
