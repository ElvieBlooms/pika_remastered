# Pika Remastered

Pokémon Yellow's partner Pikachu talks in 42 short voice clips, stored as 1-bit audio that
sounds crushed and hissy. Pika Remastered plays clearer Pikachu clips in their place, and you
can switch back to the originals with the **PIKA REMASTERED** option.

It's a mod for [gen1recomp](https://github.com/bryanthaboi/gen1recomp), built on engine 0.4.0.
The download comes with my picks for the 26 clips the game actually plays, taken from
Pokémon: Let's Go, Pikachu! and Pokémon Sword and Shield. Nothing from Yellow is included.

## What you get

- Clearer Pikachu everywhere Yellow uses its voice: talking to your partner, battle,
  the Pokédex, the title screen, the story scenes and the surfing minigame.
- Clips that can run longer or shorter than the originals. Pikachu's reactions and the
  scenes wait for the clip to finish, so nothing gets cut off.
- The game's **PIKACHU VOL** slider still sets the volume. It works on top of the SFX
  volume, so keep SFX up and use **PIKACHU VOL** to balance Pikachu against the rest.
- Any slot without a clip keeps the game's own sound.
- Five achievements when [Recomp Achievements](https://github.com/ElvieBlooms/recomp_achievements)
  is installed, under the **PIKA** tab. Without it, nothing changes.

## Installing

Copy `mod/pika_remastered/` into your gen1recomp `mods/` folder and restart the game.
**PIKA REMASTERED** is on by default.

## What's in the repo

| Path | What it is |
|---|---|
| `mod/pika_remastered/` | The mod, with my 26 clips in `assets/cries/`. |
| `recipes/pikachu.recipe.json` | My picks: which clip goes in each slot, by clip ID. |
| `tools/` | Python tools that decode Let's Go voice banks, rank clips against Yellow's, lay them out for listening, and build `assets/cries/` from a recipe. |
| `docs/CLIP_GUIDE.md` | All 42 slots, how long each original is, and where it plays. |
| `docs/PICKS.md` | My picks, with where each clip came from. |
| `docs/HOW_IT_WORKS.md` | How the mod hooks into the engine, and its limits. |
| `docs/BUILD_YOUR_OWN.md` | Making your own set from your games, or voicing a different partner such as Eevee. |

## Achievements

With Recomp Achievements 1.0 or newer installed, Pika Remastered adds these to its menu:

| Achievement | Points | How |
|---|---|---|
| Pika, Remastered | 2 | Hear Pikachu's new voice for the first time. |
| Chatterbox | 10 | Hear the new voice 100 times. |
| Full Vocabulary | 25 | Hear all 26 remastered clips in one save. Oak's Lab only comes round once. |
| Sweet Dreams | 5 | Hear Pikachu talk in its sleep. |
| ??? | 3 | Hidden. It involves the 1-bit original. |

Clips heard on the title screen count once a save is loaded. Each save keeps its own list,
so a new game starts Full Vocabulary over.

## Making your own set

The tools rebuild everything from your own copies of the games, so you can swap any slot,
redo the lot, or voice a different partner. `docs/BUILD_YOUR_OWN.md` goes through each step.

## Limits

- Restart the game after changing clips or switching **PIKA REMASTERED**. The game keeps each
  clip loaded once it has played.
- There's no modding hook for these clips, so the mod wraps the engine's audio loader
  (`docs/HOW_IT_WORKS.md`). If a later engine loads them another way, the mod does nothing
  and the originals play.
- The Pokémon Box's Pikachu cry isn't replaced.

## Credits

- [gen1recomp](https://github.com/bryanthaboi/gen1recomp) by bryanthaboi, the engine this mod runs on.
- Pikachu's voice is Ikue Ōtani's, from Pokémon: Let's Go, Pikachu! and Pokémon Sword and
  Shield by Game Freak, Nintendo and The Pokémon Company. The clips are used without
  permission in a free, non-commercial fan project. If you hold the rights and want them
  taken down, open an issue or contact me and they'll be removed.

## Licence

The code and docs are MIT (`LICENSE`). The audio clips aren't covered by that licence or
any other from me: Pokémon and all game audio belong to their owners.
