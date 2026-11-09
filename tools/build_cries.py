"""Build the mod's assets/cries/cry_NN.ogg files from a picks recipe.

The recipe is JSON: {"picks": {"cry_01": {"clip": "<clip ID>"}, ...}}. Clip IDs
are found through --source, the same way rank_matches.py finds them. A slot
left out of the recipe gets no file, so the game keeps its own clip there.

Each clip has the silence at both ends trimmed (40 dB below its peak, 30 ms
kept either side) and a 10 ms fade-out. It's then raised to --loudness (-9 LUFS
by default), with a limiter holding peaks at -1 dBFS, and written as Ogg Vorbis
at its own sample rate. Yellow's 1-bit clips are about as loud as audio gets, and
the engine scales Pikachu by the SFX volume too, so clips mixed like normal
voice lines end up far too quiet without this. --loudness off skips it.

    python3 build_cries.py recipes/pikachu.recipe.json --source lgpe_ work/lgpe \\
      --out mod/pika_remastered/assets/cries
"""
# ------------------
import argparse
import json
import os
import re
import sys

import librosa
import numpy as np
import pyloudnorm
import soundfile as sf
from scipy.ndimage import minimum_filter1d

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

CEILING_DB = -1.0
LOOKAHEAD_MS = 5
RELEASE_MS = 60


def loudness(y, rate):
    # The meter needs 400 ms, so short clips are padded with silence.
    short = int(0.4 * rate) - len(y)
    if short > 0:
        y = np.concatenate([y, np.zeros(short)])
    return pyloudnorm.Meter(rate).integrated_loudness(y)


def limit(y, rate):
    """Hold peaks at CEILING_DB, turning down only around each peak."""
    ceiling = 10 ** (CEILING_DB / 20)
    needed = np.minimum(1.0, ceiling / np.maximum(np.abs(y), 1e-9))
    # Looking ahead lets the gain drop before a peak arrives, not on it.
    reach = max(1, int(rate * LOOKAHEAD_MS / 1000))
    gain = minimum_filter1d(needed, size=2 * reach + 1)
    # Gain drops at once and recovers smoothly, so there's no pumping.
    recover = np.exp(-1.0 / (rate * RELEASE_MS / 1000))
    smooth = np.empty_like(gain)
    level = 1.0
    for i, g in enumerate(gain):
        level = g if g < level else recover * level + (1 - recover) * g
        smooth[i] = level
    return y * np.minimum(smooth, gain)


def prepare(path, target):
    y, rate = librosa.load(path, sr=None, mono=True)
    _, (start, end) = librosa.effects.trim(y, top_db=40, frame_length=1024, hop_length=256)
    pad = int(0.03 * rate)
    y = y[max(0, start - pad):min(len(y), end + pad)].copy()
    # The fade stops a click where the trim cuts the tail.
    fade = min(len(y), int(0.01 * rate))
    if fade:
        y[-fade:] *= np.linspace(1, 0, fade)
    if target is not None and len(y):
        y = limit(y * 10 ** ((target - loudness(y, rate)) / 20), rate)
    return y, rate


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("recipe")
    common.add_source_args(parser)
    parser.add_argument("--out", required=True, help="usually mod/pika_remastered/assets/cries")
    parser.add_argument("--loudness", default="-9",
                        help="target loudness in LUFS (default -9), or 'off' to keep each clip's own level")
    args = parser.parse_args()

    if args.loudness.lower() == "off":
        target = None
    else:
        try:
            target = float(args.loudness)
        except ValueError:
            raise SystemExit(f"--loudness takes a number in LUFS or 'off', not {args.loudness!r}")

    picks = json.load(open(args.recipe))["picks"]
    clips = common.index_sources(args.source)

    # Checked up front, so a bad recipe writes nothing.
    for slot in picks:
        if not re.fullmatch(r"cry_\d\d", slot) or not 1 <= int(slot[4:]) <= common.SLOT_COUNT:
            raise SystemExit(f"{slot!r} isn't a slot; use cry_01 to cry_{common.SLOT_COUNT}")
    missing = sorted({pick["clip"] for pick in picks.values()} - clips.keys())
    if missing:
        raise SystemExit("no --source has these clips: " + ", ".join(missing))

    os.makedirs(args.out, exist_ok=True)
    for slot, pick in sorted(picks.items()):
        y, rate = prepare(clips[pick["clip"]], target)
        sf.write(os.path.join(args.out, f"{slot}.ogg"), y, rate, format="OGG", subtype="VORBIS")
        print(f"{slot}  {pick['clip']:<20} {len(y) / rate:.2f}s  {loudness(y, rate):.1f} LUFS")


if __name__ == "__main__":
    main()
