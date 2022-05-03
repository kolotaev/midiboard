import random

def octaved_note(state, note):
    return note + 12 * state.octave

def rand_velocity():
    return random.randint(80, 120)
