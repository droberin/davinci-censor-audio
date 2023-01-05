# davinci-censor-audio
Python Script to add censor track (beep) on a timeline in DaVinci Resolve Studio 18.1

## Usage
* Add a shortcut for Edit view to Add Marker in Purple colour.
* Finish your composition and editing
* Play the gig and use your shortcut to add markers at censor point in the timeline, no need to stop playing
* Move slightly those markers if needed
* Run Script from Workspace -> Scripts
* Carefully rerun if needed, it will create a new track on every run.

## Video example Usage
https://youtu.be/LBVSGMBkoMo (no audio)

## WARNINGS
* It will look for a file "beep.mp3" (not valid if you rename it through DaVinci) in "censoring" subfolder of the project.
* Subfolder would be created if not found while running the script.
* Audio track will probably be stereo by default, if you beep is mono, change track to mono after generating the track
