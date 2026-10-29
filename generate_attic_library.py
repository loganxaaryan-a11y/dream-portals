import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
OUTPUT_DIR = "audio/attic_library"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS = {
    "departure_1": """
        You slip through the heavy oak door... into the warm attic reading loft. [PAUSE: 2.3]
        And the brass latch clicks quietly into place. [PAUSE: 2.3]
        Thick wool rugs muffle every footstep across the dark timber floorboards. [PAUSE: 2.2]
        You sink into a wide, corduroy-lined daybed tucked directly beneath the sloped glass skylight. [PAUSE: 2.4]
        Outside the slanted panes... steady midnight rain patters a soft, continuous rhythm against the glass. [PAUSE: 2.5]
        While inside the vaulted room... rows of ancient leather-bound books absorb all outside noise. [PAUSE: 2.4]
        Beside your bed... a small cast-iron hearth radiates a gentle, dry heat into the evening air. [PAUSE: 2.4]
        You pull a heavy knitted quilt over your legs... sheltered entirely from the storm outside. [PAUSE: 1.8]
    """,
    "departure_2": """
        The attic lamps are turned low to a warm amber glow reflecting off polished oak shelves. [PAUSE: 2.4]
        You rest your head against the bolstered cushions... [PAUSE: 1.8]
        And watch single raindrops trace silver paths down the sloping skylight overhead. [PAUSE: 2.4]
        The storm outside is distant and muffled... turned into a soothing white blanket by the steep slate roof. [PAUSE: 2.5]
        In the corner hearth... red embers settle with a tiny, drowsy crackle. [PAUSE: 2.3]
        Nothing here requires your attention... [PAUSE: 1.8] the books are closed, the fire is banked, and the night is safe. [PAUSE: 1.6]
    """,
    "departure_3": """
        Inside the timber-beamed alcove... the air smells faintly of old paper, cedar, and warm iron. [PAUSE: 2.4]
        You settle deep into the cushions of the reading couch. [PAUSE: 2.0]
        Letting your arms rest relaxed along your sides. [PAUSE: 2.2]
        Above the sloped glass... the dark night sky pours steady rain over the old house. [PAUSE: 2.3]
        While down in your sheltered corner... everything is dry, still, and profoundly quiet. [PAUSE: 2.4]
        You close your eyes to the amber light... and let the storm carry you away. [PAUSE: 1.6]
    """,
    "drift_01": """
        Against the slanted skylight overhead... steady raindrops patter a soft, unbroken rhythm. [PAUSE: 2.3]
        Washing the dark glass clean. [PAUSE: 1.5]
    """,
    "drift_02": """
        Deep in the small iron hearth... a glowing ember shifts its position with a tiny, muffled snap. [PAUSE: 2.3]
        Releasing a wave of dry warmth. [PAUSE: 1.5]
    """,
    "drift_03": """
        Along the high oak rafters... shadows stretch long and slow in the amber lamplight. [PAUSE: 2.3]
        Completely still and peaceful. [PAUSE: 1.5]
    """,
    "drift_04": """
        A loose page in an open folio on the nearby desk... flutters once in a stray thermal current. [PAUSE: 2.3]
        And settles back down. [PAUSE: 1.5]
    """,
    "drift_05": """
        The heavy slate roof tiles outside absorb the force of the midnight rain... [PAUSE: 2.2]
        Turning the storm into a deep, gentle hum. [PAUSE: 1.6]
    """,
    "drift_06": """
        Rows of leather-bound volumes line the walls from floor to ceiling... [PAUSE: 2.2]
        Holding centuries of quiet knowledge in the dark. [PAUSE: 1.5]
    """,
    "drift_07": """
        Across the dark timber floor... your daybed rests surrounded by soft wool runners. [PAUSE: 2.3]
        Shielded from every draft. [PAUSE: 1.5]
    """,
    "drift_08": """
        Through the raindrops on the skylight... a single pale cloud drifts across the night sky. [PAUSE: 2.3]
        Unseen by the rest of the sleeping house. [PAUSE: 1.5]
    """,
    "drift_09": """
        The air in the attic loft is warm, dry, and heavy with the scent of old paper. [PAUSE: 2.3]
        Breathing slowly around you. [PAUSE: 1.5]
    """,
    "drift_10": """
        A tiny gust of wind brushes the chimney stack... [PAUSE: 1.8]
        Flicking the hearth flames into a momentary, golden dance. [PAUSE: 1.6]
    """,
    "drift_11": """
        Beneath the thick wool rug... the solid pine floorboards hold the house steady against the wind. [PAUSE: 2.3]
        Firm and unmoving. [PAUSE: 1.5]
    """,
    "drift_12": """
        Your breathing settles into the same slow tempo... as the steady rain on the glass. [PAUSE: 2.3]
        Deep... rhythmic... and calm. [PAUSE: 1.5]
    """,
    "drift_13": """
        On the small cast-iron stove... a tiny speck of soot shifts in the gentle heat. [PAUSE: 2.3]
        Falling silently into the ash tray. [PAUSE: 1.5]
    """,
    "drift_14": """
        The corduroy cushions around your shoulders... hold a cozy, familiar warmth. [PAUSE: 2.2]
        While the rain taps its sleepy lullaby above. [PAUSE: 1.5]
    """,
    "drift_15": """
        Along the high gable wall... the shadows of book spines blur together in the dusk. [PAUSE: 2.3]
        Resting in profound quiet. [PAUSE: 1.5]
    """,
    "drift_16": """
        A heavier gust of rain sweeps across the roof slope... [PAUSE: 2.0]
        Swelling the patter on the glass before fading back to a whisper. [PAUSE: 1.6]
    """,
    "drift_17": """
        On the reading table, a soft ember glow warms the brass lamp... [PAUSE: 2.3]
        Glowing gently through the peaceful hours. [PAUSE: 1.5]
    """,
    "drift_18": """
        The attic room feels like a tiny island... floating high above the wet world below. [PAUSE: 2.3]
        Safe and dry. [PAUSE: 1.5]
    """,
    "drift_19": """
        A gentle wave of heat rolls out from the iron hearth... [PAUSE: 2.0]
        Warming the hem of your knitted quilt. [PAUSE: 1.6]
    """,
    "drift_20": """
        Every thought of tomorrow dissolves away... into the steady drumming of the rain. [PAUSE: 2.3]
        Nothing left to hold. [PAUSE: 1.5]
    """,
    "drift_21": """
        The old oak beams overhead settle fractionally in the damp night air. [PAUSE: 2.2]
        Creaking with a dry, ancient timber sigh. [PAUSE: 1.5]
    """,
    "drift_22": """
        Stacks of unread folios rest in quiet corners of the room... [PAUSE: 2.2]
        Waiting patiently for another day. [PAUSE: 1.5]
    """,
    "drift_23": """
        The contrast between the cold storm outside... and the deep dry warmth of the loft... [PAUSE: 2.4]
        Makes your bed feel entirely secure. [PAUSE: 1.5]
    """,
    "drift_24": """
        A single droplet runs the full length of the sloping skylight... [PAUSE: 2.2]
        And vanishes into the copper window frame. [PAUSE: 1.5]
    """,
    "drift_25": """
        The amber lamplight catches the fine weave of your wool blanket. [PAUSE: 2.3]
        Glowing softly in the shadows. [PAUSE: 1.5]
    """,
    "drift_26": """
        Outside the slate roof, the wind drops to a soft, even sigh... [PAUSE: 2.2]
        Leaving only the steady rain. [PAUSE: 1.5]
    """,
    "drift_27": """
        High in the peak of the roof, the rafters cradle the warm air of the room. [PAUSE: 2.3]
        Holding the peace of the night. [PAUSE: 1.5]
    """,
    "drift_28": """
        The rain patter on the glass blurs into an unbroken cushion of sound. [PAUSE: 2.3]
        Carrying you toward sleep. [PAUSE: 1.5]
    """,
    "drift_29": """
        Your eyelids grow heavy as the fire embers dim to a soft, dark red. [PAUSE: 2.2]
        Safe within the walls of books. [PAUSE: 1.5]
    """,
    "drift_30": """
        The attic library rests quietly in the heart of the storm... [PAUSE: 2.0]
        Holding you safe until morning. [PAUSE: 1.6]
    """,
    "lucid_seed_1": """
        As the rain taps softly on the glass above... [PAUSE: 2.2]
        Your body sleeps deeply... while a calm awareness rests inside the dream. [PAUSE: 2.4]
        Knowing softly... [PAUSE: 1.8] that you are dreaming. [PAUSE: 1.8]
    """,
    "lucid_seed_2": """
        Whenever you notice the rain falling on the skylight later tonight... [PAUSE: 2.2]
        You will recognize gently that this attic library is a dream... [PAUSE: 2.0]
        Safe... warm... and deeply asleep. [PAUSE: 1.8]
    """,
    "lucid_seed_3": """
        The vaulted library has folded quietly into your dream world. [PAUSE: 2.2]
        And you can rest inside the warm shadows... [PAUSE: 1.8] knowing it is all a dream. [PAUSE: 1.8]
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
    print(f"Rendering {len(SCRIPTS)} Attic Library clips...")
    for name, script in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {out}")
            continue
        print(f" -> {out}")
        render(script, out)
    print("Attic Library clips complete!")
