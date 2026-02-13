# SwillingSwedesSongbook

This is a collection of songs from my days in the SCA at the College of St. Golias and since. It is a work in progress, and will be updated as I have time.

It is compiled from many sources into a series of XML files and a songbook template using my OpenLyrics Songbook Maker tool.

## View Online

**[Browse the songbook online](https://carmiac.github.io/SwillingSwedesSongbook/)** with our red and gold themed HTML version, or download PDFs for offline use!

If you want to be able to build it yourself, keep reading. The current version of the build system has been tested in Linux. It may work in MacOS and Windows, but I haven't tested it there.

**Prereqs**

- Python 3, from http://www.python.org
- Windows
  - MiKTeX, from http://www.miktex.org/
  - Complete songs package for LaTeX from http://songs.sourceforge.net/
- OSX
  - MacTeX, from http://www.tug.org/mactex/
- Linux
  - TeX Live, from http://www.tug.org/texlive/

**Building**

1. Install the OpenLyric Bookmaker package:

   ```bash
   pip install git+https://github.com/carmiac/openlyric_bookmaker.git
   ```

2. Build the songbook:

   ```bash
   cd SwillingSwedesSongbook
   openlyric_bookmaker --config book_config.toml
   ```

3. Sing with gusto!
