# Lexend expansion project
History: Began as expansion of the existing family of styles into an OT1.8 weight axis (wght) for design use. 
Additional work was then done to add this variable font with a wght axis to a variable version of the Lexend width axis. 
Arabic is being added to the glyph repertoire in a separate effort. 

The original Lexend project started by Bonnie Shaver-Troup and Thomas Jockin in 2018 [https://github.com/ThomasJockin/lexend](https://github.com/ThomasJockin/lexend)

## Axis

- Weight (wght) ranges from 100 to 800
- LXND (LXND) ranges from 0 to 1
- XTRA (XTRA) measures 'H's counter space as width’s reference, ranges form 349 to 489, dissected from original LXND axis
- SPAC (SPAC) measures spacing in percentage, ranges from 100 to 125, , dissected from original LXND axis

Notes:
- wght 400 is now more appropriate for body text. Former Regular is wght 500.
- experimental SPACE and XTRA axes, the "dissected" ingredients of the original LXND axes, are in /sources 


## Install

    # Create a new virtualenv
    virtualenv env
    # Activate env
    source env/bin/activate
    # Install dependencies
    pip install .
    pip install -r requirements.txt

## Generate

    sh sources/build.sh

