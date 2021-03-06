#!/usr/bin/env python3

import glob
import os
import fileinput
import subprocess
import platform
import shutil
import argparse
import re
from collections import OrderedDict

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

def make_index(indexfile, bible):
    # create the outfile name
    outfile = os.path.splitext(indexfile)[0] + '.sbx'
    # open index_file
    with open(indexfile, 'r') as f:
        # determine type from first line
        type = f.readline().strip()
    # call indexer
    if type == 'AUTHOR INDEX DATA FILE':
        make_author_index(indexfile, outfile)
    elif type == 'TITLE INDEX DATA FILE':
        make_title_index(indexfile, outfile)
    elif type == 'SCRIPTURE INDEX DATA FILE':
        make_verse_index(indexfile, outfile, bible)
    else:
        print('{} : UNKNOWN file type : {}'.format(indexfile, type))

def _make_author_dictionary(infile):
    authors = {}
    # read each 3 line song entry
    with open(infile, 'r') as f:
        typeline = f.readline() # skip the first line that is just used for file typing
        while True:
            # read 3 line song entry, stripping excess whitespace
            author = f.readline().strip()
            songnum = f.readline().strip()
            link = f.readline().strip()
            if not link: break  # EOF
            # process list of authors into entry format
            # this may be ',' , 'and' and/or ';' delimited
            # '~' or '\ ' may have been used to replace spaces to prevent name breaking
            for name in [x for x in re.split(' and |[^a-zA-Z~. ]+', author.replace('\\ ','~')) if x != '']:
                try:
                    first, last = name.rsplit(maxsplit=1)
                except: # only one word in name
                    entry = name.replace('~', ' ').strip()
                else:
                    entry = ', '.join([last.strip(), first.strip()]).replace('~', ' ')
                # add to the dictionary
                # {'Doe, John': [{'num': '1', 'link': 'song1-1.1'}, etc...]}
                try:
                    authors[entry].append({'songnum': songnum, 'link': link})
                except KeyError:
                    authors[entry] = [{'songnum': songnum, 'link': link}]
    return authors

def make_author_index(infile, outfile):
    # get a dict of authors and their songs
    authors = _make_author_dictionary(infile)

    # setup some formatting string constants
    beginsection = '\\begin{{idxblock}}{{}}\n'
    endsection = '\\end{{idxblock}}\n'
    auth_entry = '\\idxentry{{{author}}}{{'
    song_entry = '\\songlink{{{link}}}{{{songnum}}}'

    # write the author index
    with open(outfile, 'w') as f:
        f.write(beginsection.format())
        for author in sorted(authors, key=str.casefold):
            # write author entry
            f.write(auth_entry.format(author = author))
            # write first song entry
            songs = authors[author]
            songs.sort(key = lambda k: int(k['songnum']))
            f.write(song_entry.format(songnum = songs[0]['songnum'], link = songs[0]['link']))
            # write subsequent song entries
            for song in songs[1:]:
                f.write('\\\\')
                f.write(song_entry.format(songnum = song['songnum'], link = song['link']))
            # and end the line
            f.write('}\n')
        f.write(endsection.format())

def _make_title_list(infile):
    titles = []
    with open(infile, 'r') as f:
        typeline = f.readline() # skip the first line that is just used for file typing
        while True:
            # read 3 line song entry, stripping excess whitespace
            title = f.readline().strip()
            songnum = f.readline().strip()
            link = f.readline().strip()
            if not link: break  # EOF
            # if the song title begins with a '*', remove it and set 'alt' = True
            if title.startswith('*'):
                title = title.lstrip('*')
                alt = True
            else:
                alt = False
            # move beginning 'a', 'an', and 'the' to the end of the title and remove leading whitespace
            try:
                begin, end = title.split(maxsplit=1)
            except ValueError: # only one word in title
                pass
            else:
                if begin in ['a', 'an', 'the', 'A', 'An', 'The']:
                    title = ', '.join([end, begin])
            # capitalize just the first letter of the first word
            title = title[0].upper() + title[1:]
            # make into a dictionary and add the song to the song list
            titles.append({'title': title, 'songnum': songnum, 'link': link, 'alt':alt})

    return titles

def make_title_index(infile, outfile, letterblock = True):
    # get the list of song titles and sort it
    titles = _make_title_list(infile)
    titles.sort(key=lambda k: k['title'].casefold())

    # setup some formatting string constants
    beginsection = '\\begin{{idxblock}}{{{}}}\n'
    endsection = '\\end{{idxblock}}\n'
    entry = '\\{linktype}{{{title}}}{{\\songlink{{{link}}}{{{songnum}}}}}\n'

    # write out the index file
    with open(outfile, 'w') as f:
        if letterblock:
            section = titles[0]['title'][0]
            f.write(beginsection.format(section))
        for song in titles:
            if letterblock: # check for a new index section
                if song['title'][0].casefold() != section.casefold():
                    f.write(endsection.format()) # close out old block
                    section = song['title'][0].upper()
                    f.write(beginsection.format(section))
            if song['alt']: # check for alternate title
                linktype = 'idxaltentry'
            else:
                linktype = 'idxentry'
            f.write(entry.format(
                linktype = linktype,
                title = song['title'],
                link = song['link'],
                songnum = song['songnum']))
        if letterblock:
            f.write(endsection.format()) # close out final block

def _make_book_dictionary(infile, bible):
    # parse bible into an ordered dictionary of books
    books = OrderedDict()
    altnames = {} #
    for line in fileinput.input(bible):
        # skip lines beginning with '#' or '0'
        if(line[0] not in ['#', '0']):
            # split along the | symbol, and only use the first one
            try:
                name, *alt = line.split('|')
            except ValueError:
                name = line.strip()
            else:
                for each in alt:
                    altnames[each.strip()] = name.strip()
            books[name.strip()] = []
    # process infile:
    with open(infile, 'r') as f:
        typeline = f.readline() # skip the first line that is just used for file typing
        while True:
            # read 3 line song entry, stripping excess whitespace
            verses = f.readline().strip()
            songnum = f.readline().strip()
            link = f.readline().strip()
            if not link: break  # EOF
            # split verses by semicolon
            for verse in verses.split(';'):
                # split into book and verse list
                try:
                    b, v = verse.strip().rsplit(maxsplit=1)
                except ValueError:
                    v = verse.strip()
                # add song verse list, songnum and link as additional entry for book
                if b in altnames:
                    b = altnames[b]
                books[b].append({'verses': v, 'songnum': songnum, 'link': link})
    return books

def make_verse_index(infile, outfile, bible):
    books = _make_book_dictionary(infile, bible)

    beginsection = '\\begin{{idxblock}}{{{}}}\n'
    endsection = '\\end{{idxblock}}\n'
    entry = '\\idxentry{{{verse}}}{{\\songlink{{{link}}}{{{songnum}}}}}\n'
    # write out the index file
    with open(outfile, 'w') as f:
        for b in [x for x in books if len(books[x]) > 0]:
            # write beginning block
            f.write(beginsection.format(b))
            # write each song entry
            for song in sorted(books[b], key = lambda k: int(k['verses'].split(':')[0])):
                f.write(entry.format(verse = song['verses'], songnum = song['songnum'], link = song['link']))
            # write end block
            f.write(endsection.format())

if __name__ == "__main__":

    # create the argument parser and config defaults
    parser = argparse.ArgumentParser(description="Makes songbooks based on tex files")
    parser.add_argument("-i", "--infile", nargs='*', default=['songs.sbd'], help="Song file(s) to include, wildcards supported. ( default %(default)s)")
    parser.add_argument("-d", "--header", default='', help="Header for the entire songbook (default %(default)s)")
    parser.add_argument("-b", "--bible", default='bible.can', help="Location of bible file (default %(default)s)")
    parser.add_argument("-t", "--tex", nargs='*', default=['*.tex'], help="tex file(s) to process, wildcards supported. (default %(default)s)")
    parser.add_argument("-p", "--pdflatex", default='pdflatex', help="command to call pdflatex (default %(default)s )")
    parser.add_argument("-o", "--outfile", default = 'songs.sbd', help="File of songs created from infile(s) and referenced in tex files. If infile = outfile, the header is not used. (default %(default)s)")
    parser.add_argument("-s", "--sort", default=True, help="sort the list of infiles (default %(default)s)")
    args = parser.parse_args()

    # make the working song file
    infiles = [item for sublist in [glob.glob(x) for x in args.infile] for item in sublist]
    if infiles[0] != args.outfile:
        make_songfile(infiles, args.outfile, args.header, args.sort)

    # process all tex files to generate indexed pdfs
    texfiles = [item for sublist in [glob.glob(x) for x in args.tex] for item in sublist]
    for tex in texfiles:
        subprocess.call([args.pdflatex, tex])
        for sxd in glob.glob('*.sxd'):
            make_index(sxd, args.bible)
        subprocess.call([args.pdflatex, tex])
