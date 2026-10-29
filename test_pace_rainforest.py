import os
import re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000

os.makedirs("audio/rainforest", exist_ok=True)

# ---------------------------------------------------------
# PACE TEST SCRIPTS (Explicit [PAUSE: X.X] silence tags)
# ---------------------------------------------------------

PACE_TEST_SCRIPTS = {
    "departure_1": """
        You step inside the warm wooden sleeper car. [PAUSE: 1.6]
        And the heavy glass door slides shut behind you. [PAUSE: 2.4]
        The misty platform outside... softens into the dark emerald trees. [PAUSE: 2.2]
        You sink onto the wide velvet bench. [PAUSE: 1.5]
        Resting your cheek against the cool window pane. [PAUSE: 2.5]
        Beneath the floorboards... the wheels begin their slow, steady rhythm. [PAUSE: 1.8]
        Clack-clack... [PAUSE: 1.2] clack-clack. [PAUSE: 2.6]
        Above the curved roof... warm tropical rain begins to tap against the metal. [PAUSE: 2.4]
        You are dry... enclosed... and completely safe. [PAUSE: 2.0]
        With nowhere to arrive... [PAUSE: 1.8] and nothing left to carry. [PAUSE: 1.5]
    """,

    "drift_01": """
        Broad emerald fern fronds... brush past the wet window glass. [PAUSE: 2.2]
        Glowing softly... in the amber light from your cabin. [PAUSE: 1.5]
    """,

    "drift_05": """
        Pale silver mist curls between the dark tree trunks outside. [PAUSE: 2.3]
        Floating weightlessly... above the forest floor. [PAUSE: 1.5]
    """,

    "drift_11": """
        The train glides across an old stone viaduct. [PAUSE: 2.2]
        High above a wide... slow-moving jungle river. [PAUSE: 1.5]
    """
}

def apply_edge_fade(audio_array, fade_ms=45):
    """Applies a gentle cosine fade-in and fade-out to prevent any start/stop clicks."""
    fade_samples = int(SAMPLE_RATE * (fade_ms / 1000.0))
    if len(audio_array) < fade_samples * 2:
        return audio_array
    fade_in = np.linspace(0.0, 1.0, fade_samples)
    fade_out = np.linspace(1.0, 0.0, fade_samples)
    audio_array[:fade_samples] *= fade_in
    audio_array[-fade_samples:] *= fade_out
    return audio_array

def render_paced_clip(marked_text, output_path, speed=0.78):
    # Split text by [PAUSE: X.X] tags
    tokens = re.split(r'(\[PAUSE:\s*\d+(?:\.\d+)?\])', marked_text.strip())
    full_audio = []

    # 250ms gentle lead-in silence so the clip never starts abruptly
    full_audio.append(np.zeros(int(SAMPLE_RATE * 0.25), dtype=np.float32))

    for token in tokens:
        token = token.strip()
        if not token:
            continue
        pause_match = re.match(r'\[PAUSE:\s*(\d+(?:\.\d+)?)\]', token)
        if pause_match:
            pause_sec = float(pause_match.group(1))
            silence = np.zeros(int(SAMPLE_RATE * pause_sec), dtype=np.float32)
            full_audio.append(silence)
        else:
            clean_line = " ".join(token.splitlines()).strip()
            if not clean_line:
                continue
            generator = pipeline(clean_line, voice='af_nicole', speed=speed, split_pattern=r'\n+')
            phrase_Collapse = [seg for _, _, audio_seg in generator for seg in audio_seg]
            if phrase_Collapse:
                phrase_arr = apply_edge_fade(np.array(phrase_Collapse, dtype=np.float32), fade_ms=45)
                full_audio.append(phrase_arr)

    # 350ms gentle tail silence
    full_audio.append(np.zeros(int(SAMPLE_RATE * 0.35), dtype=np.float32))
    final_wav = np.concatenate(full_audio)
    sf.write(output_path, final_wav, SAMPLE_RATE)

if __name__ == "__main__":
    print("Rendering 4 Pace-Test Clips with true sentence silences...")
    for clip_name, script in PACE_TEST_SCRIPTS.items():
        out_file = f"audio/rainforest/{clip_name}.wav"
        print(f" -> {out_file}")
        render_paced_clip(script, out_file)
    print("Pace test clips complete!")
