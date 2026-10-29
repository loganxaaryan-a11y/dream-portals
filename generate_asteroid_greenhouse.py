import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
OUTPUT_DIR = "audio/asteroid_greenhouse"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS = {
    # --- 3 ROTATING DEPARTURES ---
    "departure_1": """
        You step through the curved glass partition... into the warm sleeping alcove of the orbital conservatory. [PAUSE: 2.4]
        And the bronze door seals softly behind you. [PAUSE: 2.3]
        Around your cushioned hemp daybed... giant ferns and broad-leafed palms arch up toward the geodesic glass dome. [PAUSE: 2.5]
        Above the canopy... the black night of space is dusted with quiet, unblinking stars. [PAUSE: 2.3]
        While inside the dome... the air is humid, warm, and rich with the scent of damp earth and night blossoms. [PAUSE: 2.5]
        High in the branches... fine misting nozzles breathe a gentle veil of warm vapor over the leaves. [PAUSE: 2.4]
        And beside your bed... a narrow stone rill carries a steady trickle of clear water through the moss. [PAUSE: 2.4]
        You sink back into the deep cushions... cradled inside a living garden that floats through the quiet dark. [PAUSE: 1.8]
    """,
    "departure_2": """
        The conservatory's night lamps are dimmed to a soft amber glow along the terracotta garden paths. [PAUSE: 2.4]
        You stretch out on the wide woven lounger... tucked inside a bower of broad banana leaves. [PAUSE: 2.3]
        Pulling a soft cotton blanket over your chest. [PAUSE: 2.0]
        Beneath the stone floor... the station's climate system hums a deep, grounding chord. [PAUSE: 2.3]
        Keeping the garden at the exact warmth of a tropical summer evening. [PAUSE: 2.2]
        Through the glass ribs of the dome overhead... a pale silver nebula drifts slowly across the sky. [PAUSE: 2.4]
        Nothing here ever hurries... [PAUSE: 1.8] the plants grow, the water flows, and the night stays still. [PAUSE: 1.6]
    """,
    "departure_3": """
        Inside the glasshouse sanctuary... the air circulation vents create a soft, continuous breeze through the leaves. [PAUSE: 2.4]
        You settle into the deep recessed sofa beside the mossy rock basin. [PAUSE: 2.2]
        Listening to the gentle patter of water drops falling from leaf to leaf. [PAUSE: 2.3]
        Outside the thick faceted dome... the silent void of space stretches without a sound. [PAUSE: 2.3]
        Inside... you are surrounded by warm greenery, trickling water, and soft amber light. [PAUSE: 2.3]
        Completely sheltered... with the whole night to rest. [PAUSE: 1.6]
    """,

    # --- 30 STANDALONE MICRO-DRIFTS ---
    "drift_01": """
        High in the bronze rafters... the misting nozzles release a soft cloud of warm vapor. [PAUSE: 2.3]
        Settling silently over the broad green canopy. [PAUSE: 1.5]
    """,
    "drift_02": """
        Through the faceted glass dome overhead... the Milky Way glows like a pale silver cloud. [PAUSE: 2.3]
        Framed by dark palm fronds. [PAUSE: 1.5]
    """,
    "drift_03": """
        Beside your alcove... clear water trickles smoothly over rounded river pebbles in the stone rill. [PAUSE: 2.4]
        Never changing its gentle song. [PAUSE: 1.5]
    """,
    "drift_04": """
        A slow, warm draft from the air louvers... stirs the broad monstera leaves around your bed. [PAUSE: 2.3]
        With a soft, papery rustle. [PAUSE: 1.5]
    """,
    "drift_05": """
        Single drops of condensation... slide down the waxy tip of a fern leaf... [PAUSE: 2.2]
        And tap softly into the damp moss below. [PAUSE: 1.5]
    """,
    "drift_06": """
        Beneath the terracotta tiles... the deep environmental hum holds a steady, comforting warmth. [PAUSE: 2.3]
        Keeping the garden alive and still. [PAUSE: 1.5]
    """,
    "drift_07": """
        White night-blooming jasmine flowers... open along the bronze trellis beside you. [PAUSE: 2.3]
        Filling the warm air with a sweet, sleepy scent. [PAUSE: 1.5]
    """,
    "drift_08": """
        The great conservatory rotates at a barely perceptible pace... [PAUSE: 2.2]
        Causing the stars above the glass to drift an inch to the left. [PAUSE: 1.6]
    """,
    "drift_09": """
        Low amber path lights... glow softly beneath the wet fern fronds. [PAUSE: 2.2]
        Turning the rising mist into warm gold dust. [PAUSE: 1.5]
    """,
    "drift_10": """
        In the warm moss along the stream bank... a single greenhouse cricket trills softly. [PAUSE: 2.3]
        Tucked safely under the leaves. [PAUSE: 1.5]
    """,
    "drift_11": """
        Outside the thick glass panels... the silver curve of a distant moon hangs still in the dark. [PAUSE: 2.4]
        Washing the upper leaves in pale light. [PAUSE: 1.5]
    """,
    "drift_12": """
        Your woven daybed gives gently under your weight... [PAUSE: 2.0]
        Supporting every muscle from head to toe. [PAUSE: 1.6]
    """,
    "drift_13": """
        Broad lotus pads float in the small stone reflection pool at the center of the dome. [PAUSE: 2.3]
        Still as green glass. [PAUSE: 1.5]
    """,
    "drift_14": """
        A fine veil of warm mist... drifts past the amber lantern beside your alcove. [PAUSE: 2.2]
        Dissolving into the humid air. [PAUSE: 1.5]
    """,
    "drift_15": """
        The bronze ribs of the dome arch high overhead... [PAUSE: 2.0]
        Strong, solid, and glistening with dew. [PAUSE: 1.6]
    """,
    "drift_16": """
        Water flows from a small terracotta spout... into a cushion of thick green moss. [PAUSE: 2.3]
        Making a muffled, liquid hush. [PAUSE: 1.5]
    """,
    "drift_17": """
        Hanging air-plants sway a fraction of an inch in the gentle circulation breeze. [PAUSE: 2.3]
        Weightless in the dim glow. [PAUSE: 1.5]
    """,
    "drift_18": """
        The scent of warm soil... wet stone... and green leaves wraps around your bed like a blanket. [PAUSE: 2.4]
        Earthy and calm. [PAUSE: 1.5]
    """,
    "drift_19": """
        High on the outer glass... starlight refracts through tiny beads of moisture. [PAUSE: 2.3]
        Sparkling softly like distant fireflies. [PAUSE: 1.5]
    """,
    "drift_20": """
        Your breathing slows... matching the gentle rhythm of the misting cycle overhead. [PAUSE: 2.3]
        Warm... deep... and effortless. [PAUSE: 1.5]
    """,
    "drift_21": """
        Along the curving garden path... smooth flagstones glisten darkly with moisture. [PAUSE: 2.2]
        Untrodden and quiet for the night. [PAUSE: 1.5]
    """,
    "drift_22": """
        Giant tree ferns arch over your sleeping nook like a green roof within a roof. [PAUSE: 2.3]
        Shading your eyes in soft shadow. [PAUSE: 1.5]
    """,
    "drift_23": """
        The contrast between the cold stars outside... and the lush tropical warmth inside... [PAUSE: 2.3]
        Makes your bed feel deeply secure. [PAUSE: 1.5]
    """,
    "drift_24": """
        A tiny ripple crosses the stone basin... as a single drop falls from an orchid leaf. [PAUSE: 2.3]
        Widening until the water is flat again. [PAUSE: 1.5]
    """,
    "drift_25": """
        Warm air rises from the terracotta floor grates... [PAUSE: 2.0]
        Blending into the soft hush of the water rill. [PAUSE: 1.6]
    """,
    "drift_26": """
        Climbing vines wrap around the bronze pillars... [PAUSE: 2.0]
        Their dark leaves resting still against the metal. [PAUSE: 1.6]
    """,
    "drift_27": """
        Far out beyond the dome... a silent stream of stardust drifts across the black sky. [PAUSE: 2.3]
        While the garden inside stays warm and unchanged. [PAUSE: 1.5]
    """,
    "drift_28": """
        The cotton blanket rests lightly over your shoulders... [PAUSE: 2.0]
        Dry and cozy in the soft garden air. [PAUSE: 1.6]
    """,
    "drift_29": """
        The misting nozzles fade to a gentle whisper... [PAUSE: 2.0]
        Leaving the leaves damp and gleaming in the amber dusk. [PAUSE: 1.6]
    """,
    "drift_30": """
        The living garden breathes quietly around you... [PAUSE: 2.0]
        Carrying your sleeping alcove smoothly through the stars. [PAUSE: 1.6]
    """,

    # --- 3 ROTATING LUCID SEEDS ---
    "lucid_seed_1": """
        As the warm garden floats among the quiet stars... [PAUSE: 2.2]
        Your body sleeps deeply... while a calm awareness rests inside the dream. [PAUSE: 2.4]
        Knowing softly... [PAUSE: 1.8] that you are dreaming. [PAUSE: 1.8]
    """,
    "lucid_seed_2": """
        Whenever you notice the stars shining above the green leaves later tonight... [PAUSE: 2.2]
        You will recognize gently that this conservatory is a dream... [PAUSE: 2.0]
        Safe... warm... and deeply asleep. [PAUSE: 1.8]
    """,
    "lucid_seed_3": """
        The glasshouse around you has blossomed into the dream world. [PAUSE: 2.2]
        And you can rest inside the quiet garden... [PAUSE: 1.8] knowing it is all a dream. [PAUSE: 1.8]
    """
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
    print(f"Rendering {len(SCRIPTS)} Greenhouse clips...")
    for name, script in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {out}")
            continue
        print(f" -> {out}")
        render(script, out)
    print("Greenhouse clips complete!")
