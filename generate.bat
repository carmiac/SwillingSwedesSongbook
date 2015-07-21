@REM Copyright (C) 2013 Kevin W. Hamlen
@REM
@REM This program is free software; you can redistribute it and/or
@REM modify it under the terms of the GNU General Public License
@REM as published by the Free Software Foundation; either version 2
@REM of the License, or (at your option) any later version.
@REM
@REM This program is distributed in the hope that it will be useful,
@REM but WITHOUT ANY WARRANTY; without even the implied warranty of
@REM MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
@REM GNU General Public License for more details.
@REM
@REM You should have received a copy of the GNU General Public License
@REM along with this program; if not, write to the Free Software
@REM Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
@REM MA  02110-1301, USA.
@REM
@REM The latest version of this program can be obtained from
@REM http://songs.sourceforge.net.
@REM
@ECHO off

SET scripts=..\src
SET auxdir=temp
SET songidx=..\src\songidx
SET sbdchk=..\src\sbdchk
CALL "%scripts%\paths.bat"

@REM Launch the sbdchk hyphenation-checker, if requested:
IF NOT "%1"=="sbdcheck" GOTO MAIN
IF NOT "%cmdextversion%"=="" GOTO SBDCHK
@ECHO Error: The sbdchk feature requires MS-DOS Command Extensions
@ECHO (available in MS-DOS for Windows NT/2000 and later).
GOTO DONE
:SBDCHK
SET filespec=%2
IF "%filespec%"=="" SET filespec=*.sbd
FOR %%I IN (%filespec%) DO (
  IF NOT "%%~xI"==".sbd~" (
    @ECHO.
    @ECHO Checking placement of chords in %%I...
    @ECHO -----------------------------------------------
    "%sbdchk%\sbdchk.exe" -x %%I "%auxdir%\%%~nI.tex"
    IF ERRORLEVEL 1 GOTO FAILED
    "%miktexbin%\pdflatex.exe" -aux-directory="%auxdir%" "%auxdir%\%%~nI.tex"
    IF ERRORLEVEL 1 GOTO FAILED
    "%sbdchk%\sbdchk.exe" -r "%auxdir%\%%~nI.log" ".\%%~nI.hyp"
    IF ERRORLEVEL 1 GOTO FAILED
  )
)
@ECHO.
@ECHO Completed successfully!
GOTO NOPAUSE

@REM Before regenerating the book, verify that .pdf files are writable:
:MAIN
SET hasfile=0
FOR %%I IN (*.pdf) DO SET hasfile=1
IF %hasfile%==0 @GOTO COMPILE
REN *.pdf *.p~f
IF NOT ERRORLEVEL 1 GOTO FIXPDF
REN *.p~f *.pdf
@ECHO                                   ------
@ECHO Some PDF files cannot be regenerated because another program (probably Adobe
@ECHO Acrobat Reader) is currently accessing them. Please close that program first
@ECHO and then try again.
GOTO DONE
:FIXPDF
REN *.p~f *.pdf

@REM Regenerate all .tex files, all index files, then all .tex files again:
:COMPILE
SET filespec=%1
IF "%filespec%"=="-nopause" SET filespec=%2
IF "%filespec%"=="" SET filespec=*.tex
FOR %%I IN (%filespec%) DO (
  @CALL "%scripts%\miktex.bat" "%%I" "%auxdir%" 1
  @IF ERRORLEVEL 1 GOTO FAILED
)
@ECHO.
@ECHO Regenerating Indexes
@ECHO --------------------
FOR %%I IN ("%auxdir%\*.sxd") DO (
  "%songidx%\songidx.exe" -b "%songidx%\bible.can" %%I
  IF ERRORLEVEL 1 GOTO FAILED
)
FOR %%I IN (%filespec%) DO (
  CALL "%scripts%\miktex.bat" "%%I" "%auxdir%" 2
  IF ERRORLEVEL 1 GOTO FAILED
)
@ECHO.
@ECHO Completed successfully!
IF "%1"=="-nopause" EXIT
GOTO DONE

:FAILED
@ECHO.

:DONE
@PAUSE

:NOPAUSE
