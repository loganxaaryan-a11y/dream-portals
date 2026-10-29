import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
OUTPUT_DIR = "audio/nebula_cruiser"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS = {
    "departure_1": """
        You slide into the padded observation berth... deep inside the star cruiser. [PAUSE: 2.3]
        And the heavy acoustic hatch seals softly behind you. [PAUSE: 2.3]
        Brushed aluminum panels absorb every stray vibration... along the curved hull. [PAUSE: 2.2]
        You rest your head against the velvet-lined headrest... facing the massive viewport. [PAUSE: 2.3]
        Far out beyond the glass... the ship glides silently through a vast interstellar dust cloud. [PAUSE: 2.4]
        While the ion drive purrs a deep, grounding vibration through the metal frame. [PAUSE: 2.3]
        Outside... curtains of violet and teal starlight drift past like slow smoke. [PAUSE: 2.4]
        Floating through the quiet dark... with infinite space to rest. [PAUSE: 1.6]
    """,
    "departure_2": """
        The cabin lights are dimmed to a faint copper glow along the floor trim. [PAUSE: 2.3]
        You pull a heavy thermal blanket up over your shoulders... [PAUSE: 1.8]
        And settle your weight into the contour mattress. [PAUSE: 2.2]
        The cruiser floats far outside any shipping lane... where the space is calm and completely still. [PAUSE: 2.4]
        Through the multi-layered glass... starlight paints soft prismatic rings across the ceiling. [PAUSE: 2.5]
        Only a warm, rhythmic life-support hum reaches your berth... [PAUSE: 2.0]
        Holding you suspended between the stars and sleep. [PAUSE: 1.6]
    """,
    "departure_3": """
        Inside the private stateroom... the night watch is quiet and undisturbed. [PAUSE: 2.2]
        You settle into the corner berth beside the wide viewing shield. [PAUSE: 2.0]
        Resting your hands flat against the soft quilt. [PAUSE: 2.3]
        Outside... the great vessel drifts forward on pure momentum. [PAUSE: 2.3]
        No alarms... no course adjustments... and no sudden movement. [PAUSE: 2.2]
        Just the endless luminous dust cloud outside... and the deep warmth of the cabin around you. [PAUSE: 2.0]
    """,
    "drift_01": """
        Beyond the thick viewport... an immense curtain of violet dust rolls slowly past. [PAUSE: 2.3]
        Glowing like dim iridescent fog. [PAUSE: 1.5]
    """,
    "drift_02": """
        Far down the corridor spine... the main ion drive hums a deep, unchanging note. [PAUSE: 2.3]
        Muffled by heavy bulkhead insulation. [PAUSE: 1.5]
    """,
    "drift_03": """
        The shadow of the cruiser's communication array... glides silently across a luminous gas cloud. [PAUSE: 2.3]
        Smooth and unhurried. [PAUSE: 1.5]
    """,
    "drift_04": """
        Along the rim of the viewport... a recessed LED strip casts a thin line of amber light. [PAUSE: 2.3]
        Steady in the dim stateroom. [PAUSE: 1.5]
    """,
    "drift_05": """
        The automated steering dampeners correct by a fraction of a degree... [PAUSE: 1.8] and settle smoothly back. [PAUSE: 2.0]
    """,
    "drift_06": """
        Wisps of faint nebular gas... brush past the outer silicate shield like silent breath. [PAUSE: 2.3]
        Dissolving into the starfields. [PAUSE: 1.5]
    """,
    "drift_07": """
        Across the compact stateroom... spare storage lockers rest in deep, quiet shadow. [PAUSE: 2.3]
        Facing the wide window. [PAUSE: 1.5]
    """,
    "drift_08": """
        Through a gap in the luminous dust... a distant cluster of white stars glimmers once... [PAUSE: 2.4]
        And drifts slowly toward the stern. [PAUSE: 1.5]
    """,
    "drift_09": """
        The dark void beyond the nebula... looks like deep indigo glass dusted with diamond chips. [PAUSE: 2.3]
        Clear... and completely still. [PAUSE: 1.5]
    """,
    "drift_10": """
        Warm environmental air rises gently from the floor vents beneath the glass. [PAUSE: 2.2]
        Keeping the cabin climate perfectly balanced. [PAUSE: 1.5]
    """,
    "drift_11": """
        The massive structural keel overhead... carries the stateroom without a trace of strain. [PAUSE: 2.3]
        Floating through the vacuum. [PAUSE: 1.5]
    """,
    "drift_12": """
        In the wall alcove... a tiny diagnostic indicator pulses a soft, sleepy green. [PAUSE: 2.3]
        Never changing its rhythm. [PAUSE: 1.5]
    """,
    "drift_13": """
        Towering clouds of cosmic hydrogen in the distance... look like quiet mountain ridges under the moon. [PAUSE: 2.4]
        Drifting past the frame. [PAUSE: 1.5]
    """,
    "drift_14": """
        Your mattress absorbs the faint, steady pulse of the sub-space generators. [PAUSE: 2.2]
        Like a deep, resting heartbeat. [PAUSE: 1.5]
    """,
    "drift_15": """
        The ship passes through a thin patch of stellar drift... [PAUSE: 2.0]
        Softening the starlight into a warm amber haze for a few quiet moments. [PAUSE: 2.0]
    """,
    "drift_16": """
        Then the haze thins... [PAUSE: 1.6] and the open crystal starfield returns above the deck. [PAUSE: 2.0]
    """,
    "drift_17": """
        On the small alloy console table... an unsealed data pad rests completely motionless. [PAUSE: 2.2]
        Not a millimeter out of place. [PAUSE: 1.5]
    """,
    "drift_18": """
        Filtered ventilation air whispers softly through the ceiling grates. [PAUSE: 2.3]
        Barely audible in the quiet room. [PAUSE: 1.5]
    """,
    "drift_19": """
        Prismatic starlight paints long, soft rectangles across the acoustic wall padding. [PAUSE: 2.2]
        Resting still beside your head. [PAUSE: 1.5]
    """,
    "drift_20": """
        All the schedules and charts of the fleet... lie light-years behind you now. [PAUSE: 2.3]
        Unable to reach you here. [PAUSE: 1.5]
    """,
    "drift_21": """
        The reinforced alloy beams of the cabin... give a tiny, comforting flex in the thermal gradient. [PAUSE: 2.3]
        Safe and solid. [PAUSE: 1.5]
    """,
    "drift_22": """
        Out on the starboard stabilization fin... a navigation beacon glows softly, steady and unhurried. [PAUSE: 2.3]
        Calm and regular. [PAUSE: 1.5]
    """,
    "drift_23": """
        The heavy thermal blanket over your chest... rises and falls with your slow breathing. [PAUSE: 2.3]
        Warm and unhurried. [PAUSE: 1.5]
    """,
    "drift_24": """
        Valleys of soft magnetic shadow... fold between the glowing clouds of the nebula. [PAUSE: 2.3]
        Drifting silently underneath. [PAUSE: 1.5]
    """,
    "drift_25": """
        The low chord of the internal power plant... stays locked on one deep, drowsy frequency. [PAUSE: 2.3]
        Carrying you through the void. [PAUSE: 1.5]
    """,
    "drift_26": """
        Micro-frost crystals form a delicate lace border along the corner seals of the pane. [PAUSE: 2.3]
        Gleaming faintly in the starlight. [PAUSE: 1.5]
    """,
    "drift_27": """
        Down the main corridor... the engineering bays are dark and sealed for the watch. [PAUSE: 2.2]
        Still and undisturbed... for the night. [PAUSE: 1.5]
    """,
    "drift_28": """
        The path ahead is a clean, open channel where luminous dust meets dark infinity. [PAUSE: 2.3]
        Open and peaceful. [PAUSE: 1.5]
    """,
    "drift_29": """
        Your head sinks deeper into the memory-foam pillow... [PAUSE: 2.0]
        Supported evenly on all sides. [PAUSE: 1.5]
    """,
    "drift_30": """
        The star cruiser drifts on through the infinite quiet... [PAUSE: 2.0]
        With the whole galaxy to rest across. [PAUSE: 1.5]
    """,
    "lucid_seed_1": """
        As the star cruiser glides through the quiet nebula... [PAUSE: 2.2]
        Your body sleeps deeply... while a calm awareness rests inside the dream. [PAUSE: 2.4]
        Knowing softly... [PAUSE: 1.8] that you are dreaming. [PAUSE: 1.8]
    """,
    "lucid_seed_2": """
        Whenever you look out over the glowing starfields later tonight... [PAUSE: 2.2]
        You will know gently that you are inside a dream... [PAUSE: 2.0]
        Floating safely... and deeply asleep. [PAUSE: 1.8]
    """,
    "lucid_seed_3": """
        The silent space outside has become your dream world. [PAUSE: 2.2]
        And you can drift through it effortlessly... [PAUSE: 1.8] knowing it is all a dream. [PAUSE: 1.8]
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
    print(f"Rendering {len(SCRIPTS)} Nebula Cruiser clips...")
    for name, script in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {out}")
            continue
        print(f" -> {out}")
        render(script, out)
    print("Nebula Cruiser clips complete!")
