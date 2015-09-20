#!/usr/bin/env python3

import glob
import os
import fileinput
import subprocess
import platform
import shutil
import argparse

# create the song file, with optional header and sorting
def make_songfile(infiles, outfile, header = False, sort = False):
    if sort:
        infiles.sort()
    with open(outfile, 'w') as fout:
        # add the header boilerplate
        if header:
            for line in fileinput.input(header):
                fout.write(line)
        # add the individual files
        for line in fileinput.input(infiles):
            fout.write(line)

# process all tex files to generate indexed pdfs
def process_tex(texfiles, pdflatex = 'pdflatex' , bible = ''):
    for tex in texfiles:
        print(tex, " Pass 1")
        subprocess.call([pdflatex, tex])
        print(tex, " Generating indices")
        for sxd in glob.glob('*.sxd'):
            subprocess.call([songidx, '-b', bible, sxd])
        print(tex, " Pass 2")
        subprocess.call([pdflatex, tex])

# def make_indices(index_files):
#     # for f in index_files:
#         # open f
#         # determine type
#         # call indexer
#
#     pass
#
# def make_author_index(infile, outfile, letter_block = True):
#     # read each 3 line song entry in to a dictionary
#     # {'John Doe': [{'num': '1', 'link': 'song1-1.1'}, etc...]}
#     # making multiple entires if there are multiple authors
#
#     # process authors names
#     # lastname, all other names
#     # but use the '~' to join names into one big one
#     # and capitalize the first letter of the last name
#
#     # open outfile
#     # for each author in dictionary, sorted
#         # if letter_block
#             # if author has a new starting letter
#                 # write new letter index line
#         # write author index line
#
#
# def make_title_index(infile, outfile, letter_block = True):
#     # create an empty song list
#
#     # read each 3 line song entry in sxd to a dictionaries
#     # with the keys 'title', 'num', 'link', 'alt'
#     # eg {'title': 'Some Song', 'num': '1', 'link', 'song1-1.1', 'alt': False}
#
#     # if the song title begins with a '*', remove it and set 'alt' = True
#
#     # move beginning 'a', 'an', and 'the' to the end of the title and remove leading whitespace
#
#     # capitalize the first letter of the first title word, after everything else is done
#
#     #and add the song to the song list
#
#     # open outfile
#     # for each song in list, sorted by title
#         # if letter_block
#             # if song has a new starting letter
#                 # write new letter index line
#         # if alt
#             # write alt entry line
#         # else
#             # write normal entry line
#
#
# def make_verse_index(infile, outfile, bible):
#     pass
#

if __name__ == "__main__":
    # some os specific things
    if platform.system() == 'Windows':
        pdflatex = os.sep.join(['C:\Program Files (x86)\MiKTeX 2.9','miktex','bin', 'pdflatex.exe'])
        songidx = '..\src\songidx\songidx.exe'
    else: # must be *nix
        songidx = '../src/songidx/songidx'
        pdflatex = 'pdflatex'
        # copy over the songs style file
        shutil.copy2('../src/songs/songs.sty', './songs.sty')

    # create the argument parser and config defaults
    parser = argparse.ArgumentParser(description="Makes songbooks based on tex files")
    parser.add_argument("-i", "--infile", nargs='*', default=[os.sep.join(['src','*.txt'])], help="Song file(s) to include, wildcards supported. ( default %(default)s)")
    parser.add_argument("-d", "--header", default='header.txt', help="Header for the entire songbook (default %(default)s)")
    parser.add_argument("-b", "--bible", default=os.sep.join(['..','src','songidx','bible.can']), help="Location of bible file (default %(default)s)")
    parser.add_argument("-t", "--tex", nargs='*', default=['*.tex'], help="tex file(s) to process, wildcards supported. (default %(default)s)")
    parser.add_argument("-p", "--pdflatex", default=pdflatex, help="command to call pdflatex (default %(default)s )")
    parser.add_argument("-o", "--outfile", default = 'songs.sbd', help="File of songs created from infile(s) and referenced in tex files. Must not be the same as infile. (default %(default)s)")
    parser.add_argument("-s", "--sort", default=True, help="sort the list of infiles (default %(default)s)")
    args = parser.parse_args()

    # make the working song file
    infiles = []
    for each in args.infile:
        infiles.extend(glob.glob(each))
    make_songfile(infiles, args.outfile, args.header, args.sort)

    # make the songbooks
    texfiles = []
    for each in args.tex:
        texfiles.extend(glob.glob(each))
    process_tex(texfiles, args.pdflatex, args.bible)


