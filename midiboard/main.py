from app import CliApplication, GuiApplication


if __name__ == '__main__':
    import mido
    outs = mido.get_output_names()
    print(outs)
    a = GuiApplication()
    print('Starting...')
    a.run()
