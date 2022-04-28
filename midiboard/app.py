import re
import time

from pynput.keyboard import Key, Controller
from pynput import keyboard
import mido

from state import State
from constants import KEYS_NOTES_MAP
import utils


class Application:
    def __init__(self):
        self.state = State()
        self.outport = mido.open_output('IAC Driver Virtual cable')
    
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
                    mm = mido.Message('note_off', note=utils.octaved_note(self.state, note), velocity=100, time=6.2)
                    self.outport.send(mm)
                except ValueError as e:
                    print(e)
            except AttributeError:
                print(f'special key {key} released')

        def on_press(key):
            if key == keyboard.Key.esc:
                self.toggle_enable()
            if self.disabled():
                return
            print(f'{key} pressed')
            # Change octaves
            if key == keyboard.Key.up:
                self.state.octave += 1
            elif key == keyboard.Key.down:
                self.state.octave -= 1
            # Map to notes 
            key_symbol_pressed = str(key)[1:-1]
            if self.state.was_key_pressed(key_symbol_pressed):
                return
            self.state.add_pressed_key(key_symbol_pressed)
            base_note = KEYS_NOTES_MAP.get(key_symbol_pressed) 
            if base_note is None:
                return
            octaved_note = utils.octaved_note(self.state, base_note)
            try:
                mm = mido.Message('note_on', note=octaved_note, velocity=100, time=6.2)
                self.outport.send(mm)
            except ValueError as e:
                print(e)
            # if str(key) == "'a'":
            #     mm = mido.Message('note_on', note=50, velocity=100, time=6.2)
            # elif str(key) == "'s'":
            #     mm = mido.Message('note_on', note=60, velocity=100, time=6.2)
            # elif str(key) == "'d'":
            #     mm = mido.Message('note_on', note=70, velocity=100, time=6.2)
            # elif str(key) == "'f'":
            #     for _ in range(127):
            #         mm = mido.Message('control_change', control=2, value=50)
            #         # time.sleep(0.1)
            #         self.outport.send(mm)
            #     return                
            # if key == keyboard.Key.esc:
            #     # Stop listener
            #     return False

        def darwin_intercept(event_type, event):
            import Quartz
            length, chars = Quartz.CGEventKeyboardGetUnicodeString(event, 100, None, None)
            if length <= 0:
                return event
            print(f'darwin chars: =={chars}==')
            # Block every key except several special keys: (ESC, Space)
            if chars not in ['\x1b', ' ']:
                if self.disabled():
                    return event
                return None
            # elif length > 0 and chars == 'a':
            #     # Transform a to b
            #     Quartz.CGEventKeyboardSetUnicodeString(event, 1, 'b')
            else:
                return event

        # Collect events until released
        ll = keyboard.Listener(
            darwin_intercept=darwin_intercept,
            suppress=True,
            on_press=on_press,
            on_release=on_release
        )
        print(f'Is App trusted? Answer: {ll.IS_TRUSTED}')
        print('Started listening.')
        with ll as listener:
            listener.join()
        # # ...or, in a non-blocking fashion:
        # listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        # listener.start()