-- Pika Remastered achievements
-- Adds five achievements to Recomp Achievements when it's installed, under
-- their own PIKA tab. Clips are counted from the engine's
-- sound.played event, which names each Pikachu clip PIKACHU_PCM_<slot>.
-- Which clips you've heard is kept per save in mod.save, so each playthrough
-- starts fresh. Without Recomp Achievements this file does nothing.
-- ------------------

local PLAYED = { 1, 2, 3, 4, 5, 6, 9, 10, 11, 13, 15, 18, 19, 20, 25, 26, 28, 29, 31,
                 33, 34, 35, 37, 38, 39, 40 }
local SLEEPING = 37

local DEFINITIONS = {
  { id = "first_words", title = "Pika, Remastered", points = 2, category = "AUDIO",
    games = { "yellow" },
    description = "Hear Pikachu's new voice for the first time." },
  { id = "chatterbox", title = "Chatterbox", points = 10, category = "AUDIO",
    games = { "yellow" }, goal = 100, unit = "CLIPS",
    description = "Hear Pikachu's new voice 100 times." },
  { id = "full_vocabulary", title = "Full Vocabulary", points = 25, category = "AUDIO",
    games = { "yellow" }, goal = #PLAYED, unit = "CLIPS",
    description = "Hear all 26 remastered clips in one save. Oak's Lab only comes round once." },
  { id = "sweet_dreams", title = "Sweet Dreams", points = 5, category = "AUDIO",
    games = { "yellow" },
    description = "Hear Pikachu talk in its sleep." },
  { id = "glutton", title = "Glutton for Punishment", points = 3, category = "AUDIO",
    games = { "yellow" }, hidden = true,
    description = "Switch PIKA REMASTERED off and listen to the 1-bit original on purpose." },
}

-- clips: slot -> file, from main.lua. enabled: reads the PIKA REMASTERED option.
return function(mod, clips, enabled)
  local found = mod.find("recomp_achievements")
  if not found then return end
  local ach = found.exports
  local major = tonumber(tostring(ach.apiVersion or ""):match("^(%d+)"))
  if major ~= 1 or not ach.supports("progress") then
    mod.log:warn("Recomp Achievements API %s isn't supported, so no achievements", tostring(ach.apiVersion))
    return
  end

  -- The full mod name is too wide for a tab, so it gets a short label.
  local handle, code, message = ach.connect(mod, { tab = "PIKA" })
  if not handle then
    mod.log:warn("couldn't connect to Recomp Achievements: %s %s", tostring(code), tostring(message))
    return
  end
  local ok, errors = handle:registerMany(DEFINITIONS)
  for i, err in pairs(errors or {}) do
    mod.log:warn("achievement %d rejected: %s %s", i, tostring(err[1]), tostring(err[2]))
  end
  mod.log:info("registered %d achievements", ok or 0)

  local played = {}
  for _, slot in ipairs(PLAYED) do played[slot] = true end

  -- Heard slots are saved as a 42-character string of 0s and 1s, which any save can hold.
  local function heardSet()
    local saved = mod.save:get("heard", "")
    local set = {}
    for slot = 1, 42 do set[slot] = saved:sub(slot, slot) == "1" end
    return set
  end

  local function saveHeard(set)
    local out = {}
    for slot = 1, 42 do out[slot] = set[slot] and "1" or "0" end
    mod.save:set("heard", table.concat(out))
  end

  local function vocabulary(set)
    local count = 0
    for _, slot in ipairs(PLAYED) do
      if set[slot] then count = count + 1 end
    end
    return count
  end

  local function record(slot, remastered)
    if not remastered then
      handle:unlock("glutton")
      return
    end
    handle:unlock("first_words")
    handle:addProgress("chatterbox", 1)
    if slot == SLEEPING then handle:unlock("sweet_dreams") end
    if played[slot] then
      local set = heardSet()
      if not set[slot] then
        set[slot] = true
        saveHeard(set)
      end
      handle:setProgress("full_vocabulary", vocabulary(set))
    end
  end

  -- The title screen plays clips before a save is attached, so those wait for ready.
  local waiting = {}

  mod.events:on(ach.events.ready, function()
    for _, clip in ipairs(waiting) do record(clip.slot, clip.remastered) end
    waiting = {}
    -- Brings the counter in line with the save after a rewind or a reinstall.
    handle:setProgress("full_vocabulary", vocabulary(heardSet()))
  end)

  mod.events:on("sound.played", function(ev)
    local slot = ev and type(ev.name) == "string" and tonumber(ev.name:match("^PIKACHU_PCM_(%d+)$"))
    if not slot then return end
    local on = enabled()
    -- A slot without a clip plays the original even with the option on; that counts for nothing.
    if on and not clips[slot] then return end
    if ach.currentGame() then
      record(slot, on)
    else
      waiting[#waiting + 1] = { slot = slot, remastered = on }
    end
  end)
end
