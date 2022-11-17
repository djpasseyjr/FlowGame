from dynamics import FlowDynamics
import itertools
import pygame
import sys
import time

SCREEN_HIEGHT = 640
SCREEN_WIDTH = 640
SCREEN_SIZE = (SCREEN_HIEGHT, SCREEN_WIDTH)

IMAGE_FILE_SIZE = (128, 128)
IMAGE_FILE_RESIZE = (1280, 1280)

QUARTER1 = pygame.Rect(0, 0, 640, 640)
QUARTER2 = pygame.Rect(640, 0, 640, 640)
QUARTER3 = pygame.Rect(0, 640, 640, 640)
QUARTER4 = pygame.Rect(640, 640, 640, 640)

def load_image(im_file):
    """Each of my png files contains four 64 x 64 images.
     To fit the screen, we resize the entire image to 1280 x 1280.
    """
    img = pygame.image.load(im_file)
    img = pygame.transform.scale(img, IMAGE_FILE_RESIZE)
    return img


pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE)

# Load Images
# Pipe Images
pipe = load_image("../images/clouds0.png")
pipe_low = load_image("../images/clouds4.png")

# Plant images
lush_plants = load_image("../images/lush.png")
wet_plants = load_image("../images/wet.png")
wet_dying_plants = load_image("../images/wet_dying.png")
dry_plants = load_image("../images/dry.png")
dry_dying_plants = load_image("../images/dry_dying.png")

img_dict = {
    "lush": lush_plants,
    "wet": wet_plants,
    "dry": dry_plants,
    "wet_dying": wet_dying_plants,
    "dry_dying": dry_dying_plants
}

quarters = [QUARTER1, QUARTER2, QUARTER3, QUARTER4]

fd = FlowDynamics()

i = 0
print("i   fd.soil_water_level fd.vegitation_level fd.vegitation_state")

while True:
    print(i, "\t", fd.soil_water_level, "\t", fd.vegitation_level, "\t", fd.vegitation_state)
    i += 1
    # time.sleep(1)

    # Check for exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    # Check for pressed keys
    keys = pygame.key.get_pressed()
    if i % 100 == 0:
        fd.vegitation_transition()

    screen.blit(img_dict[fd.vegitation_state], (0,0), quarters[fd.vegitation_level])

    # Animate water flow by changing which quarter of the image
    # to display
    if keys[pygame.K_SPACE]:
        screen.blit(pipe, (0, 0), quarters[0])
        fd.update_soil_water_level(False)
    else:
        pipe_frame = (i % 40) // 10
        screen.blit(pipe_low, (0, 0), quarters[pipe_frame])
        fd.update_soil_water_level(True)

    pygame.display.flip()
