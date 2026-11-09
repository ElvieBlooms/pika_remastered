"""Decode every sound in one Let's Go voice bank to WAV.

Reads BANK_NAME.bnk from BANK_DIR, finds its sounds, and writes each
<media id>.wem as OUT_DIR/<media id>.wav. Files come from your own copy of the
game; nothing is downloaded or included.

    python3 extract_bank.py BANK_DIR PokemonVoice_AibouPikatyuu work/lgpe

Partner banks: PokemonVoice_AibouPikatyuu (Pikachu), PokemonVoice_AibouIibui (Eevee).
"""
# ------------------
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wwise  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("bank_dir", help="folder with the game's .bnk and .wem files")
    parser.add_argument("bank_name", help="bank file name without .bnk")
    parser.add_argument("out_dir")
    args = parser.parse_args()

    ids = wwise.bank_media_ids(os.path.join(args.bank_dir, args.bank_name + ".bnk"))
    os.makedirs(args.out_dir, exist_ok=True)
    decoded, missing, failed, seconds = 0, 0, 0, 0.0
    for media_id in ids:
        src = os.path.join(args.bank_dir, f"{media_id}.wem")
        if not os.path.exists(src):
            missing += 1
            continue
        try:
            seconds += wwise.wem_to_wav(src, os.path.join(args.out_dir, f"{media_id}.wav"))
            decoded += 1
        except (ValueError, RuntimeError) as e:
            failed += 1
            print(f"{media_id}.wem: {e}", file=sys.stderr)

    print(f"{args.bank_name}: {len(ids)} sounds, {decoded} decoded ({seconds:.1f}s), "
          f"{missing} missing .wem, {failed} failed")


if __name__ == "__main__":
    main()
