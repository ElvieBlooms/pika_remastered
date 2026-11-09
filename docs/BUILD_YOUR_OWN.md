# Build your own

Three ways to use the tools: rebuild my picks, make your own, or voice a different partner.
Every clip comes from games you own. This guide starts from game files you already have and
doesn't cover dumping or decrypting games.

## Setup

- Python 3.9 or newer, then `pip install -r tools/requirements.txt`.
- libopus for the Let's Go audio: `libopus0` on Debian and Ubuntu, `opus` on Homebrew and Arch.
- Yellow's own clips, for ranking and listening. After you import Yellow into gen1recomp
  they're in your game data at `yellow/assets/generated/audio/pika_cries/cry_NN.wav`.

## Clip IDs

Each clip gets an ID: a prefix you choose, plus its file name or part of it. You set this up
with `--source PREFIX DIR [GLOB [REGEX]]`, the same way in every tool:

```
--source lgpe_ work/lgpe
    work/lgpe/102097674.wav becomes lgpe_102097674

--source swsh_ swsh 'Play_PV_025_00_00*.ogg' '(PM025_\d+)'
    Play_PV_025_00_00 [PM025VC=PM025_42].ogg becomes swsh_PM025_42
```

Recipes and rankings store these IDs, so keep the same prefixes from start to finish.

## 1. Decode a Let's Go voice bank

```
python3 tools/extract_bank.py BANK_DIR PokemonVoice_AibouPikatyuu work/lgpe
```

`BANK_DIR` is the game's folder of `.bnk` and `.wem` files. The tool reads the bank's list of
sounds and writes each one as `work/lgpe/<media id>.wav`.

| Bank | Partner | Sounds |
|---|---|---|
| `PokemonVoice_AibouPikatyuu` | Pikachu | 250 |
| `PokemonVoice_AibouIibui` | Eevee | 380 |

The banks only keep scrambled versions of the sound names, so clips go by number rather
than by name. The decoder reads Switch Opus (Wwise codec `0x3039`) and plain 16-bit PCM,
which covers both partner banks. To decode a single file:
`python3 tools/wwise.py INPUT.wem OUTPUT.wav`.

## 2. Rank the clips against Yellow's

```
python3 tools/rank_matches.py --originals YELLOW_CLIPS_DIR \
  --source lgpe_ work/lgpe \
  --source swsh_ SWSH_DIR 'Play_PV_025_00_00*.ogg' '(PM025_\d+)' \
  --out work/ranking.json
```

For each slot, every clip is scored on how closely it follows the Yellow clip's pitch
movement, with overall pitch and length counting for less. The top 8 are kept. A few
hundred clips take a few minutes. A good score means a similar delivery, not the same
recording, so treat it as a shortlist.

## 3. Listen side by side

```
python3 tools/listen_pack.py work/ranking.json work/listen
```

Each `work/listen/{played,unused}/slot_NN/` gets Yellow's clip as `0_...` and the four
closest as `1_<id>` to `4_<id>`. `MATCHES.md` lists the slots by match strength. Start with
the 26 played slots; the other 16 never play in the game. `docs/CLIP_GUIDE.md` says where
each slot is heard.

## 4. Write a recipe and build

A recipe maps slots to clip IDs. Leave a slot out to keep Yellow's own clip there.

```json
{
  "recipe_format": 1,
  "kind": "anime_pikachu_cries",
  "picks": {
    "cry_01": { "clip": "swsh_PM025_74" },
    "cry_02": { "clip": "lgpe_985767294" }
  }
}
```

Only `picks` is read; the other keys are for your own tools. Then:

```
python3 tools/build_cries.py my.recipe.json \
  --source lgpe_ work/lgpe \
  --source swsh_ SWSH_DIR 'Play_PV_025_00_00*.ogg' '(PM025_\d+)' \
  --out mod/pika_remastered/assets/cries
```

Each clip has the silence at both ends trimmed and a 10 ms fade-out, then is raised to
-9 LUFS with a limiter holding peaks at -1 dBFS, and saved as `cry_NN.ogg`. The boost
matters: Yellow's 1-bit clips are about as loud as audio gets, so clips mixed like normal
voice lines sound far too quiet next to them. Use `--loudness -12` (or any LUFS value) for a
different level, or `--loudness off` to keep each clip as it is. A recipe with an unknown
clip ID or slot name stops before writing anything.

## Voicing a different partner

Pika Remastered only changes the 42 clips Yellow plays for its partner. Filling them with
Eevee clips makes your partner sound like Eevee, but it's still Pikachu everywhere else: the
walking sprite, the species and the scenes stay the game's own. Pair it with a mod that
changes those for a full partner Eevee.

To make an Eevee version:

1. Fork the repo and rename the mod: `id` and `name` in `manifest.json`, the option `label`
   in `main.lua`, and the folder name.
2. Decode the Eevee bank:
   `python3 tools/extract_bank.py BANK_DIR PokemonVoice_AibouIibui work/eevee`
3. Rank, listen, write a recipe and build, with `--source eevee_ work/eevee`.

Ranking Eevee clips against Yellow's Pikachu still finds ones with a similar rise, fall and
length, which is a good start for matching each slot's mood and timing.
