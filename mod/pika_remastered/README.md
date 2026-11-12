# Pika Remastered

Plays clearer Pikachu clips in place of Pokémon Yellow's 42 bitcrushed partner voice clips.
Switch it on and off with the **PIKA REMASTERED** option. It comes with clips for the 26 slots
the game plays, from Pokémon: Let's Go, Pikachu! and Pokémon Sword and Shield.

## Setting it up

1. Copy this folder into your gen1recomp `mods/` folder and restart the game.
2. **PIKA REMASTERED** is on by default; turn it off in the mod's options to hear the originals.

A slot with no clip keeps the game's own sound. The **PIKACHU VOL** slider still sets the
volume, on top of the SFX volume, so turning SFX down turns Pikachu down too. At startup
the log says how many slots have a clip, for example `26 of 42 slots have a replacement`.

## Achievements

With Recomp Achievements installed, there are five achievements under the **PIKA** tab,
one of them hidden. Without it, the mod works the same and adds none.

## Changing clips

Clips live in `assets/cries/`, named by slot: `cry_01.ogg` to `cry_42.ogg`. `.wav`, `.mp3`
and `.flac` work too. Replace or delete any of them; a deleted slot plays Yellow's original.
`docs/CLIP_GUIDE.md` in the repo says where each slot plays, and the repo's tools build a
whole set from your own games.

## Limits

- Restart after changing clips or switching the option, because the game keeps each clip
  loaded once it has played.
- Built for engine 0.4.0. If a later engine loads the clips another way, the mod does
  nothing and the originals play.
- The Pokémon Box's Pikachu cry isn't replaced.

## Credits

Pikachu's voice is Ikue Ōtani's, from Pokémon: Let's Go, Pikachu! and Pokémon Sword and
Shield by Game Freak, Nintendo and The Pokémon Company, used without permission in a free
fan project and removed on request. The engine is gen1recomp by bryanthaboi.
