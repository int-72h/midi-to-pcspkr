#!/bin/python
from math import exp,log
from sys import exit, argv
try:
    from pretty_midi import PrettyMIDI
except ImportError:
    print("PrettyMIDI needed, install it from pip.")
    sys.exit()
help="midi2beep -m file [-c 0] [-h] [-q] [-d] \n\
Program to produce a string which can be put in grub as an init-tune to play on boot \n\
where:\n\
\t-c Choose the MIDI channel you want to play (default :1)\n\
\t-h Display this help\n\
\t-m MIDI file to play (mandatory)\n\
\t-q Doesn't produce output\n\
\n(c) int10h. Licensed under GPLv3."
if len(argv) == 0 or '-h' in argv:
    print(help)
    exit()
channel = 0
if '-m' in argv:
    midifile = argv[argv.index('-m')+1]
else:
    print(help)
    exit()
if '-c' in argv:
    try:
        channel = int(argv[argv.index('-c')+1])
    except ValueError:
        print('invalid channel!')
        exit()
mid = PrettyMIDI(midifile).instruments
command = []
command.append('60000')
midi = mid[channel].notes
for i in range(0,len(midi)):
    Note = midi[i]
    if i+1 == len(midi): ## avoid pesky index errors
        break
    Note2 = midi[i+1]
    note= int(440*exp(((Note.pitch-69)/12) * log(2))) ## weird midi notation -> freq
    time= int((Note.end - Note.start)* 1000) ## note objects in prettymidi are very nice to work with
    if Note.end == Note2.start: ## no overlap or delay
        command1="{} {}".format(note,time)
        command.append(command1)
    if Note.end < Note2.start: ## handles delay
        delay = int((Note2.start - Note.end) * 1000)
        command1="0 {}".format(delay)
        command.append(command1)
    if Note.end < Note2.start: ## attempts to handle overlap, appears to fail? need to look at lib
        time = int((Note.end-(Note2.start-Note.end))*1000)
        if time > 5000:
            continue
        command1="{} {}".format(note,time)
        if time <= 0: ## if somethings sodded up, just get out
            continue
        command.append(command1)
    if '-d' in argv:  
        print(drums[str(Note.pitch)]) ## drum debugging
    if command == '':
        exit()      

totalcommand = ' '.join(command)
if '-q' not in argv:
    print(totalcommand) ## massive getoutput at the end, as line by line only occasionally works for some reason on my machine(s)
