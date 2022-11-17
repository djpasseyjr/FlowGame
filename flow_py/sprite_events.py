# Sprite events
from flow_py.flow_tools import in_interval
import pygame
import numpy as np
import pathlib

IMAGE_PATH = (pathlib.Path(__file__).parents[1] / "images").resolve()

PLANT_LEVEL_IDX = 0
SOIL_WATER_LEVEL_IDX = 1

QUARTER1 = pygame.Rect(0, 0, 640, 640)
QUARTER2 = pygame.Rect(640, 0, 640, 640)
QUARTER3 = pygame.Rect(0, 640, 640, 640)
QUARTER4 = pygame.Rect(640, 640, 640, 640)
QUARTERS = [QUARTER1, QUARTER2, QUARTER3, QUARTER4]

class SpriteEvent:

    def __init__(self,
                 num_extra_states=0,
                 extra_state_names=[],
                 imgs=[],
                 anchors=[],
                 cycle=False,
                 frame_rate=1,
                 event_indicator=lambda fd: False):

        self.state = np.zeros(1 + num_extra_states)
        self.state_names = ["cycle idx"]
        self.imgs = imgs
        self.anchors = anchors
        self.cycle = cycle
        self.frame_rate = frame_rate
        self.event_indicator = event_indicator
        self.display = False

    def detect_event(self, fd):
        self.display = self.event_indicator(fd)

    def blit(self, surface):
        if self.display:
            if self.cycle:
                # Increase picture idx but mod by the number of pictures * rate
                state = (self.state[0] + 1) % (len(self.imgs) * self.frame_rate)
                i = int(state) // self.frame_rate
                surface.blit(self.imgs[i], self.anchors[i])
                self.state[0] = state
            else:
                for img, anc in zip(self.imgs, self.anchors):
                    surface.blit(img, anc)

    def __call__(self, fd, surface):
        self.detect_event(fd)
        self.blit(surface)
# Events
def pipe_flow_event(screen_size=(640, 640)):
    """Creates a SpriteEvent that cycles through low pipe flow pictures."""
    # Detect key press
    indicator = lambda fd: pygame.key.get_pressed()[pygame.K_SPACE]
    # Make images
    width, height = screen_size
    img = pygame.image.load(IMAGE_PATH / "pipe_low.png")
    img = pygame.transform.scale(img, (2 * width, 2 * height))
    pipes = [pygame.transform.chop(img, q) for q in QUARTERS]
    anchors = [(0, 0)] * 4
    # Put them together
    sp = SpriteEvent(imgs=pipes, anchors=anchors, frame_rate=1,
                     cycle=True, event_indicator=indicator)
    return sp

def pipe_no_flow_event(screen_size=(640, 640)):
    """Creates a SpriteEvent that displays a pipe with no flow."""
    # Detect key press
    indicator = lambda fd: not pygame.key.get_pressed()[pygame.K_SPACE]
    # Pipe image
    width, height = screen_size
    img = pygame.image.load(IMAGE_PATH / "pipe.png")
    img = pygame.transform.scale(img, (2 * width, 2 * height))
    pipe = pygame.transform.chop(img, QUARTER1)
    # Put them together
    sp = SpriteEvent(imgs=[pipe], anchors=[(0,0)], event_indicator=indicator)
    return sp

def rain_event(screen_size=(640, 640)):
    """Creates a SpriteEvent that cycles through low pipe flow pictures."""
    # Detect key press
    indicator = lambda fd: pygame.key.get_pressed()[pygame.K_SPACE]
    # Make images
    width, height = screen_size
    img = pygame.image.load(IMAGE_PATH / "clouds1.png")
    img = pygame.transform.scale(img, (2 * width, 2 * height))
    pipes = [pygame.transform.chop(img, q) for q in QUARTERS]
    anchors = [(0, 0)] * 4
    # Put them together
    sp = SpriteEvent(imgs=pipes, anchors=anchors, frame_rate=1,
                     cycle=True, event_indicator=indicator)
    return sp

def no_rain_event(screen_size=(640, 640)):
    """Creates a SpriteEvent that displays a pipe with no flow."""
    # Detect key press
    indicator = lambda fd: not pygame.key.get_pressed()[pygame.K_SPACE]
    width, height = screen_size
    img = pygame.image.load(IMAGE_PATH / "clouds0.png")
    img = pygame.transform.scale(img, (2 * width, 2 * height))
    pipe = pygame.transform.chop(img, QUARTER1)
    # Put them together
    sp = SpriteEvent(imgs=[pipe], anchors=[(0,0)], event_indicator=indicator)
    return sp

def state_window_event(fd_state_idx, window, img_file,
                       anchor=(0, 0), screen_size=(640, 640)):
    """Blits the image at `img_file` if `FlowDynamics.state[fd_state_idx]`
    is contained in `window`."""
    indicator = lambda fd, i=fd_state_idx, w=window: in_interval(fd.state[i], w)
    img = pygame.image.load(img_file)
    img = pygame.transform.scale(img, screen_size)
    sp = SpriteEvent(imgs=[img], anchors=[anchor],
                     cycle=True, event_indicator=indicator)
    return sp

# Vegitation events
def grass_event(window=(-np.inf, 10)):
    return state_window_event(PLANT_LEVEL_IDX, window,
                              IMAGE_PATH / "grass.png")
def small_plants_event(window=(10, 20)):
    return state_window_event(PLANT_LEVEL_IDX, window,
                              IMAGE_PATH / "small_plants.png")
def med_plants_event(window=(20, 30)):
    return state_window_event(PLANT_LEVEL_IDX, window,
                              IMAGE_PATH / "med_plants.png")
def big_plants_event(window=(30, np.inf)):
    return state_window_event(PLANT_LEVEL_IDX, window,
                              IMAGE_PATH / "big_plants.png")
