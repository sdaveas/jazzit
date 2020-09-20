"""Handy Utilities."""

import os
import time
from playsound import playsound
from multiprocessing import Process

_current_dir, _ = os.path.split(__file__)
_flags = {}


def _track_length(track_path):
    """Get length of Track."""
    from mutagen.mp3 import MP3

    audio = MP3(track_path)
    return audio.info.length


def _get_track_path(track):
    """Get Track Path."""
    track_path = os.path.join(_current_dir, "tracks", track)
    if os.path.exists(track_path):
        return track_path
    else:
        return track


def _in_notebook():
    """Are you in a notebook ?."""
    try:
        in_notebook = _flags["in_notebook"]
    except KeyError:
        in_notebook = True
        try:
            from IPython import get_ipython

            if "IPKernelApp" not in get_ipython().config:  # pragma: no cover
                in_notebook = False
        except:
            in_notebook = False
        _flags["in_notebook"] = in_notebook
    return in_notebook


def _play_music(track_path):
    """Play Music in a loop."""
    while True:
        playsound(track_path)
        time.sleep(0.1)


def _start_music(track_path, loop=True):
    """Start Music."""
    if _in_notebook():
        from .jupyter.player import _start_music

        process = _start_music(track_path)
    else:
        process = Process(target=_play_music, args=(track_path,), daemon=True)
        process.start()
    return process


def _stop_music(process):
    """Stop Music."""
    if _in_notebook():
        from .jupyter.player import _stop_music

        _stop_music(process)
    else:
        process.terminate()
        process.join()
