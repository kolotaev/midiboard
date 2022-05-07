import time

from pynput import keyboard
import mido
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from state import State
from constants import KEYS_NOTES_MAP
import utils


class Midiboard():
    def __init__(self, *args, **kwargs):
        # super(QSystemTrayIcon, self).__init__(*args, **kwargs)
        self.state = State()
        self.outport = mido.open_output('IAC Driver Virtual cable')
        self.keyboard_listener = None
        # self.run()
    
    def toggle_enable(self):
        self.state.on = not self.state.on
        print(f'App is enabled: {self.state.on}')
    
    def disabled(self):
        return not self.state.on

    def run(self):
        def restart_listener(suppress):
            if self.keyboard_listener:
                self.keyboard_listener.stop()
            self.keyboard_listener = keyboard.Listener(
                suppress=suppress,
                on_press=on_press,
                on_release=on_release
            )
            self.keyboard_listener.start()
        
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
            if key == keyboard.Key.esc:
                self.toggle_enable()
                restart_listener(suppress=not self.disabled())
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

        try:
            restart_listener(True)
            # var = False
            # import threading
            # def f():
            #     import time
            #     counter = 0
            #     kbl = keyboard.Listener(
            #         suppress=True,
            #         on_press=on_press,
            #         on_release=on_release
            #     )
            #     kbl.start()
            #     while var:
            #         time.sleep(0.1)
            #         print("Function {} run!".format(counter))
            #         counter+=1
            # t1 = threading.Thread(target=f)
            # t1.start()

            print(f'Is App trusted? Answer: {self.keyboard_listener.IS_TRUSTED}')
            print('Started listening.')
        except Exception as e:
            print(e)


class CliApplication():
    def run(self):
        mb = Midiboard()
        mb.run()
        while True:
            time.sleep(0.01)


class GuiMidiboard(QSystemTrayIcon, Midiboard):
    def __init__(self, *args, **kwargs):
        super(QSystemTrayIcon, self).__init__(*args, **kwargs)
        super(Midiboard, self).__init__(*args, **kwargs)


class GuiApplication:
    def run(self):
        app = QApplication([])
        app.setQuitOnLastWindowClosed(False)

        # Create the icon
        icon = QIcon('resources/easy.png')

        # Create the tray
        midiboard_tray = GuiMidiboard()
        midiboard_tray.setIcon(icon)
        midiboard_tray.setVisible(True)
        midiboard_tray.run()

        # Create the menu
        menu = QMenu()
        action = QAction("A menu item")
        menu.addAction(action)
        # Add a Quit option to the menu.
        quit = QAction("Quit")
        quit.triggered.connect(app.quit)
        menu.addAction(quit)

        # Add the menu to the tray
        midiboard_tray.setContextMenu(menu)
        app.exec_()
