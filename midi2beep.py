#!/bin/python
from subprocess import getoutput
from math import exp,log
from sys import exit, argv
from os import getuid
try:
	from pretty_midi import PrettyMIDI
except ImportError:
	print("PrettyMIDI needed, install it from pip.")
	sys.exit()
drums = { ## Massive array of all drum names to help with implementing them
'37':'Side Stick',
'39':'Hand Clap',
'42':'Closed Hi-Hat',
'44':'Pedal Hi-Hat',
'46':'Open Hi-Hat',
'49':'Crash Cymbal 1',
'51':'Ride Cymbal 1',
'54':'Tambourine',
'56':'Cowbell',
'58':'Vibraslap',
'35':'Accoustic Bass Drum',
'36':'Bass Drum 1',
'38':'Accoustic Snare',
'40':'Electric Snare',
'41':'Low Floor Tom',
'43':'High Floor Tom',
'45':'Low Tom',
'47':'Low-Mid Tom',
'48':'Hi-Mid Tom',
'50':'High Tom',
'52':'Chinese Cymbal',
'53':'Ride Bell',
'55':'Splash Cymbal',
'57':'Crash Cymbal 2',
'59':'Ride Cymbal 2',
'61':'Low Bongo',
'63':'Open Hi Conga',
'66':'Low Timbale',
'68':'Low Agogo',
'70':'Maracas',
'73':'Short Guiro',
'75':'Claves',
'78':'Mute Cuica',
'80':'Mute Triangle',
'60':'Hi Bongo',
'62':'Mute Hi Conga',
'64':'Low Conga',
'65':'High Timbale',
'67':'High Agogo',
'69':'Cabasa',
'71':'Short Whistle',
'72':'Long Whistle',
'74':'Lon Guiro',
'76':'Hi Wood Block',
'77':'Low Wood Block',
'79':'Open Cuica',
'81':'Open Triangle'
} 
help="midi2beep -m file [-c 0] [-h] [-q] [-d] \n\
Program to play a midi track on the PC speaker/buzzer\n\
where:\n\
\t-c Choose the MIDI channel you want to play (default :1)\n\
\t-h Display this help\n\
\t-i Display infos about the MIDI file (useful for finding channels) //not implemented\n\
\t-m MIDI file to play (mandatory)\n\
\t-q Doesn't play a sound\n\
\t-s Modify the speed of playback (not limited to int) //not implemented\n\
\t-d Experimental drum mode\n\
\n(c) int10h. Licensed under GPLv3. Attributions to Cquoicebordel for the original Bash version."
if getuid() != 0:
    print('needs to be run as root, no sudo due to beep not allowing it.')
    exit()
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
command.append('beep -f 0 -l 0')
midi = mid[channel].notes
for i in range(0,len(midi)):
    Note = midi[i]
    if i+1 == len(midi): ## avoid pesky index errors
        break
    Note2 = midi[i+1]
    note= round(440*exp(((Note.pitch-69)/12) * log(2)),2) ## weird midi notation -> freq
    time= round((Note.end - Note.start)* 1000,2) ## note objects in prettymidi are very nice to work with
    if Note.end == Note2.start: ## no overlap or delay
        command1="-n -f {} -l {}".format(note,time)
        command.append(command1)
    if Note.end < Note2.start: ## handles delay
        delay = int((Note2.start - Note.end) * 1000)
        command1="-n -f {} -l {} -d {}".format(note,time, delay)
        command.append(command1)
    if Note.end < Note2.start: ## attempts to handle overlap, appears to fail? need to look at lib
        time = (Note.end-(Note2.start-Note.end))*1000
        command1="-n -f {} -l {}".format(note,time)
        if time <= 0: ## if somethings sodded up, just get out
            continue
        command.append(command1)
    if '-d' in argv:  
        print(drums[str(Note.pitch)]) ## drum debugging
    if command == '':
        exit()      

totalcommand = ' '.join(command)
if '-q' not in argv:
    getoutput(totalcommand) ## massive getoutput at the end, as line by line only occasionally works for some reason on my machine(s)
