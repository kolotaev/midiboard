from app import Application


if __name__ == '__main__':
    import mido
    outs = mido.get_output_names()
    print(outs)
    a = Application()
    print('Starting...')
    a.run()
