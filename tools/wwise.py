"""Wwise banks and .wem audio from Let's Go, Pikachu! and Let's Go, Eevee!

Reads a .bnk to find the media IDs of its sounds, and decodes .wem files to
16-bit WAV. Handles codec 0x3039 (Switch Opus, through the system's libopus)
and plain 16-bit PCM. Other Wwise codecs, and readable event names, are out of
scope: the banks only store hashes of the names.

    python3 wwise.py INPUT.wem OUTPUT.wav
"""
# ------------------
import ctypes
import ctypes.util
import struct
import sys
import wave

import numpy as np

SOUND_OBJECT = 2  # HIRC type for a Sound
OPUS_SWITCH = 0x3039
PCM_CODECS = (0x0001, 0xFFFE)
MAX_FRAME = 5760  # 120 ms at 48 kHz, the largest Opus frame

_opus = None


def _libopus():
    # Loaded on first use, so PCM files decode without libopus installed.
    global _opus
    if _opus is None:
        name = ctypes.util.find_library("opus")
        if not name:
            raise RuntimeError("libopus not found; install libopus0 (Debian/Ubuntu) or opus (Homebrew/Arch)")
        lib = ctypes.CDLL(name)
        lib.opus_decoder_create.restype = ctypes.c_void_p
        lib.opus_decoder_create.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int)]
        lib.opus_decode.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int,
                                    ctypes.POINTER(ctypes.c_int16), ctypes.c_int, ctypes.c_int]
        lib.opus_decoder_destroy.argtypes = [ctypes.c_void_p]
        _opus = lib
    return _opus


# Banks

def bank_sections(data):
    """Map each section tag (BKHD, HIRC...) to its (offset, size)."""
    sections, pos = {}, 0
    while pos + 8 <= len(data):
        tag = data[pos:pos + 4].decode("latin1")
        size = struct.unpack_from("<I", data, pos + 4)[0]
        sections[tag] = (pos + 8, size)
        pos += 8 + size
    return sections


def bank_objects(data):
    """Yield (type, id, body) for each object in the bank's HIRC section."""
    sections = bank_sections(data)
    if "HIRC" not in sections:
        return
    pos, _ = sections["HIRC"]
    count = struct.unpack_from("<I", data, pos)[0]
    pos += 4
    for _ in range(count):
        kind = data[pos]
        size, object_id = struct.unpack_from("<II", data, pos + 1)
        yield kind, object_id, data[pos + 9:pos + 5 + size]
        pos += 5 + size


def bank_media_ids(path):
    """Media IDs of every Sound in a bank, which are also its .wem file names."""
    data = open(path, "rb").read()
    ids = set()
    for kind, _, body in bank_objects(data):
        if kind == SOUND_OBJECT:
            # Plugin ID (u32) and stream type (u8) come before the media ID.
            ids.add(struct.unpack_from("<I", body, 5)[0])
    return sorted(ids)


# .wem files

def _riff_chunks(data):
    chunks, pos = {}, 12
    while pos + 8 <= len(data):
        tag = data[pos:pos + 4]
        size = struct.unpack_from("<I", data, pos + 4)[0]
        chunks[tag] = data[pos + 8:pos + 8 + size]
        pos += 8 + size + (size & 1)
    return chunks


def _decode_opus(fmt, data, rate, channels):
    # fmt extras: total samples at +6, offset-table size at +18.
    extra = fmt[18:]
    total = struct.unpack_from("<I", extra, 6)[0]
    table_size = struct.unpack_from("<I", extra, 18)[0]
    count = table_size // 4
    offsets = list(struct.unpack_from(f"<{count}I", data, 0))
    packets = data[table_size:]
    offsets.append(len(packets))

    lib = _libopus()
    err = ctypes.c_int()
    decoder = lib.opus_decoder_create(rate, channels, ctypes.byref(err))
    if err.value != 0:
        raise RuntimeError(f"opus_decoder_create failed ({err.value})")
    buf = (ctypes.c_int16 * (MAX_FRAME * channels))()
    pcm = []
    try:
        for i in range(count):
            raw = packets[offsets[i]:offsets[i + 1]]
            # Nintendo's 8-byte header: packet size (big-endian), then final range.
            size = struct.unpack_from(">I", raw, 0)[0]
            packet = raw[8:8 + size]
            got = lib.opus_decode(decoder, packet, len(packet), buf, MAX_FRAME, 0)
            if got < 0:
                raise RuntimeError(f"opus_decode failed ({got}) at packet {i}")
            pcm.append(np.frombuffer(bytes(buf)[:got * channels * 2], dtype=np.int16).copy())
    finally:
        lib.opus_decoder_destroy(decoder)

    out = np.concatenate(pcm) if pcm else np.zeros(0, np.int16)
    # The decoder's start-up samples sit in front of the real audio.
    skip = max(0, len(out) // channels - total)
    return out[skip * channels:]


def decode_wem(path):
    """Decode a .wem to (interleaved int16 samples, sample rate, channels)."""
    chunks = _riff_chunks(open(path, "rb").read())
    fmt, data = chunks[b"fmt "], chunks[b"data"]
    codec, channels, rate = struct.unpack_from("<HHI", fmt)
    bits = struct.unpack_from("<H", fmt, 14)[0]
    if codec in PCM_CODECS and bits == 16:
        # A few Let's Go sounds are stored as plain PCM.
        return np.frombuffer(data, dtype="<i2").copy(), rate, channels
    if codec == OPUS_SWITCH:
        return _decode_opus(fmt, data, rate, channels), rate, channels
    raise ValueError(f"unsupported codec {codec:#x}")


def wem_to_wav(src, dst):
    """Write src as a 16-bit WAV at dst and return its length in seconds."""
    pcm, rate, channels = decode_wem(src)
    with wave.open(dst, "wb") as out:
        out.setnchannels(channels)
        out.setsampwidth(2)
        out.setframerate(rate)
        out.writeframes(pcm.tobytes())
    return len(pcm) / channels / rate


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: python3 wwise.py INPUT.wem OUTPUT.wav")
    print(f"{wem_to_wav(sys.argv[1], sys.argv[2]):.2f}s")
