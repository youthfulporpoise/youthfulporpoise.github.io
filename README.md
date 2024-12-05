# Achezhuth Shaala

## Basic Details
**Team Name**: *Singularity* 

### Team Members
- Hathim Ali K. H., GECI
- Dalia Susan Thomas, GECI
- Nidhin Gireesh, GECI

### Project Description
A *living* keyboard that humorously evaluates your attempt to type Malayalam
poetry in Manglish — so you grow to type ever faster these classic poems in a
form no one will ever read.  At least you had fun, right?

### The Grand Problem
I feel a tangible absence of a program, that teaches someone to type faster
Manglish poetry, in the space-time fabric.  Don't you feel it too?

### The Grand Solution
This abomination.

## Technical Details
Languages: Python 3.12

Packages used:
- `sshkeyboard` to read keystrokes
- `colorama` for a better interface to manage terminal colors
- `pygame.mixer` for playing audio samples
- `yaml` to parse typing test contents

The aim is to create a typing speed tester that throws snarky remarks when the
user makes a mistake or types too slow.  This is a barebones implementation.
Only the classic terminal interface is guaranteed to work.  The web interface
currently does not work due limitations in PyScript framework (and Pyodide) not
supporting standard python modules such as `fcntl`.

# Installation
There are no installations.  Clone this repository.  Install the dependencies.
~~~
python3 -m pip install pygame sshkeyboard colorama
~~~
`yaml` is shipped with the official Python installation.

# Run
~~~
python main.py
~~~

# There’s One Thing
Our program will reluctantly appreciate *you*, if you can achieve at least 50
WPM with at least 90% accuracy.  If you want to take on the challenge, more
power to you!

# Project Documentation

## Screenshots
*Screenshots will be coming soon.*
you
## Team Contributions
- Dalia Susan Thomas: transliteration of Malayalam into Manglish; editing of
  audio cuts;
- Nidhin Gireesh: curation of poems; curation of audio cuts;
- Hathim Ali: program implementation
