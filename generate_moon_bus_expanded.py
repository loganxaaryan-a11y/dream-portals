import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
OUTPUT_DIR = "audio/moon_bus_expanded"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS = {
    "departure_1": """
        You step aboard the quiet night coach. [PAUSE: 1.6]
        And the cushioned door seals with a low, gentle hush. [PAUSE: 2.3]
        Down the dim aisle... rows of wide, quilted wool seats wait in the amber dusk. [PAUSE: 2.2]
        You settle into a window seat near the middle of the cabin. [PAUSE: 1.8]
        Letting your shoulders drop into the deep padding behind you. [PAUSE: 2.4]
        Beneath your feet... the floor warms with a steady, low vibration. [PAUSE: 2.0]
        The dark tarmac outside falls away... replaced by open night sky. [PAUSE: 2.5]
        There are no stops to watch for... [PAUSE: 1.8] and nowhere you need to be. [PAUSE: 1.6]
    """,
    "departure_2": """
        The cabin air is cool... clean... and still. [PAUSE: 1.8]
        You sink back into the wide reclining seat... [PAUSE: 1.6]
        And pull the woven lap blanket across your knees. [PAUSE: 2.3]
        Along the floor... a thin ribbon of amber light marks the empty aisle. [PAUSE: 2.2]
        A deep, muffled hum rises smoothly through the frame of the coach. [PAUSE: 2.4]
        Outside your window... the distant city lights dim to tiny embers... [PAUSE: 2.0]
        And then dissolve into calm, open darkness. [PAUSE: 2.5]
        You are completely supported... drifting upward on a smooth, invisible road. [PAUSE: 1.6]
    """,
    "departure_3": """
        The ticket machine at the front of the coach is dark... and switched off for the night. [PAUSE: 2.2]
        You choose a quiet row by the wide observation pane. [PAUSE: 1.8]
        Resting your forearms on the padded armrests. [PAUSE: 2.3]
        The cabin pressure settles around your ears like a heavy winter coat. [PAUSE: 2.4]
        Without a jolt or a sound... the coach lifts into the clear night air. [PAUSE: 2.2]
        Only the steady ventilation whisper... and the low purr beneath the floorboards remain. [PAUSE: 2.5]
        Every muscle in your jaw... and your hands... can finally let go. [PAUSE: 1.6]
    """,
    "drift_01": """
        Far behind the rear window... the curve of the Earth glows in pale blue light. [PAUSE: 2.3]
        Slowly growing smaller... in the deep quiet. [PAUSE: 1.5]
    """,
    "drift_02": """
        Dim amber strips along the cabin floor... cast long shadows across the carpet. [PAUSE: 2.2]
        Nothing flickers... and nothing changes. [PAUSE: 1.5]
    """,
    "drift_03": """
        The coach glides through a thin bank of silver night mist. [PAUSE: 2.1]
        Fine droplets of light... trail smoothly past the outer pane. [PAUSE: 1.5]
    """,
    "drift_04": """
        Above your head... the small air vent breathes a steady stream of cool air. [PAUSE: 2.3]
        Blending into the deep hum of the hull. [PAUSE: 1.5]
    """,
    "drift_05": """
        Across the aisle... the empty wool seats rest in deep shadow. [PAUSE: 2.2]
        Swaying almost imperceptibly... with the motion of the coach. [PAUSE: 1.5]
    """,
    "drift_06": """
        Outside the thick window... unblinking stars hang still against the black sky. [PAUSE: 2.3]
        While the cabin around you stays dim and enclosed. [PAUSE: 1.5]
    """,
    "drift_07": """
        Your hands rest heavy and still... on the woven blanket across your lap. [PAUSE: 2.2]
        Rising and falling... with each unhurried breath. [PAUSE: 1.5]
    """,
    "drift_08": """
        Up near the front windshield... the instrument console glows a muted, sleepy green. [PAUSE: 2.3]
        Steady and calm... through the long night stretch. [PAUSE: 1.5]
    """,
    "drift_09": """
        A pale wash of silver moonlight... slides slowly across the padded headrest beside you. [PAUSE: 2.4]
        Moving less than an inch... every minute. [PAUSE: 1.5]
    """,
    "drift_10": """
        Beneath the rubber floor mat... the deep engine note holds a single, unwavering tone. [PAUSE: 2.3]
        Carrying the heavy coach without effort. [PAUSE: 1.5]
    """,
    "drift_11": """
        Fine cosmic dust drifts past the dark glass... like slow winter snow under a streetlamp. [PAUSE: 2.4]
        Silent... and weightless. [PAUSE: 1.5]
    """,
    "drift_12": """
        The heavy velvet curtain at the back of the cabin... hangs completely still. [PAUSE: 2.2]
        Holding the warmth inside the coach. [PAUSE: 1.5]
    """,
    "drift_13": """
        Ahead in the distance... the pale grey curve of the moon fills the upper window. [PAUSE: 2.4]
        Its quiet plains bathed in soft silver light. [PAUSE: 1.5]
    """,
    "drift_14": """
        The cool acrylic window frame... presses gently against your shoulder. [PAUSE: 2.2]
        Solid... smooth... and unchanging. [PAUSE: 1.5]
    """,
    "drift_15": """
        Every rattle of the road is gone... replaced by a smooth, floating glide. [PAUSE: 2.3]
        As if the tires are rolling over deep clouds. [PAUSE: 1.5]
    """,
    "drift_16": """
        In the reflection on the dark pane... the dim cabin light looks miles away. [PAUSE: 2.3]
        Fading further into the night. [PAUSE: 1.5]
    """,
    "drift_17": """
        A gentle warmth radiates from the baseboard heater near your ankles. [PAUSE: 2.2]
        Steady and unhurried. [PAUSE: 1.5]
    """,
    "drift_18": """
        The long metal frame of the coach... gives a tiny, muffled settle as it drifts. [PAUSE: 2.3]
        Cradling the quiet rows inside. [PAUSE: 1.5]
    """,
    "drift_19": """
        Out beyond the wing mirror... a wide sea of dark space stretches without end. [PAUSE: 2.3]
        Peaceful... and completely still. [PAUSE: 1.5]
    """,
    "drift_20": """
        Your eyelids grow heavier... matching the slow, steady hum beneath the seat. [PAUSE: 2.4]
        Letting the night coach carry you the rest of the way. [PAUSE: 1.5]
    """,
    "lucid_seed_1": """
        As the coach glides deeper into the silver quiet... [PAUSE: 2.2]
        Your body sleeps... [PAUSE: 1.8] while a calm spark of awareness rests inside the dream. [PAUSE: 2.4]
        Knowing you are dreaming... [PAUSE: 2.0] safe inside the quiet night. [PAUSE: 1.8]
    """,
    "lucid_seed_2": """
        Everything outside the glass is now a dream unfolding on its own. [PAUSE: 2.4]
        If you notice the silver moonlight later tonight... [PAUSE: 2.0]
        You will know softly that you are dreaming... [PAUSE: 2.2] and continue to rest. [PAUSE: 1.8]
    """,
    "lucid_seed_3": """
        You are drifting smoothly into deep, restful sleep. [PAUSE: 2.2]
        And as the dream world opens around this cabin... [PAUSE: 2.0]
        You can watch it gently... [PAUSE: 1.8] knowing it is all a dream. [PAUSE: 1.8]
    """,
}

def apply_edge_fade(a, fade_ms=45):
    fs = int(SAMPLE_RATE * (fade_ms / 1000.0))
    if len(a) < fs * 2:
        return a
    a[:fs] *= np.linspace(0.0, 1.0, fs)
    a[-fs:] *= np.linspace(1.0, 0.0, fs)
    return a

def render(marked, out, speed=0.78):
    tokens = re.split(r'(\[PAUSE:\s*\d+(?:\.\d+)?\])', marked.strip())
    full = [np.zeros(int(SAMPLE_RATE * 0.25), dtype=np.float32)]
    for tok in tokens:
        tok = tok.strip()
        if not tok:
            continue
        m = re.match(r'\[PAUSE:\s*(\d+(?:\.\d+)?)\]', tok)
        if m:
            full.append(np.zeros(int(SAMPLE_RATE * float(m.group(1))), dtype=np.float32))
        else:
            clean = " ".join(tok.splitlines()).strip()
            if not clean:
                continue
            gen = pipeline(clean, voice='af_nicole', speed=speed, split_pattern=r'\n+')
            arr = [seg for _, _, seg in gen for seg in seg]
            if arr:
                full.append(apply_edge_fade(np.array(arr, dtype=np.float32), 45))
    full.append(np.zeros(int(SAMPLE_RATE * 0.35), dtype=np.float32))
    sf.write(out, np.concatenate(full), SAMPLE_RATE)

def valid_wav(path):
    try:
        info = sf.info(path)
        return info.samplerate == 24000 and info.frames > 0
    except Exception:
        return False

if __name__ == "__main__":
    print(f"Rendering {len(SCRIPTS)} Moon expanded clips...")
    for name, script in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {out}")
            continue
        print(f" -> {out}")
        render(script, out)
    print("Moon expanded clips complete!")
