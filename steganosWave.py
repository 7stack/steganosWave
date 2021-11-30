

import click
import wave
import argparse
from loaders import TextLoader

parser = argparse.ArgumentParser()


parser.add_argument("-f", help="Select Audio File", dest="audiofile")
parser.add_argument("-m", help="Enter your Secret Message", dest="secretmsg")
parser.add_argument("-o", help="Your Output file path and name", dest="outputfile")
parser.add_argument("-e", help="Select Audio File To Extract Message", dest="exfile")

args = parser.parse_args()

audiofile = args.audiofile
string = args.secretmsg
outputfile = args.outputfile
exfile = args.exfile


def clean():
    # Clear screen using click.clear() function
    click.clear()


def banner():
    print(
        """\033[0m \033[1;37m
          __                                           
  _______/  |_  ____   _________    ____   ____  ______
 /  ___/\   __\/ __ \ / ___\__  \  /    \ /  _ \/  ___/
 \___ \  |  | \  ___// /_/  > __ \|   |  (  <_> )___ \ 
/____  > |__|  \___  >___  (____  /___|  /\____/____  > 
     \/            \/_____/     \/     \/ \033[1;33mV1.0\033[1;37m      \/ \033[1;33mWAVE
\033[1;37mMIT License Copyright (c) 2021 symmetricAlgo1     
\033[92mVisit for more amazing: https://github.com/symmetricAlgo1\033[0m 
\033[1;37mSteganos your message in wave audio file\033[0m"""
    )


def help():
    print(
        """usage: HiddenWave.py [-h] [-f AUDIOFILE] [-m SECRETMSG] [-o OUTPUTFILE]

optional arguments:
  -h, --help    show this help message and exit
  -f AUDIOFILE  Select Audio File
  -m SECRETMSG  Enter your message
  -o OUTPUTFILE Your output file path and name"""
    )


def steg_audio(af, string, output):

    print("Please wait........")
    waveaudio = wave.open(af, mode="rb")
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    string = string + int((len(frame_bytes) - (len(string) * 8 * 8)) / 8) * "#"
    bits = list(
        map(int, "".join([bin(ord(i)).lstrip("0b").rjust(8, "0") for i in string]))
    )
    for i, bit in enumerate(bits):
        frame_bytes[i] = (frame_bytes[i] & 254) | bit
    frame_modified = bytes(frame_bytes)
    with wave.open(output, "wb") as fd:
        fd.setparams(waveaudio.getparams())
        fd.writeframes(frame_modified)
    waveaudio.close()
    print("Done...")


def extr_msg(af):

    print("Please wait......")
    waveaudio = wave.open(af, mode="rb")
    frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
    extracted = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
    string = "".join(
        chr(int("".join(map(str, extracted[i : i + 8])), 2))
        for i in range(0, len(extracted), 8)
    )
    msg = string.split("###")[0]
    print("Your Secret Message is: \033[1;91m" + msg + "\033[0m")
    waveaudio.close()


banner()

if audiofile and string and outputfile:
    try:
        steg_audio(audiofile, string, outputfile)
    except:
        print("Something went wrong!! try again")
        quit("")
else:
    if not exfile:
        help()
    else:
        try:
            extr_msg(exfile)
        except:
            print("Something went wrong!! try again")
            quit("")

