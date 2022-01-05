MIN = 11
MAX = 99


def grid_to_midi(x, y):
    # Convert x,y (zero-inclusive) to the midi note
    # extended: If true use outer edge 9x9, otherwise 8x8
    # TO BE FAIR it does not matter if extended or not in this conversion.

    # NOTE THAT the programmer layout skips to start on a 1 every row
    # 91 92 93 94 ...           99
    # ..
    # ...
    # 31 32 33 34 35 ...        39
    # 21 22 23 24 25 ...        29
    # 11 12 13 14 15 ...        19
    if x > 8 or y > 8:
        raise Exception("Grid coordinate out of higher bound")
    if x < 0 or y < 0:
        raise Exception("Grid coordinate out of lower bound")

    return MIN + x + 10 * y
