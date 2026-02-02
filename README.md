# SwillingSwedesSongbook

This is a collection of songs from my days in the SCA at the College of St. Golias and since. It is a work in progress, and will be updated as I have time.

It is compiled from many sources into a series of XML files and a songbook template using my OpenLyrics Songbook Maker tool.

## 🌐 View Online

**[Browse the songbook online](https://carmiac.github.io/SwillingSwedesSongbook/)** with our red and gold themed HTML version, or download PDFs for offline use!

If you want to be able to build it yourself, keep reading. The current version of the build system has been tested in Linux.  It may work in MacOS and Windows, but I haven't tested it there.

**Prereqs**

* Python 3, from http://www.python.org
* Windows
   * MiKTeX, from http://www.miktex.org/
   * Complete songs package for LaTeX from http://songs.sourceforge.net/
* OSX
   * MacTeX, from http://www.tug.org/mactex/
* Linux
   * TeX Live, from http://www.tug.org/texlive/

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

Output files will be in `output/` directory (PDF and HTML versions).

## GitHub Pages Deployment

This repository is configured with GitHub Actions to automatically build and deploy the songbook when changes are pushed to the `main` branch.

### First-Time Setup

To enable GitHub Pages deployment:

1. Go to your repository Settings > Pages
2. Under "Source", select "GitHub Actions"
3. The workflow will automatically deploy on the next push to `main`

The deployed site will be available at: `https://carmiac.github.io/SwillingSwedesSongbook/`

### What Gets Deployed

- **HTML Songbook**: Interactive version with red and gold theme
- **PDF Downloads**: All three PDF versions (Bound Print, Display, eReader)
- **Landing Page**: A downloads page with links to all resources

### Manual Deployment

You can also trigger a manual deployment:

1. Go to Actions tab in your repository
2. Select "Build and Deploy Songbook" workflow
3. Click "Run workflow" button

## Customization

### HTML Theme

The HTML version uses a custom red and gold color scheme defined in `stylesheets/custom-theme.css`. You can modify this file to change colors, fonts, and styling.
