
import mido
from pynput.keyboard import Key, Listener

from state import State
from midimapping import KEYS_NOTES_MAP
import utils


class Midiboard():
    def __init__(self, *args, **kwargs):
        self.state = State()
        self.outport = mido.open_output('IAC Driver Virtual cable')
        self.keyboard_listener = None
    
    def toggle_enable(self):
        self.state.on = not self.state.on
        print(f'App is enabled: {self.state.on}')
    
    def disabled(self):
        return not self.state.on

    def run(self):
        def on_release(key):
            if self.disabled():
                return
            try:
                print(f'alphanumeric key {key.char} ({key}) released')
                key_symbol_released = str(key)[1:-1]
                self.state.remove_pressed_key(key_symbol_released)
                note = KEYS_NOTES_MAP.get(key_symbol_released)
                if note is None:
                    return
                try:
                    mm = mido.Message('note_off',
                                note=utils.octaved_note(self.state, note), 
                                velocity=utils.rand_velocity(), time=6.2)
                    self.outport.send(mm)
                except ValueError as e:
                    print(e)
            except AttributeError:
                print(f'special key {key} released')

        def on_press(key):
            if key == Key.esc:
                self.toggle_enable()
            if self.disabled():
                return
            print(f'{key} pressed')
            # Change octaves
            if key == Key.up:
                self.state.octave += 1
            elif key == Key.down:
                self.state.octave -= 1
            # Map to notes
            # ToDo - maybe map to keyboard.Key values
            key_symbol_pressed = str(key)[1:-1]
            base_note = KEYS_NOTES_MAP.get(key_symbol_pressed)
            if base_note is None:
                return
            octaved_note = utils.octaved_note(self.state, base_note)
            if self.state.was_key_pressed(key_symbol_pressed):
                if self.state.polytouch_on:
                    self.outport.send(mido.Message('polytouch', note=octaved_note, value=utils.rand_velocity()))
                return
            self.state.add_pressed_key(key_symbol_pressed)
            try:
                mm = mido.Message('note_on', note=octaved_note, velocity=utils.rand_velocity(), time=6.2)
                self.outport.send(mm)
            except ValueError as e:
                print(e)
        
        def darwin_intercept(event_type, event):
            try:
                # hacky private access, but it's better then own implementation
                key = self.keyboard_listener._event_to_key(event)
            except IndexError:
                key = None
            print(f'-----\ndarwin key {key} pressed\n')
            if key in (Key.esc, Key.up, Key.down): # Block keys that are not allowed to be passed anyway!
                return None
            if not self.disabled() and KEYS_NOTES_MAP.get(str(key)[1:-1]) is not None:
                return None
            return event

        self.keyboard_listener = Listener(
            darwin_intercept=darwin_intercept,
            suppress=True,
            on_press=on_press,
            on_release=on_release
        )
        print(f'Is App trusted? Answer: {self.keyboard_listener.IS_TRUSTED}')
        print('Started listening.')
        self.keyboard_listener.start()
