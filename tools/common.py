"""Shared pieces for the Pika Remastered tools.

Yellow's slot facts, and the --source rule that turns folders of clips into
clip IDs like lgpe_102097674 or swsh_PM025_42. Recipes and rankings use those
IDs, so every tool reads sources the same way.
"""
# ------------------
import glob
import os
import re

SLOT_COUNT = 42

# Slots engine 0.4.0 plays (docs/CLIP_GUIDE.md). The other 16 are on the cart but never called.
PLAYED = {1, 2, 3, 4, 5, 6, 9, 10, 11, 13, 15, 18, 19, 20, 25, 26, 28, 29, 31,
          33, 34, 35, 37, 38, 39, 40}

AUDIO_EXTS = (".wav", ".ogg", ".mp3", ".flac")

SOURCE_HELP = (
    "Clip source: PREFIX DIR [GLOB [REGEX]]. A clip's ID is PREFIX plus its file "
    "name, or PREFIX plus REGEX group 1. Repeat for each source, e.g. "
    "--source swsh_ ./swsh 'Play_PV_025_00_00*.ogg' '(PM025_\\d+)'")


def add_source_args(parser):
    parser.add_argument("--source", nargs="+", action="append", metavar="ARG",
                        required=True, help=SOURCE_HELP)


def _parse(specs):
    for spec in specs:
        if not 2 <= len(spec) <= 4:
            raise SystemExit(f"--source needs PREFIX DIR [GLOB [REGEX]], got {spec}")
        prefix, folder = spec[0], spec[1]
        pattern = spec[2] if len(spec) > 2 else "*"
        regex = re.compile(spec[3]) if len(spec) > 3 else None
        yield prefix, folder, pattern, regex


def index_sources(specs):
    """Map every clip ID the --source specs describe to its file."""
    clips = {}
    for prefix, folder, pattern, regex in _parse(specs):
        for path in sorted(glob.glob(os.path.join(folder, pattern))):
            if not path.lower().endswith(AUDIO_EXTS):
                continue
            name = os.path.splitext(os.path.basename(path))[0]
            if regex:
                match = regex.search(name)
                if not match:
                    continue
                name = match.group(1)
            clip_id = prefix + name
            # Two files with one ID would make recipes ambiguous.
            if clip_id in clips:
                raise SystemExit(f"two files share the clip ID {clip_id}: {clips[clip_id]} and {path}")
            clips[clip_id] = path
    return clips


def yellow_clips(folder):
    """Map slot number to Yellow's cry_NN.wav, searching subfolders too."""
    clips = {}
    for path in glob.glob(os.path.join(folder, "**", "cry_*.wav"), recursive=True):
        match = re.search(r"cry_(\d+)\.wav$", path)
        if match:
            clips[int(match.group(1))] = path
    return dict(sorted(clips.items()))
