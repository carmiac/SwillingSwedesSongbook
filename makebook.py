import glob
import os
import fileinput
import subprocess

song_glob = "src\*.txt"
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

# and then run the generator batch file
#subprocess.Popen("generate.bat -nopause")

# replacing generate.bat

# first, set up a bunch of paths for later
scripts = '..\src'
auxdir = 'temp'
songidx = '..\src\songidx'
sbdchk = '..\src\sbdchk'
miktexpath = 'C:\Program Files (x86)\MiKTeX 2.9'
miktexbin= os.sep.join([miktexpath,'miktex','bin'])

# next, get a list of .tex files to use
texfiles = sorted(glob.glob('*.tex'))
print(texfiles)
# then, regenerate all .tex files, all index files, then all .tex files again
for tex in texfiles:
    print(tex, " Pass 1")
    subprocess.call([os.sep.join([miktexbin, 'pdflatex.exe']), '='.join(['-aux-directory',auxdir]), tex])
    
    print(tex, " Generating indices")
    for idx in glob.glob(os.sep.join([auxdir, '*.sxd'])):
        subprocess.call([os.sep.join([songidx, 'songidx.exe']), '-b', os.sep.join([songidx, 'bible.can']), idx])
    
    print(tex, " Pass 2")
    subprocess.call([os.sep.join([miktexbin, 'pdflatex.exe']), '='.join(['-aux-directory',auxdir]), tex])    

        