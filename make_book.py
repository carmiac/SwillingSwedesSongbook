import glob
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
subprocess.Popen("generate.bat -nopause")
        