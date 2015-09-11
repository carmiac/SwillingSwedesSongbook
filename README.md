# SwillingSweedesSongbook

This is a songbook from my days in the SCA at the College of St. Golias.

It is compilied from many sources into the songs package for LaTeX, and includes some helper scripts to make it easily buildable.

If you just want the pdf's of the songbook, look in the pdf directory.

If you want to be able to build it yourself, keep reading. It it tested in Windows and OSX, and should work the same in Linux.

**Prereqs**

* Python 3, from http://www.python.org
* Songs package for LaTeX from http://songs.sourceforge.net/
    * And its prereqs, described on the Downloads page
    * Install songs in single user mode
    
**Building**
1) Clone into the top songs directory, alongside ./src and ./Sample 
2) python makebook.py
3) Sing with gusto!