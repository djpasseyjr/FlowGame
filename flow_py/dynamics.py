""" Class for implementing the numerical ode engine underneath the game.

Main class is `FlowDynamics` with key `.step()` method, called during the game
event loop.

`FlowDynamics` is highly customizable as can have a variable length state
and accepts lists of derivatives for each state. It also accepts a list of
associated SpriteEvents. These events check if they should display each timestep
and if they should, they blit their associated sprites.

With these pieces in place, a `FlowDynamics` class has everything it needs to
be a complete game scenario, sprites and all.
"""
import copy
import numpy as np
import pygame
from scipy.integrate import odeint
import flow_py.flow_tools as ft
import flow_py.sprite_events as se

PLANT_LEVEL_IDX = 0
SOIL_WATER_LEVEL_IDX = 1
# Default derivatives

def plant_growth_rate(optimal_soil=(0., 40.), growth_rate=1., decay_rate=-1.):
    """Returns a function that produces `growth_rate` when the soil water
    level is within the `optimal_soil` interval and produces `decay_rate`
    otherwise.
    """
    i = SOIL_WATER_LEVEL_IDX
    dp_dt = ft.interval_indicator_dt(optimal_soil, i, on_true=growth_rate,
                                     on_false=decay_rate)
    return dp_dt

def water_flow_rate(on_push=1., no_push=-1.):
    return ft.input_switched_constants_dt(on_push, no_push)

class FlowDynamics:
    """Class for storing and updating soil and plant dynamics."""
    max_stored_timesteps = 100_000

    def __init__(self,
                 num_extra_states=0,
                 extra_state_names=[],
                 derivatives=[plant_growth_rate(),
                              water_flow_rate()],
                 sprite_events=[se.grass_event(), se.small_plants_event(),
                                se.med_plants_event(), se.big_plants_event(),
                                se.no_rain_event(), se.rain_event()],
                 initial_state=[0., 0.],
                 numerical_dt=0.01):
        """Initializes FlowDynamics.

        Args:
            num_extra_states: Number of internal states in addition to
                "vegitation_level" and "soil_water_level"
            extra_state_names: Names of all extra states.
            derivatives: List of callables with length equal to
                num_extra_states + 2. Each callable should be of the form
                    f(x, t, inp) -> dx
                where x is an array with length = (num_extra_states + 2)
                t is a float, the current time value, and inp is a bool
                signifying if a key is pressed or not.
            sprite_events: List of SpriteEvent instances to call on this class
            initial_state: Array of initial values for each state.
        """

        nd = len(derivatives)
        ns = num_extra_states + 2
        nsn = len(extra_state_names) + 2
        nis = len(initial_state)
        if (nd != ns) or (nd != ns) or (nd != nsn) or (nd != nis):
            raise ValueError("Number of states, state names, initial "
                             "state length, and number of derivatives"
                             " must all be equal.")
        # Timestep for numerical solver
        self.numerical_dt = numerical_dt
        self.sprite_events = sprite_events

        # Start time
        self.time_points = np.zeros(1)
        self.end = False

        # Internal states
        self.state = initial_state
        self.state_names = ["plant_level", "soil_water_level"] + extra_state_names
        self.state_history = copy.deepcopy(self.state)
        # Derivatives of each state
        self.derivatives = derivatives

    def update_history(self, states, time_points):
        # Drop first state because it was the last state of the previous step
        self.state_history = np.vstack([self.state_history, states[1:, :]])
        self.time_points = np.hstack([self.time_points, time_points[1:]])
        # Prevent history from getting too big
        # Note `len()` gives the number of rows in a 2D array here
        if len(self.state_history) > self.max_stored_timesteps:
            self.state_history = self.state_history[len(states):, :]
            self.time_points = self.time_points[len(states):]

    def dxdt(self, x, t, inp):
        return [ddt(x, t, inp) for ddt in self.derivatives]

    def step(self, inp, timestep):
        """Steps forward one timestep.

        Args:
            inp: Boolian. True if a key is pressed, false otherwise.
            timestep: The amount to step the flow simulation forward
                in time.
        """
        # Timesteps
        curr_time = self.time_points[-1]
        end_time = curr_time + timestep + self.numerical_dt
        time_points = np.arange(curr_time, end_time, self.numerical_dt)
        # Scipy integrator
        states = odeint(self.dxdt, self.state, time_points, (inp,))
        self.state = states[-1]
        self.update_history(states, time_points)
