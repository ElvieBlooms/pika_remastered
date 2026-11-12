-- Pika Remastered
-- Plays your chosen clips in place of Yellow's 42 bitcrushed Pikachu voice clips.
-- Every clip goes through Sound.playPikaCry (src/core/Sound.lua), which opens
-- assets/generated/audio/pika_cries/cry_NN.wav with love.audio.newSource and
-- caches it. There's no mod hook for that, so this wraps love.audio.newSource
-- and points those 42 paths at assets/cries/cry_NN.* in this folder.
-- Every other sound passes straight through, and a slot with no file keeps
-- the game's own clip. achievements.lua adds achievements when Recomp
-- Achievements is installed.
-- ------------------

local CLIP_COUNT = 42
local EXTENSIONS = { "ogg", "wav", "mp3", "flac" }
local CLIP_PATH = "pika_cries[/\\]cry_(%d%d)%.wav$"

-- Finds which slots have a file, keyed by slot number.
-- Loads one of our own files inside the mod's sandbox, whatever the folder is called.
local function import(mod, path)
  local source = mod:read(path)
  assert(source, "pika_remastered: missing file " .. path)
  local chunk, err = load(source, "@" .. mod.id .. "/" .. path)
  assert(chunk, err)
  return chunk()
end

local function findClips(mod)
  local ok, names = pcall(mod.list, mod, "assets/cries")
  if not ok or type(names) ~= "table" then return {}, 0 end

  -- Matched case-insensitively, so CRY_04.WAV still counts.
  local byLower = {}
  for _, name in ipairs(names) do byLower[name:lower()] = name end

  local clips, count = {}, 0
  for slot = 1, CLIP_COUNT do
    for _, ext in ipairs(EXTENSIONS) do
      local name = byLower[("cry_%02d.%s"):format(slot, ext)]
      if name then
        clips[slot] = mod.assets:path("assets/cries/" .. name)
        count = count + 1
        break
      end
    end
  end
  return clips, count
end

return function(mod)
  mod.options:define({
    { key = "enabled", type = "toggle", label = "PIKA REMASTERED", default = true },
  })

  -- Read at play time, so the toggle reaches any clip that hasn't played yet.
  local function enabled()
    local ok, value = pcall(mod.options.get, mod.options, "enabled")
    if not ok or value == nil then return true end
    return value and true or false
  end

  local clips, count = findClips(mod)
  mod.log:info("%d of %d slots have a replacement", count, CLIP_COUNT)
  if count == 0 then return end

  local audio = love and love.audio
  if not (audio and type(audio.newSource) == "function") then
    mod.log:warn("love.audio isn't available, so the game's own clips will play")
    return
  end

  -- Achievements are a bonus, so a problem in them never stops the clips.
  local ok, err = pcall(function() import(mod, "achievements.lua")(mod, clips, enabled) end)
  if not ok then mod.log:warn("achievements are off: %s", tostring(err)) end

  local newSource = audio.newSource
  audio.newSource = function(source, ...)
    if type(source) == "string" and enabled() then
      local slot = source:match(CLIP_PATH)
      local path = slot and clips[tonumber(slot)]
      if path then
        local ok, replacement = pcall(newSource, path, ...)
        if ok and replacement then return replacement end
        -- A file that won't load falls back to the game's clip.
        mod.log:warn("couldn't load %s, playing the original (%s)", path, tostring(replacement))
      end
    end
    return newSource(source, ...)
  end
end
