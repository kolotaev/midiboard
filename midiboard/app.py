import time

import mido
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from .board import Midiboard


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
        icon = QIcon('resources/piano.png')

        # Create the tray
        midiboard_tray = GuiMidiboard()
        midiboard_tray.setIcon(icon)
        midiboard_tray.setVisible(True)
        midiboard_tray.run()

        # Create the menu
        menu = QMenu()
        # Random velocity button
        random_vel = QAction("Random vel", checkable=True)
        random_vel.setChecked(midiboard_tray.state.rand_velocity_enabled)
        # ToDo - redo with signals and slots (+ state reader-only access)
        def on_triggered():
            midiboard_tray.state.rand_velocity_enabled = not midiboard_tray.state.rand_velocity_enabled
            random_vel.setChecked(midiboard_tray.state.rand_velocity_enabled)
        random_vel.triggered.connect(on_triggered)
        menu.addAction(random_vel)
        # Add a Quit option to the menu.
        quit = QAction("Quit")
        quit.triggered.connect(app.quit)
        menu.addAction(quit)

        # Add the menu to the tray
        midiboard_tray.setContextMenu(menu)
        app.exec_()


def exec(cli=False):
    outs = mido.get_output_names()
    print(outs)
    print('Starting...')
    if cli:
        CliApplication().run()
    else:
        GuiApplication().run()
