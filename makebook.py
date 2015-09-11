#!/usr/bin/env python3

import glob
import os
import fileinput
import subprocess
import platform
import shutil

# first, set up a bunch of paths for later
if platform.system == 'Windows':
    songidx = '..\src\songidx.exe'
    bible = '..\src\songidx\bible.can'
    pdflatex = 'C:\Program Files (x86)\MiKTeX 2.9\miktex\bin\pdflatex.exe'

else:
    songidx = '../src/songidx/songidx'
    bible = '../src/songidx/bible.can'
    pdflatex = 'pdflatex'
    shutil.copy2('../src/songs/songs.sty', './songs.sty')

song_glob = os.sep.join(['src','*.txt'])
sbd_header = "header.txt"
sbd_out = "songs.sbd"

# get the list of song files to add and sort it
filenames = sorted(glob.glob(song_glob))

# create the sbd output file
with open(sbd_out, 'w') as fout:
    # add the header boilerplate
    for line in fileinput.input(sbd_header):
        fout.write(line)
    # add the individual files
    for line in fileinput.input(filenames):
        fout.write(line)

# next, get a list of .tex files to use
texfiles = sorted(glob.glob('*.tex'))

# then, regenerate all .tex files, all index files, then all .tex files again
for tex in texfiles:
    print(tex, " Pass 1")
    subprocess.call([pdflatex, tex])

    print(tex, " Generating indices")
    for sxd in glob.glob('*.sxd'):
        subprocess.call([songidx, '-b', bible, sxd])

    print(tex, " Pass 2")
    subprocess.call([pdflatex, tex])
