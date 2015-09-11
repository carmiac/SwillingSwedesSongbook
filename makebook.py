#!/usr/bin/env python3

import glob
import os
import fileinput
import subprocess
import platform
import shutil

## first, set up some paths for later
# where to find the individual song files
song_glob = os.sep.join(['src','*.txt']) 
# header for the entire songbook
sbd_header = "header.txt" 
# name of the sorted song file
sbd_out = "songs.sbd"
# some os specific paths
if platform.system() == 'Windows':
    songidx = '..\src\songidx\songidx.exe'
    bible = '..\src\songidx\bible.can'
    pdflatex = os.sep.join(['C:\Program Files (x86)\MiKTeX 2.9','miktex','bin', 'pdflatex.exe'])
    auxdir = 'temp'
    auxcmd = '='.join(['-aux-directory', auxdir])
    if not os.path.exists(auxdir):
        os.makedirs(auxdir)
else: # must be *nix
    songidx = '../src/songidx/songidx'
    bible = '../src/songidx/bible.can'
    pdflatex = 'pdflatex'
    auxdir = '.'
    auxcmd = ''
    # copy over the songs style file 
    shutil.copy2('../src/songs/songs.sty', './songs.sty')

# get the list of song files and sort them
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
texfiles = glob.glob('*.tex')

# process all .tex files, all index files, then all .tex files again
for tex in texfiles:
    print(tex, " Pass 1")
    subprocess.call([pdflatex, auxcmd, tex])
    print(tex, " Generating indices")
    for sxd in glob.glob(os.sep.join([auxdir, '*.sxd'])):
        subprocess.call([songidx, '-b', bible, sxd])
    print(tex, " Pass 2")
    subprocess.call([pdflatex, auxcmd, tex])
