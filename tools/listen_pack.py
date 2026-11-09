"""Build a folder per slot for listening side by side.

Each OUT_DIR/{played,unused}/slot_NN/ gets Yellow's clip as 0_yellow_cry_NN.wav,
then the closest candidates as 1_<id>, 2_<id> and so on. MATCHES.md lists every
slot by match strength, played slots first. Files are copied, never changed.

    python3 listen_pack.py work/ranking.json work/listen
"""
# ------------------
import argparse
import json
import os
import shutil

TIER_ORDER = {"Strong": 0, "Possible": 1, "Weak": 2, "None": 3}

INTRO = """# Closest matches

Each `slot_NN` folder holds Yellow's clip (`0_...`) and the closest candidates, closest
first. A strong match means a similar delivery, not the same recording, so pick by ear.

**Strong:** clearly closer than the runner-up. **Possible:** close, with near-ties.
**Weak:** a rough fit. **None:** nothing fits.
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("ranking", help="JSON from rank_matches.py")
    parser.add_argument("out_dir")
    parser.add_argument("--top", type=int, default=4, help="candidates per slot (default 4)")
    args = parser.parse_args()

    slots = json.load(open(args.ranking))["slots"]
    rows = []
    for key, slot in slots.items():
        group = "played" if slot["played"] else "unused"
        folder = os.path.join(args.out_dir, group, f"slot_{key}")
        os.makedirs(folder, exist_ok=True)
        shutil.copy(slot["original"], os.path.join(folder, f"0_yellow_cry_{key}.wav"))
        ids = []
        for i, candidate in enumerate(slot["candidates"][:args.top], 1):
            ext = os.path.splitext(candidate["file"])[1]
            shutil.copy(candidate["file"], os.path.join(folder, f"{i}_{candidate['id']}{ext}"))
            ids.append(candidate["id"])
        rows.append((group, key, slot["tier"], slot["original_length"], ids))

    lines = [INTRO]
    for group in ("played", "unused"):
        lines += [f"## {group.capitalize()} slots", "",
                  "| Slot | Yellow length | Match | Candidates, closest first |", "|---|---|---|---|"]
        for _, key, tier, length, ids in sorted((r for r in rows if r[0] == group),
                                                key=lambda r: (TIER_ORDER[r[2]], r[1])):
            lines.append(f"| {key} | {length:.2f}s | {tier} | {', '.join(ids)} |")
        lines.append("")
    with open(os.path.join(args.out_dir, "MATCHES.md"), "w") as f:
        f.write("\n".join(lines))
    print(f"wrote {len(rows)} slots to {args.out_dir}")


if __name__ == "__main__":
    main()
