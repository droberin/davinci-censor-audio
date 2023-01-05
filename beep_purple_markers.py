#!/usr/bin/env python
"""
Author: Roberto Salgado
Email: drober plus davinci at gmail dot com
Purpose: Mark censoring points in "Main timeline using Purple markers", run this script... and create a timeline with
    beeping tracks at markers' frame.
"""

import sys

def GetResolve():
    try:
    # The PYTHONPATH needs to be set correctly for this import statement to work.
    # An alternative is to import the DaVinciResolveScript by specifying absolute path (see ExceptionHandler logic)
        import DaVinciResolveScript as bmd
    except ImportError:
        if sys.platform.startswith("darwin"):
            expectedPath="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules/"
        elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            import os
            expectedPath=os.getenv('PROGRAMDATA') + "\\Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules\\"
        elif sys.platform.startswith("linux"):
            expectedPath="/opt/resolve/libs/Fusion/Modules/"

        # check if the default path has it...
        print("Unable to find module DaVinciResolveScript from $PYTHONPATH - trying default locations")
        try:
            import imp
            bmd = imp.load_source('DaVinciResolveScript', expectedPath+"DaVinciResolveScript.py")
        except ImportError:
            # No fallbacks ... report error:
            print("Unable to find module DaVinciResolveScript - please ensure that the module DaVinciResolveScript is discoverable by python")
            print("For a default DaVinci Resolve installation, the module is expected to be located in: "+expectedPath)
            sys.exit()

    return bmd.scriptapp("Resolve")



resolve = GetResolve()
projectManager = resolve.GetProjectManager()
project = projectManager.GetCurrentProject()
timeline = project.GetCurrentTimeline()


def go_to_edit():
    resolve.OpenPage("Edit")


def get_censoring_markers(timeline):
    markers = timeline.GetMarkers()
    censoring_frames = list()
    for marker in markers:
        marker_data = markers[marker]
        if marker_data['color'].lower() == "purple":
            censoring_frames.append(marker)
            print(f"Found censorship request at frame: {marker}")
    print(f"Total censor point found: {len(censoring_frames)}")
    return censoring_frames


def construct_censoring_frames_data(censoring_frames, initial_position=216000, track_index=1):
    beeping_elements = list()
    for marker in censoring_frames:
        insertion_clip = {
            "mediaPoolItem": beep_file,
            "startFrame": 0,
            "endFrame": 20,
            "recordFrame": initial_position + marker - 5,
            "trackIndex": track_index
        }
        print(insertion_clip)
        beeping_elements.append(insertion_clip)
    return beeping_elements


censoring_markers = get_censoring_markers(timeline)

if len(censoring_markers) < 1:
    print("No censoring points found. exiting.")
    sys.exit()

media_pool = project.GetMediaPool()
sub_folders = media_pool.GetRootFolder().GetSubFolders()
censoring_folder_found = False
censoring_sub_folder = None
for folder in sub_folders:
    if sub_folders[folder].GetName() == "censoring":
        censoring_folder_found = True
        censoring_sub_folder = sub_folders[folder]
        break

if not censoring_folder_found:
    print("Censoring SubFolder not found. Creating it...")
    censoring_sub_folder = media_pool.AddSubFolder(media_pool.GetRootFolder(), "censoring")
else:
    print("Censoring SubFolder found. Skipping creation...")

clips = censoring_sub_folder.GetClips()
beep_file = None
for clip in clips:
    clip_name = clips[clip].GetName()
    print(clip_name)
    if clip_name == "beep.mp3":
        print("Beep Found!")
        beep_file = clips[clip]
        break
if beep_file is None:
    print("Beep file not found. Copy a beep.mp3 in 'censoring' sub folder.")
    sys.exit()

go_to_edit()

audio_track = int(project.GetCurrentTimeline().GetTrackCount("audio") + 1)
initial_frame_project = project.GetCurrentTimeline().GetCurrentVideoItem().GetStart()
censoring_data_elements = construct_censoring_frames_data(censoring_markers, initial_frame_project, audio_track)

media_pool.AppendToTimeline(censoring_data_elements)
