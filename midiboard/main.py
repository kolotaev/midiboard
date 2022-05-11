
import sys

from app import CliApplication, GuiApplication


if __name__ == '__main__':
    import mido
    outs = mido.get_output_names()
    print(outs)
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        a = CliApplication()
    else:
        a = GuiApplication()
    print('Starting...')
    a.run()
