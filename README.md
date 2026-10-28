# Dream Portals

A sleep app: OLED-black, one-tap "Dream Portals" — guided drift journeys that carry
you to sleep. 10 portals planned; Portal #1 (Bus to the Moon) is the prototype.

## Concept

Standardized 30-minute structure per portal:

- **0–4 min — boarding:** settle in, departure narration
- **4–18 min — modular drift:** 8–10 scenes, 5 picked per run
- **18–22 min — lucid seed:** quiet suggestion at −30% volume
- **22–30 min — pure soundscape fade**

Optional pre-flights: +3-min Body Unwind, +5-min Mind Shuffle.
Standalone modes (planned, not built): Quiet Mind (cognitive shuffler) and Sound Mixer.

Voice: Kokoro-82M local (`af_nicole`, 0.80x) or ElevenLabs Creator. Static client-side
stitcher, no server runtime.

## Current status (prototype — work in progress)

Built:

- Portal #1: Bus to the Moon — page (`index.html`) + 8 voice clips
  (`audio/moon_bus/`, 24kHz WAV, ~5.4 min total: departure, 6 drifts, lucid seed)
- Voice generation script (`generate_moon_bus.py`, Kokoro)

Not built yet:

- Portals #2–10
- Full 30-minute runtime (current prototype runs ~7 min of voice+pauses, not 30)
- Toggles are visual-only; Quiet Mind / Sound Mixer modes not built
- No sleep-timer / fade-out, no sentence-level pauses

## Files

- `index.html` — the prototype page (Portal #1)
- `generate_moon_bus.py` — generates the Portal #1 voice clips with Kokoro
- `audio/moon_bus/` — the 8 generated WAV clips
- `index-standalone.html` (local only, not in repo) — single-file build with audio
  embedded; regenerate from the sources above

## Run it

Open `index.html` in a browser. To regenerate voice clips, install Kokoro
(`pip install kokoro soundfile`) and run `python generate_moon_bus.py`.
