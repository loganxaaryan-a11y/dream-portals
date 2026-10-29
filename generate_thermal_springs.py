import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
OUTPUT_DIR = "audio/thermal_springs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS = {
    "departure_1": """
        You slide shut the cedar lattice screen... with a muted wooden click. [PAUSE: 2.2]
        Inside the private mountain pavilion... the air is rich with warm mineral steam. [PAUSE: 2.4]
        You recline on the wide floor cushion of woven reed... [PAUSE: 1.8]
        Wrapped in a thick, dry linen robe. [PAUSE: 2.3]
        Just beyond the open timber eaves... a natural rock pool brims with steaming spring water. [PAUSE: 2.5]
        And past the dark boulders... slow mountain snow falls silently into the mist. [PAUSE: 2.3]
        You are enclosed in deep cedar warmth... watching the quiet winter night from inside. [PAUSE: 1.6]
    """,
    "departure_2": """
        The wooden floor beneath your cushion... is heated from below by the natural thermal rock. [PAUSE: 2.4]
        Radiating a steady, gentle warmth up through your back and shoulders. [PAUSE: 2.2]
        Through the wide viewing opening... ribbons of white vapor rise off the dark stone pool. [PAUSE: 2.4]
        A hollowed bamboo spout at the edge of the basin... pours a continuous, muffled stream of hot spring water. [PAUSE: 2.5]
        Never changing its pitch... and never stopping. [PAUSE: 2.0]
        Outside in the pine forest... the snow absorbs every other sound for miles. [PAUSE: 1.6]
    """,
    "departure_3": """
        Low paper lanterns sit tucked in the corners of the cedar pavilion. [PAUSE: 2.2]
        Glowing like dim amber embers against the unpainted wood. [PAUSE: 2.2]
        You rest your head on the firm buckwheat pillow... [PAUSE: 1.8]
        Pulling the heavy quilted duvet over your chest. [PAUSE: 2.3]
        Outside the timber sill... the steaming thermal pool mirrors the dark mountain sky. [PAUSE: 2.4]
        While slow flakes of snow drift down... vanishing the moment they touch the warm water. [PAUSE: 2.3]
        There is nothing left to do tonight... except breathe the warm cedar air. [PAUSE: 1.6]
    """,
    "drift_01": """
        Thick clouds of white steam... curl lazily off the surface of the dark stone pool. [PAUSE: 2.3]
        Floating upward into the cold night air. [PAUSE: 1.5]
    """,
    "drift_02": """
        Large, slow snowflakes drift down between the dark pine branches... [PAUSE: 2.2]
        Melting silently into the warm mineral water. [PAUSE: 1.5]
    """,
    "drift_03": """
        From the bamboo spout... a smooth ribbon of hot water pours into the basin. [PAUSE: 2.3]
        Blending seamlessly into the pool. [PAUSE: 1.5]
    """,
    "drift_04": """
        The scent of wet Japanese cedar... rises gently on the humid breeze. [PAUSE: 2.2]
        Clean... woody... and grounding. [PAUSE: 1.5]
    """,
    "drift_05": """
        Along the edge of the pool... smooth black river stones glisten in the lantern light. [PAUSE: 2.3]
        Half covered in warm water... and half dusted with snow. [PAUSE: 1.5]
    """,
    "drift_06": """
        Beneath your back... the heated timber floor holds a steady, comforting warmth. [PAUSE: 2.3]
        Loosening every muscle along your spine. [PAUSE: 1.5]
    """,
    "drift_07": """
        A thin veil of vapor... drifts past the cedar eaves of your pavilion. [PAUSE: 2.2]
        Turning the paper lantern glow into a soft golden halo. [PAUSE: 1.5]
    """,
    "drift_08": """
        High on the ridge across the valley... dark fir trees stand heavy with fresh powder. [PAUSE: 2.3]
        Completely still in the windless night. [PAUSE: 1.5]
    """,
    "drift_09": """
        Warm water overflows the smooth slate lip of the pool... [PAUSE: 2.0]
        Gliding in a thin sheet across the stone drain. [PAUSE: 1.8]
    """,
    "drift_10": """
        Inside the paper lantern... the dim light never wavers. [PAUSE: 2.2]
        Sheltered by the deep wooden roof. [PAUSE: 1.5]
    """,
    "drift_11": """
        A cushion of white snow... rests six inches deep on the stone lantern beside the pool. [PAUSE: 2.3]
        Rounded and untouched. [PAUSE: 1.5]
    """,
    "drift_12": """
        Ripples spread slowly across the dark mineral water... [PAUSE: 2.0]
        Catching a faint copper reflection from the pavilion eaves. [PAUSE: 1.8]
    """,
    "drift_13": """
        Your breathing slows... matching the unhurried rise of steam above the rocks. [PAUSE: 2.3]
        Effortless... and deep. [PAUSE: 1.5]
    """,
    "drift_14": """
        The woven reed mat beneath your futon cushion... feels firm and dry. [PAUSE: 2.2]
        Holding the gentle heat of the mountain spring below. [PAUSE: 1.5]
    """,
    "drift_15": """
        Out in the dark garden... a pine bough settles an inch lower under its blanket of snow. [PAUSE: 2.4]
        Without making a sound. [PAUSE: 1.5]
    """,
    "drift_16": """
        Warm humidity softens the air at the edge of the veranda... [PAUSE: 2.2]
        Meeting the crisp winter night in a slow swirl of mist. [PAUSE: 1.5]
    """,
    "drift_17": """
        Small bubbles of warm spring water... rise from the sandy bottom of the rock basin. [PAUSE: 2.3]
        Drifting quietly to the surface. [PAUSE: 1.5]
    """,
    "drift_18": """
        The heavy cedar beams overhead... rest solid and dark in the shadows. [PAUSE: 2.2]
        Holding the snow high above you. [PAUSE: 1.5]
    """,
    "drift_19": """
        Across the water... damp green moss clings to the warm side of a granite boulder. [PAUSE: 2.3]
        Untouched by the winter frost. [PAUSE: 1.5]
    """,
    "drift_20": """
        Every sound beyond the valley... is muffled by miles of deep mountain snow. [PAUSE: 2.3]
        Leaving only the steady flow of the spring. [PAUSE: 1.5]
    """,
    "drift_21": """
        Snowflakes catch the amber light as they drift past the eaves... [PAUSE: 2.2]
        Looking like slow sparks floating downward. [PAUSE: 1.5]
    """,
    "drift_22": """
        The heavy linen robe around your shoulders... feels warm as sunlight. [PAUSE: 2.2]
        Resting lightly against your skin. [PAUSE: 1.5]
    """,
    "drift_23": """
        Where the hot spring meets the snowy bank... a narrow circle of bare earth stays warm and dark. [PAUSE: 2.4]
        Breathing thin wisps of vapor. [PAUSE: 1.5]
    """,
    "drift_24": """
        The wooden lattice screen behind you... shuts out the rest of the world completely. [PAUSE: 2.3]
        Leaving only this quiet sanctuary. [PAUSE: 1.5]
    """,
    "drift_25": """
        Across the dark surface of the pool... steam drifts from left to right in a slow current. [PAUSE: 2.3]
        Smoothing out every ripple. [PAUSE: 1.5]
    """,
    "drift_26": """
        A single drop of condensation... slides smoothly down the oiled cedar post. [PAUSE: 2.2]
        Glistening in the dim glow. [PAUSE: 1.5]
    """,
    "drift_27": """
        High above the steam clouds... a clear patch of night sky shows a handful of pale stars. [PAUSE: 2.4]
        Silent above the white peaks. [PAUSE: 1.5]
    """,
    "drift_28": """
        The continuous hush of the bamboo spout... blurs into a single, soothing drone. [PAUSE: 2.3]
        Washing away the last trace of thought. [PAUSE: 1.5]
    """,
    "drift_29": """
        Warmth settles deep into your hands and feet... under the heavy quilt. [PAUSE: 2.2]
        Nothing left to hold onto. [PAUSE: 1.5]
    """,
    "drift_30": """
        Steam and snow mingle together in the amber dusk... [PAUSE: 2.0]
        Until the edge of the pool softens into the night. [PAUSE: 1.8]
    """,
    "lucid_seed_1": """
        As the warm steam drifts through the winter night... [PAUSE: 2.2]
        Your body sinks into deep sleep... while a quiet spark of awareness remains. [PAUSE: 2.4]
        Knowing softly... [PAUSE: 1.8] that you are now dreaming. [PAUSE: 1.8]
    """,
    "lucid_seed_2": """
        If you notice the rising mist later tonight... [PAUSE: 2.0]
        You will recognize gently that this sanctuary is a dream... [PAUSE: 2.2]
        Safe... warm... and deeply asleep. [PAUSE: 1.8]
    """,
    "lucid_seed_3": """
        The mountain pavilion is folding quietly into your dream. [PAUSE: 2.2]
        And you can rest inside it... [PAUSE: 1.8] knowing it is all a dream. [PAUSE: 1.8]
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
    print(f"Rendering {len(SCRIPTS)} Thermal Springs clips...")
    for name, script in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {out}")
            continue
        print(f" -> {out}")
        render(script, out)
    print("Thermal Springs clips complete!")
