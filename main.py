import mido
import time
from time import sleep
import random
from views import *
from util import *
import threading
import subprocess

print(mido.get_output_names())
names = mido.get_output_names()
match = [s for s in names if "MIDIOUT2 (LPMiniMK3 MIDI)" in s]
if len(match) == 0:
    raise("Could not find Launchpad!")
    quit()

port_name = match[0]
#port_name = "MIDIOUT2 (LPMiniMK3 MIDI) 3"
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

running = True
# load configuration here
music_programs = ["reaper.exe", "FL64.exe", "FL32.exe", "Ableton Index.exe"]


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


picks = {"rbreathe": 0.2, "rain": 0.2,
         "snake": 0.2, "checkers": 0.2, "scroller": 0.2}
#picks = {"asteroids": 1}


def run_view(view):
    global port
    view.compile()
    for frame in view.frames:
        if not running:
            break
        render_frame(frame)
        msg2 = mido.Message("clock")
        port.send(msg2)
        time.sleep(1/view.framespeed)


def run_display():
    while True:
        if not running:
            time.sleep(10)
        else:
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
            elif pick == "checkers":
                view = Checkers()
            elif pick == "asteroids":
                view = Asteroids()

            if pick != "clock":
                run_view(view)

            else:
                render_frame(view.get_frame())
                time.sleep(5)


disp = threading.Thread(target=run_display, daemon=True)
disp.start()


while True:
    if not running:
        time.sleep(10)

    output = subprocess.check_output(('TASKLIST', '/FO', 'CSV')).decode()
    # get rid of extra " and split into lines
    output = output.replace('"', '').split('\r\n')
    keys = output[0].split(',')
    proc_list = [i.split(',') for i in output[1:] if i]
    # make dict with proc names as keys and dicts with the extra nfo as values
    proc_dict = dict((i[0], dict(zip(keys[1:], i[1:]))) for i in proc_list)
    found = False
    for name, values in sorted(proc_dict.items(), key=lambda x: x[0].lower()):
        if name in music_programs:
            if running:
                livem = mido.Message('sysex', data=livem_data)
                port.send(livem)
                running = False
            found = True
            break
    if not found:
        running = True
        progm = mido.Message('sysex', data=progm_data)
        port.send(progm)
    time.sleep(3)
