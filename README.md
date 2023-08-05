# SwillingSweedesSongbook

This is a songbook from my days in the SCA at the College of St. Golias.

It is compiled from many sources into the songs package for LaTeX, and includes some helper scripts to make it easily buildable.

If you just want the pdf's of the songbook, look in the pdf directory.

If you want to be able to build it yourself, keep reading. It is tested in Windows and OSX, and should work the same in Linux.

**Prereqs**

* Python 3, from http://www.python.org
* Windows
   * MiKTeX, from http://www.miktex.org/
   * Complete songs package for LaTeX from http://songs.sourceforge.net/
* OSX
   * MacTeX, from http://www.tug.org/mactex/
* Linux (untested, but it should work)
   * TeX Live, from http://www.tug.org/texlive/

**Building**

1. Clone
2. python makebook.py -i src/*.txt -d header.txt
3. Sing with gusto!
