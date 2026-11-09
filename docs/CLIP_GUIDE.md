# Clip guide

All 42 of Yellow's Pikachu voice clips: how long each original is, and everywhere
engine 0.4.0 plays it. A replacement goes in the mod's `assets/cries/` as `cry_NN.ogg`
(or `.wav`, `.mp3`, `.flac`), using the two-digit slot number.

**26 slots play somewhere in the game. The other 16 never do**: they're on the cart,
but nothing in the engine calls them. Start with the 26.

## How talking to Pikachu picks a reaction

Outside the scripted scenes, two hidden values pick Pikachu's reaction when you talk
to it: friendship (0 to 255) and mood (0 to 255, drifting back to 128 over time). Here,
"good mood" means above 128, "bad mood" below 128, and "neutral" exactly 128. Mood keeps
settling at 128, so the neutral reactions are the ones you hear most.

Some cases come first and skip the friendship and mood table: Pikachu asleep, a status
problem, Pokémon Tower, just after catching or fishing, and the scripted scenes.

Two reactions play no clip at all: friendship 0 to 50 in a good mood, and the reaction
after you try a Thunder Stone. The refusal itself still plays clip 01.

| Slot | Original | Where it plays |
|---|---|---|
| 01 | 0.84s | Title screen: Pikachu pops up<br>Every generic Pikachu cry: battle send-out, Pokédex, refusing a Thunder Stone<br>Talk: friendship 161 to 200, neutral mood |
| 02 | 0.63s | Oak's Lab: Pikachu refuses the Poké Ball |
| 03 | 0.93s | Talk: friendship 101 to 130, neutral mood |
| 04 | 1.48s | Battle: any Pikachu fainting<br>Talk: inside Pokémon Tower |
| 05 | 1.51s | Talk: friendship 201+, good mood (heart)<br>Pokémon Fan Club scenes |
| 06 | 1.68s | Talk: friendship 51 to 100, bad mood (skull) |
| 07 | 1.27s | _not played in engine 0.4.0_ |
| 08 | 1.56s | _not played in engine 0.4.0_ |
| 09 | 1.23s | Bill's House: Bill steps out of the machine (!) |
| 10 | 2.97s | Talk: friendship 0 to 50, bad mood (angry bolt) |
| 11 | 0.66s | Title screen: pressing Start/A to leave |
| 12 | 1.25s | _not played in engine 0.4.0_ |
| 13 | 1.81s | Talk: friendship 161+, bad mood |
| 14 | 2.28s | _not played in engine 0.4.0_ |
| 15 | 1.90s | Talk: Pikachu has a status problem (poison, burn, etc.) |
| 16 | 1.91s | _not played in engine 0.4.0_ |
| 17 | 0.78s | _not played in engine 0.4.0_ |
| 18 | 1.40s | Talk: right after you catch a Pokémon |
| 19 | 2.06s | Bill's House: Bill-as-a-Pokémon confusion (?)<br>Bill's House: talking to Pikachu after meeting human Bill |
| 20 | 2.97s | Talk: right after fishing |
| 21 | 2.97s | _not played in engine 0.4.0_ |
| 22 | 2.33s | _not played in engine 0.4.0_ |
| 23 | 1.38s | _not played in engine 0.4.0_ |
| 24 | 2.61s | _not played in engine 0.4.0_ |
| 25 | 1.32s | Talk: friendship 51 to 100, good mood |
| 26 | 1.26s | Bill's House: talking to Pikachu before meeting human Bill, and a scripted walk |
| 27 | 1.05s | _not played in engine 0.4.0_ |
| 28 | 1.70s | Day-Care: leaving Pikachu there<br>Surfing minigame: finished, no new high score |
| 29 | 1.13s | Talk: friendship 131 to 160, neutral mood |
| 30 | 0.44s | _not played in engine 0.4.0_ |
| 31 | 0.70s | Talk: friendship 51 to 100, neutral mood |
| 32 | 0.51s | _not played in engine 0.4.0_ |
| 33 | 1.18s | Talk: friendship 201 to 250, neutral mood<br>Talk: friendship 251+, neutral mood (heart) |
| 34 | 1.95s | Talk: friendship 131 to 160, good mood<br>Surfing minigame: new high score |
| 35 | 1.69s | Talk: friendship 161 to 200, good mood (smile)<br>Talk: just learned Thunderbolt/Thunder (bolt)<br>Day-Care: getting Pikachu back |
| 36 | 2.59s | _not played in engine 0.4.0_ |
| 37 | 1.30s | Talk: Pikachu is asleep (Zzz)<br>Pewter Pokémon Center: sleeping scene |
| 38 | 1.15s | Talk: friendship 0 to 50, neutral mood (skull) |
| 39 | 1.63s | Talk: friendship 101 to 130, good mood |
| 40 | 1.40s | Talk: friendship 101 to 160, bad mood |
| 41 | 2.24s | _not played in engine 0.4.0_ |
| 42 | 2.00s | _not played in engine 0.4.0_ |

## Notes

- **Length:** a clip can run longer or shorter than the original. Reactions and
  scenes wait for it to finish, so nothing gets cut off; a long clip just holds
  Pikachu's reaction longer.
- **Clip 01 does the most work.** It's Pikachu's cry in battle, the Pokédex and on the
  title screen, so a clean, neutral "Pika!" suits it best.
- **Format:** any sample rate, mono or stereo. OGG keeps the mod small.
