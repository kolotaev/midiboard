class State:
    def __init__(self):
        self.on = True
        self._pressed_keys = []
        # todo - move to config
        self.octave = 0
        self.polytouch_on = True

    def add_pressed_key(self, key):
        self._pressed_keys.append(key)

    def remove_pressed_key(self, key):
        try:
            self._pressed_keys.remove(key)
        except ValueError:
            # todo - maybe log
            pass

    def was_key_pressed(self, key):
        return key in self._pressed_keys
