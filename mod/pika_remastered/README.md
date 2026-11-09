# Pika Remastered

Plays clearer Pikachu clips in place of Pokémon Yellow's 42 bitcrushed partner voice clips.
Switch it on and off with the **PIKA REMASTERED** option. This folder has no audio in it;
the clips come from your own games, built with the tools in the repo.

## Setting it up

1. Put clips in `assets/cries/`, named by slot: `cry_01.ogg` to `cry_42.ogg`. `.wav`, `.mp3`
   and `.flac` work too. `docs/CLIP_GUIDE.md` in the repo says where each slot plays, and
   `tools/build_cries.py` makes this folder from a recipe.
2. Copy this folder into your gen1recomp `mods/` folder and restart the game.
3. Turn on **PIKA REMASTERED** in the mod's options. It's on by default.

A slot with no clip keeps the game's own sound. The **PIKACHU VOL** slider still sets the
volume, on top of the SFX volume, so turning SFX down turns Pikachu down too. At startup
the log says how many slots have a clip, for example `26 of 42 slots have a replacement`.

## Limits

- Restart after changing clips or switching the option, because the game keeps each clip
  loaded once it has played.
- Built for engine 0.4.0. If a later engine loads the clips another way, the mod does
  nothing and the originals play.
- The Pokémon Box's Pikachu cry isn't replaced.
