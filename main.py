import sys

from midiboard.app import exec


if __name__ == '__main__':
    is_cli = len(sys.argv) > 1 and sys.argv[1] == 'cli'
    exec(is_cli)
