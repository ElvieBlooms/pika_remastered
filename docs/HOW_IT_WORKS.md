# How it works

## Where Yellow's Pikachu clips play

In gen1recomp engine 0.4.0, every Pikachu voice clip goes through one function,
`Sound.playPikaCry(data, n)` in `src/core/Sound.lua`. That covers:

- talking to your partner (its reactions to friendship and mood),
- Pikachu's cry in battle, the Pokédex and on the title screen, and its faint cry,
- the story scenes: Oak's Lab, Bill's House, the Day-Care, the Fan Club and the Pewter
  Pokémon Center,
- the surfing minigame.

`playPikaCry` builds the path `assets/generated/audio/pika_cries/cry_NN.wav`, which is in the
game data you imported. It opens that file with `love.audio.newSource` the first time the
clip plays and keeps it loaded for the rest of the session.

The engine's data only stores how many clips there are (`pikaCries = 42`). The `PIKACHU`
entry in the `cries` registry is Pikachu's ordinary chiptune cry, a different sound. So
there's no modding hook or registry entry to change these clips through.

## What the mod does

The mod sandbox blocks `love.filesystem`, `love.thread`, `love.system` and `love.event`, but
gives mods the real `love.audio`. When it loads, the mod:

1. lists its own `assets/cries/` with `mod:list` and notes which slots have a clip
   (`cry_NN` as `.ogg`, `.wav`, `.mp3` or `.flac`),
2. wraps `love.audio.newSource`. When **PIKA REMASTERED** is on and the engine asks for
   `pika_cries/cry_NN.wav` for a slot with a clip, it opens the mod's clip instead. Every
   other sound goes through unchanged.

Because only the file changes, the engine handles the rest as usual:

- **Timing:** reactions and scenes wait on the clip's real length (`Sound.waitFrames`).
- **Volume:** **PIKACHU VOL** still applies. It trims Pikachu on top of the SFX volume, so
  turning SFX down turns Pikachu down too.
- **Format:** any sample rate, mono or stereo.

## Achievements

`achievements.lua` connects to Recomp Achievements through its provider API when it's
installed (an optional dependency in `manifest.json`), and does nothing when it isn't.

- **Counting clips:** the engine's `sound.played` event names each Pikachu clip
  `PIKACHU_PCM_<slot>`. A clip counts when **PIKA REMASTERED** is on and the slot has a
  replacement. With the option off, the original plays and counts toward the hidden one.
- **Full Vocabulary:** which slots you've heard is kept per save in `mod.save`, as a
  42-character string of 0s and 1s, and the progress is set from it whenever a save loads.
- **The title screen:** clips there play before a save is attached, so they're held and
  counted on the framework's `ready` event.
- **Problems stay contained:** the achievements load inside `pcall`, so an error in them
  logs a warning and the clips still play.

## Limits

- **Restarting:** each clip stays loaded after its first play, so switching the option
  mid-session only reaches clips that haven't played yet. New files need a restart too.
- **Engine changes:** this relies on engine 0.4.0 loading the clips through
  `love.audio.newSource` by path. If that changes, the wrapper never matches and the
  originals play.
- **Old imports:** if your import has 8-bit mono clips, the engine converts the original
  file itself and may skip the mod's clip. Current imports are 16-bit stereo and work.
- **Pokémon Box:** its Pikachu cry reads `cry_01.wav` directly and isn't replaced.

## Why the originals sound the way they do

Yellow stores these clips as 1-bit audio: every sample is either fully up or fully down.
That's the crushed sound, and it's why a waveform view of one is a solid block. The clips
were sampled from the late-90s anime, and the Switch games use newer recordings, so no
replacement is the same take. The tools look for a similar delivery instead.
