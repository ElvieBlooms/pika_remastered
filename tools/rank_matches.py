"""Rank candidate clips against each of Yellow's 42 Pikachu clips.

Scores how closely each candidate follows a Yellow clip's pitch movement, with
overall pitch and length as smaller factors. Loudness counts for little,
because Yellow's 1-bit clips don't keep it. No candidate is the same recording
as a Yellow clip (those come from the late-90s anime), so the result is a
shortlist for your ears. In a self-test with known clips crushed to 1-bit, the
right clip came out first about 7 times in 10.

    python3 rank_matches.py --originals YELLOW_DIR --source lgpe_ work/lgpe --out work/ranking.json
"""
# ------------------
import argparse
import json
import os
import sys
import warnings

import librosa
import numpy as np
import scipy.signal as sg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common  # noqa: E402

warnings.filterwarnings("ignore")  # librosa is noisy about short clips
RATE = 16000
HOP = 160  # 10 ms frames


def load(path):
    y, _ = librosa.load(path, sr=RATE, mono=True)
    # Keeps the voice band and drops most of the 1-bit hiss.
    b, a = sg.butter(4, [180 / (RATE / 2), 4500 / (RATE / 2)], btype="band")
    y = sg.filtfilt(b, a, y)
    y, _ = librosa.effects.trim(y, top_db=28, frame_length=512, hop_length=HOP)
    return y


def features(y):
    f0, _, _ = librosa.pyin(y, fmin=180, fmax=1600, sr=RATE, frame_length=1024, hop_length=HOP)
    semitones = 12 * np.log2(f0 / 440.0)
    rms = librosa.feature.rms(y=y, frame_length=512, hop_length=HOP)[0]
    loudness = librosa.amplitude_to_db(rms, ref=np.max(rms) + 1e-9)
    n = min(len(semitones), len(loudness))
    semitones, loudness = semitones[:n], loudness[:n]
    voiced = ~np.isnan(semitones)
    median = float(np.nanmedian(semitones)) if voiced.any() else 0.0
    # Unvoiced gaps are bridged so the pitch line has no holes.
    frames = np.arange(n)
    if voiced.sum() > 1:
        pitch = np.interp(frames, frames[voiced], semitones[voiced])
    else:
        pitch = np.full(n, median)
    return dict(length=len(y) / RATE, pitch=pitch, loudness=np.maximum(loudness, -40) / 40.0, median=median)


def contour_cost(a, b, shift, loudness_weight):
    # Dynamic time warping, so a slower or faster delivery still lines up.
    A = np.vstack([(a["pitch"] - shift) / 6.0, a["loudness"] * loudness_weight])
    B = np.vstack([b["pitch"] / 6.0, b["loudness"] * loudness_weight])
    D, path = librosa.sequence.dtw(X=A, Y=B, metric="euclidean", global_constraints=True, band_rad=0.3)
    return D[-1, -1] / len(path)


def compare(a, b, loudness_weight):
    ratio = max(a["length"], b["length"]) / max(1e-3, min(a["length"], b["length"]))
    gap = a["median"] - b["median"]
    # The pitch gap is removed first, so a higher or lower voice can still match.
    shape = contour_cost(a, b, gap, loudness_weight)
    score = shape + 0.35 * np.log2(ratio) + 0.03 * abs(gap)
    return dict(score=round(float(score), 4), shape=round(float(shape), 4),
                length_ratio=round(float(ratio), 3), pitch_gap_semitones=round(float(gap), 2))


def tier(candidates):
    best, ratio = candidates[0]["score"], candidates[0]["length_ratio"]
    margin = candidates[1]["score"] - best if len(candidates) > 1 else 1.0
    if best <= 0.25 and margin >= 0.08 and ratio <= 1.25:
        return "Strong"
    if best <= 0.30 and ratio <= 1.3:
        return "Possible"
    if best <= 0.45:
        return "Weak"
    return "None"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--originals", required=True, help="folder with Yellow's cry_NN.wav files")
    common.add_source_args(parser)
    parser.add_argument("--out", required=True)
    parser.add_argument("--top", type=int, default=8, help="candidates kept per slot (default 8)")
    parser.add_argument("--loudness-weight", type=float, default=0.2)
    args = parser.parse_args()

    yellow = common.yellow_clips(args.originals)
    candidates = common.index_sources(args.source)
    print(f"{len(yellow)} Yellow clips, {len(candidates)} candidates", file=sys.stderr)
    yellow_features = {slot: features(load(path)) for slot, path in yellow.items()}
    candidate_features = {}
    for i, (clip_id, path) in enumerate(candidates.items(), 1):
        candidate_features[clip_id] = features(load(path))
        if i % 50 == 0:
            print(f"  analysed {i}/{len(candidates)}", file=sys.stderr)

    slots = {}
    for slot, a in yellow_features.items():
        rows = [dict(id=clip_id, file=candidates[clip_id], **compare(a, b, args.loudness_weight))
                for clip_id, b in candidate_features.items()]
        rows.sort(key=lambda row: row["score"])
        top = rows[:args.top]
        slots[f"{slot:02d}"] = dict(played=slot in common.PLAYED, original=yellow[slot],
                                    original_length=round(a["length"], 3), tier=tier(top), candidates=top)

    with open(args.out, "w") as f:
        json.dump(dict(format=1, slots=slots), f, indent=1)
    print(f"wrote {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
