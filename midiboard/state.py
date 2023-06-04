class State:
    def __init__(self):
        self.on = True
        self._pressed_keys = {}
        # todo - move to config
        self.octave = 0
        self.polytouch_on = True
        self.rand_polytouch_enabled = True
        self.rand_velocity_enabled = True

    def add_pressed_key(self, key):
        self._pressed_keys[key] = True

    def remove_pressed_key(self, key):
        self._pressed_keys.pop(key, None)

    def was_key_pressed(self, key):
        return key in self._pressed_keys
