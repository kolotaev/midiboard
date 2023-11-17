import random


class VelocityGenerator:
    def __init__(self, app_state):
        self._state = app_state

    def velocity(self):
        if self._state.rand_velocity_enabled:
            return random.randint(70, 120)
        return 100


class PolyTouchGenerator:
    def __init__(self, app_state):
        self._state = app_state

    def value(self):
        if self._state.rand_polytouch_enabled:
            return random.randint(50, 125)
        return 0
