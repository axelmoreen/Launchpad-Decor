import mido
import time
from time import sleep
import random
from views import *
from util import *

print(mido.get_output_names())

port_name = "MIDIOUT2 (LPMiniMK3 MIDI) 3"
print("Using "+port_name)
port = mido.open_output(port_name)
# midiout2 CUSTOM MODE NOTES GO FROM 56 to 124!
# midiout2 PROGM MODE NOTES GO FROM 11 TO 100!

progm_data = [0, 32, 41, 2, 13, 14, 1]
livem_data = [0, 32, 41, 2, 13, 14, 0]

progm = mido.Message('sysex', data=progm_data)
port.send(progm)

tempo = mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(10))
#port.send(tempo)

MIN = 11
MAX = 99


def debug_on_off(note, color=1, sleep=0.07):
    msg = mido.Message('note_on', note=note, velocity=color)
    port.send(msg)
    time.sleep(sleep)
    msg = mido.Message('note_on', note=note, velocity=0)
    port.send(msg)


def off_all():
    for i in range(1, 10):
        for k in range(1, 10):
            msg = mido.Message('note_on', note=10*i + k, velocity=0)
            port.send(msg)


def render_frame(frame):
    for x in range(0, len(frame.grid)):
        for y in range(0, len(frame.grid[0])):
            port.send(mido.Message('note_on', channel=frame.get_channel_value((x, y)), note=grid_to_midi(
                x, y), velocity=frame.get_value((x, y))))


#picks = {"snake": 0.4, "clock": 0.35, "pong": 0.05, "scroller": 0.2}
picks = {"rbreathe": 0.2, "rain": 0.2,
         "snake": 0.2, "clock": 0.2, "scroller": 0.2}
#picks = {"rain": 1}
while True:
    s = 0
    k = 0
    t = random.random()
    it = list(picks.items())
    pick = None
    while k < len(it):
        s += it[k][1]
        if (s > t):
            pick = it[k][0]
            break
        k += 1
    view = None
    if pick == "pong":
        view = Pong()
    elif pick == "scroller":
        view = SpaceScroller()
    elif pick == "snake":
        view = LinearSnake()
    elif pick == "clock":
        view = Clock()
    elif pick == "rbreathe":
        view = RadialBreathe()
    elif pick == "rain":
        view = Rain()

    if pick != "clock":
        view.compile()
        for frame in view.frames:
            render_frame(frame)
            msg2 = mido.Message("clock")
            port.send(msg2)
            time.sleep(1/view.framespeed)
    else:
        render_frame(view.get_frame())
        time.sleep(15)
