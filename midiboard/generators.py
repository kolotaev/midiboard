import random


class VelocityGenerator:
    def __init__(self, app_state):
        self._state = app_state

    def velocity(self):
        if self._state.rand_velocity_enabled:
            return random.randint(80, 120)
        return 100
