# Pika Remastered

Pokémon Yellow's partner Pikachu talks in 42 (26 actually happen in game) short voice clips, stored as 1-bit audio that
sounds crushed and hissy. Pika Remastered plays clearer Pikachu clips in their place, one
slot at a time, and you can switch back to the originals with the **PIKA REMASTERED** option.

It's a mod for [gen1recomp](https://github.com/bryanthaboi/gen1recomp), built on engine 0.4.0.

## What you get

- Clearer Pikachu everywhere Yellow uses its voice: talking to your partner, battle,
  the Pokédex, the title screen, the story scenes and the surfing minigame.
- Clips that can run longer or shorter than the originals. Pikachu's reactions and the
  scenes wait for the clip to finish, so nothing gets cut off.
- The game's **PIKACHU VOL** slider still sets the volume.
- Any slot without a clip keeps the game's own sound.

## What's in the repo

| Path | What it is |
|---|---|
| `mod/pika_remastered/` | The mod|
| `recipes/pikachu.recipe.json` | My picks: which clip goes in each slot, by clip ID. |
| `tools/` | Python tools that decode Let's Go voice banks, rank clips against Yellow's, lay them out for listening, and build `assets/cries/` from a recipe. |
| `docs/CLIP_GUIDE.md` | All 42 slots, how long each original is, and where it plays. |
| `docs/PICKS.md` | My picks, with where each clip came from. |
| `docs/HOW_IT_WORKS.md` | How the mod hooks into the engine, and its limits. |
| `docs/BUILD_YOUR_OWN.md` | Rebuilding my picks, making your own, or voicing a different partner such as Eevee. |

## Building my picks

You need the Let's Go, Pikachu! voice bank files (`.bnk` and `.wem`) and the Sword and Shield
Pikachu lines (`.ogg`, named `Play_PV_025_00_00 [PM025VC=PM025_NN].ogg`), both from your own
games. Then:

```
pip install -r tools/requirements.txt
python3 tools/extract_bank.py BANK_DIR PokemonVoice_AibouPikatyuu work/lgpe
python3 tools/build_cries.py recipes/pikachu.recipe.json \
  --source lgpe_ work/lgpe \
  --source swsh_ SWSH_DIR 'Play_PV_025_00_00*.ogg' '(PM025_\d+)' \
  --out mod/pika_remastered/assets/cries
```

Copy `mod/pika_remastered/` into your gen1recomp `mods/` folder and restart the game.
`docs/BUILD_YOUR_OWN.md` goes through each step, including libopus for the Let's Go audio.

## Limits

- Restart the game after changing clips or switching **PIKA REMASTERED**. The game keeps each
  clip loaded once it has played.
- There's no modding hook for these clips, so the mod wraps the engine's audio loader
  (`docs/HOW_IT_WORKS.md`). If a later engine loads them another way, the mod does nothing
  and the originals play.
- The Pokémon Box's Pikachu cry isn't replaced.

## Credits

- [gen1recomp](https://github.com/bryanthaboi/gen1recomp) by bryanthaboi, the engine this mod runs on.
- Pikachu is voiced by Ikue Ōtani in the games the clips come from. The clips are read from
  your own copies of Pokémon: Let's Go, Pikachu! and Pokémon Sword and Shield (Game Freak,
  Nintendo, The Pokémon Company.

## Licence

The code and docs are MIT (`LICENSE`). That covers nothing from the games: Pokémon and all
game audio belong to their owners.
