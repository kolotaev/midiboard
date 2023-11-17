class State:
    def __init__(self):
        self.on = True
        self._pressed_keys = set()
        # todo - move to config
        self.octave = 0
        self.rand_velocity_enabled = True
        self.polytouch_on = True
        self.rand_polytouch_enabled = True # not configurable right now

    def add_pressed_key(self, key):
        self._pressed_keys.add(key)

    def remove_pressed_key(self, key):
        self._pressed_keys.remove(key)

    def was_key_pressed(self, key):
        return key in self._pressed_keys
