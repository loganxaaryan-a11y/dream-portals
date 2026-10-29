import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
OUTPUT_DIR = "audio/desert_caravan"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS = {
    "departure_1": """
        You step through the heavy braided curtain into the nomad pavilion. [PAUSE: 2.3]
        And the thick canvas walls muffle the desert night air. [PAUSE: 2.3]
        Layers of plush wool rugs cover the sand beneath your feet... [PAUSE: 1.8]
        Absorbing every sound in the warm, enclosed tent. [PAUSE: 2.2]
        You sink down onto a wide mattress piled deep with down pillows and plush cushions. [PAUSE: 2.4]
        Outside the arched tent entrance... high red sand dunes rise up against a sea of quiet stars. [PAUSE: 2.5]
        While the sand beneath the carpets still radiates the stored solar warmth of the afternoon. [PAUSE: 2.4]
        You pull a heavy woven wool coverlet over your body... sheltered in the heart of the desert. [PAUSE: 1.8]
    """,
    "departure_2": """
        The pavilion interior is lit by a single pierced-brass lantern hanging from the central pole. [PAUSE: 2.4]
        Casting intricate star patterns across the dark canvas ceiling. [PAUSE: 2.2]
        You rest your head against the pillowed stack... [PAUSE: 1.8]
        Feeling the deep, steady warmth radiating up from the desert floor. [PAUSE: 2.2]
        Outside... a dry, gentle breeze brushes fine sand grains across the heavy outer flaps. [PAUSE: 2.4]
        Making a soft, dry sand rustle. [PAUSE: 2.2]
        Nothing here moves in a hurry... [PAUSE: 1.8] the stars wheel slowly overhead, and the tent holds you in safety. [PAUSE: 1.6]
    """,
    "departure_3": """
        Inside the cedar-framed nomad tent... the air is dry, warm, and scented with cedarwood smoke. [PAUSE: 2.4]
        You settle deep into the cushions of your low sleeping pallet. [PAUSE: 2.0]
        Letting your arms rest relaxed along your sides. [PAUSE: 2.2]
        Outside the arched doorway... the vast silence of the high desert stretches for fifty miles. [PAUSE: 2.4]
        While inside... everything is soft, dim, and deeply secure. [PAUSE: 2.2]
        You close your eyes to the brass lantern light... and let the desert night cradle you. [PAUSE: 1.6]
    """,
    "drift_01": """
        Against the taut canvas walls outside... a gentle desert breeze brushes fine sand. [PAUSE: 2.3]
        Making a soft, dry whispering sound. [PAUSE: 1.5]
    """,
    "drift_02": """
        High on the central cedar pole, the brass lantern swings a fraction of an inch... [PAUSE: 2.2]
        Casting slow, shifting star patterns across the fabric roof. [PAUSE: 1.5]
    """,
    "drift_03": """
        Beneath the stacked wool rugs, the sun-warmed sand holds a steady, soothing heat. [PAUSE: 2.3]
        Radiating comfort up through your mattress. [PAUSE: 1.5]
    """,
    "drift_04": """
        Through the open tent archway... a magnificent canopy of desert stars fills the dark sky. [PAUSE: 2.3]
        Clear... sharp... and infinite. [PAUSE: 1.5]
    """,
    "drift_05": """
        The heavy canvas flaps bow inward a fraction of an inch in an outer eddy of wind... [PAUSE: 2.3]
        And settle smoothly back into place. [PAUSE: 1.5]
    """,
    "drift_06": """
        Across the layered rugs, copper tea vessels rest in deep, quiet shadow. [PAUSE: 2.3]
        Polished and still. [PAUSE: 1.5]
    """,
    "drift_07": """
        Far out on the high dunes, a cooling night wind whispers across the ridge crest... [PAUSE: 2.3]
        Reaching your pavilion only as a soft breath. [PAUSE: 1.5]
    """,
    "drift_08": """
        Your breathing slows down, matching the gentle expansion of the canvas roof overhead. [PAUSE: 2.3]
        Warm... deep... and unhurried. [PAUSE: 1.5]
    """,
    "drift_09": """
        The scent of sun-baked earth and aged cedar timber lingers in the dry night air. [PAUSE: 2.3]
        Earthy and peaceful. [PAUSE: 1.5]
    """,
    "drift_10": """
        Outside the pavilion, a single shooting star cuts a silent silver line across the Milky Way... [PAUSE: 2.4]
        Vanishing into the dark. [PAUSE: 1.5]
    """,
    "drift_11": """
        The woven wool coverlet feels heavy and secure across your chest. [PAUSE: 2.2]
        Shielding you from the cool night outside. [PAUSE: 1.5]
    """,
    "drift_12": """
        Deep silence settles over the high red dunes, miles from any road or town. [PAUSE: 2.3]
        Absolute and undisturbed. [PAUSE: 1.5]
    """,
    "drift_13": """
        A faint amber glow from the brass lantern catches the golden weave of the side hangings. [PAUSE: 2.3]
        Soft and warm in the shadows. [PAUSE: 1.5]
    """,
    "drift_14": """
        The cedar tent poles give a tiny, natural timber sigh as the desert air cools. [PAUSE: 2.3]
        Solid and reassuring. [PAUSE: 1.5]
    """,
    "drift_15": """
        Fine grains of red sand slide an inch down the outer dune face outside the flap... [PAUSE: 2.4]
        And come to rest in the quiet night. [PAUSE: 1.5]
    """,
    "drift_16": """
        Your muscles let go of their last tension, sinking fully into the pillowed stack. [PAUSE: 2.3]
        Supported completely. [PAUSE: 1.5]
    """,
    "drift_17": """
        The immense open space of the desert outside creates a feeling of total freedom. [PAUSE: 2.3]
        Nothing to carry, nothing to solve. [PAUSE: 1.5]
    """,
    "drift_18": """
        The fabric walls breathe inward and outward with a slow, rhythmic pulse. [PAUSE: 2.3]
        Alive and calm. [PAUSE: 1.5]
    """,
    "drift_19": """
        Starlight spills across the smooth sand outside the entrance like a silver carpet. [PAUSE: 2.3]
        Reaching toward your door. [PAUSE: 1.5]
    """,
    "drift_20": """
        The dry desert warmth holds you in a safe, quiet cocoon. [PAUSE: 2.2]
        Far away from the noise of the world. [PAUSE: 1.5]
    """,
    "drift_21": """
        A soft eddy of air stirs the edge of the braided doorway curtain... [PAUSE: 2.3]
        Then drops back into stillness. [PAUSE: 1.5]
    """,
    "drift_22": """
        The brass lantern flame burns with an unblinking, golden drop of light. [PAUSE: 2.3]
        Guiding your rest. [PAUSE: 1.5]
    """,
    "drift_23": """
        Deep beneath the rugs, the warm earth provides a steady, ancient foundation. [PAUSE: 2.3]
        Unchanging through the night. [PAUSE: 1.5]
    """,
    "drift_24": """
        Your eyelids grow heavy as the desert breeze softens to a silent hush. [PAUSE: 2.3]
        Drifting toward sleep. [PAUSE: 1.5]
    """,
    "drift_25": """
        The vast, starry sky stretches from horizon to horizon above the canvas roof. [PAUSE: 2.3]
        Holding your tent in the center of the universe. [PAUSE: 1.5]
    """,
    "drift_26": """
        The heavy wool coverlet wraps closer around your shoulders. [PAUSE: 2.2]
        Cozy and secure. [PAUSE: 1.5]
    """,
    "drift_27": """
        Out on the dunes, the night is so quiet you can hear the rhythm of your own breathing. [PAUSE: 2.4]
        Slow... steady... and deep. [PAUSE: 1.5]
    """,
    "drift_28": """
        The shadows on the tent ceiling blur together into peaceful dark softness. [PAUSE: 2.3]
        Nothing left to watch. [PAUSE: 1.5]
    """,
    "drift_29": """
        The desert nomad tent rests silently under the constellations... [PAUSE: 2.3]
        Carrying you safely through the night. [PAUSE: 1.5]
    """,
    "drift_30": """
        Sleep descends like the warm desert night... [PAUSE: 1.8] absolute, deep, and restorative. [PAUSE: 1.8]
    """,
    "lucid_seed_1": """
        As the warm desert wind brushes the canvas walls... [PAUSE: 2.2]
        Your body sleeps deeply... while a calm awareness rests inside the dream. [PAUSE: 2.4]
        Knowing softly... [PAUSE: 1.8] that you are dreaming. [PAUSE: 1.8]
    """,
    "lucid_seed_2": """
        Whenever you notice the starry desert sky later tonight... [PAUSE: 2.2]
        You will recognize gently that this nomad tent is a dream... [PAUSE: 2.0]
        Safe... warm... and deeply asleep. [PAUSE: 1.8]
    """,
    "lucid_seed_3": """
        The high red dunes have folded quietly into your dream world. [PAUSE: 2.2]
        And you can rest inside the quiet pavilion... [PAUSE: 1.8] knowing it is all a dream. [PAUSE: 1.8]
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
    print(f"Rendering {len(SCRIPTS)} Desert Caravan clips...")
    for name, script in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {out}")
            continue
        print(f" -> {out}")
        render(script, out)
    print("Desert Caravan clips complete!")
