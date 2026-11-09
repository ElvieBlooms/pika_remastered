"""Build the mod's assets/cries/cry_NN.ogg files from a picks recipe.

The recipe is JSON: {"picks": {"cry_01": {"clip": "<clip ID>"}, ...}}. Clip IDs
are found through --source, the same way rank_matches.py finds them. A slot
left out of the recipe gets no file, so the game keeps its own clip there.

Each clip has the silence at both ends trimmed (40 dB below its peak, 30 ms
kept either side), a 10 ms fade-out, and its peak held to -0.5 dBFS, then is
written as Ogg Vorbis at its own sample rate.

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
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

CEILING = 10 ** (-0.5 / 20)


def prepare(path):
    y, rate = librosa.load(path, sr=None, mono=True)
    _, (start, end) = librosa.effects.trim(y, top_db=40, frame_length=1024, hop_length=256)
    pad = int(0.03 * rate)
    y = y[max(0, start - pad):min(len(y), end + pad)].copy()
    # The fade stops a click where the trim cuts the tail.
    fade = min(len(y), int(0.01 * rate))
    if fade:
        y[-fade:] *= np.linspace(1, 0, fade)
    peak = float(np.abs(y).max()) if len(y) else 0.0
    if peak > CEILING:
        y *= CEILING / peak
    return y, rate


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("recipe")
    common.add_source_args(parser)
    parser.add_argument("--out", required=True, help="usually mod/pika_remastered/assets/cries")
    args = parser.parse_args()

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
        y, rate = prepare(clips[pick["clip"]])
        sf.write(os.path.join(args.out, f"{slot}.ogg"), y, rate, format="OGG", subtype="VORBIS")
        print(f"{slot}  {pick['clip']:<20} {len(y) / rate:.2f}s")


if __name__ == "__main__":
    main()
