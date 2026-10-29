import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
OUTPUT_DIR = "audio/cloud_airship"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS = {
    "departure_1": """
        You step into the quiet observation lounge... inside the belly of the night airship. [PAUSE: 2.3]
        And the heavy walnut door latches softly behind you. [PAUSE: 2.3]
        Thick wool carpet absorbs every footstep... along the curved promenade. [PAUSE: 2.2]
        You sink into a wide leather armchair... facing the slanted panoramic windows. [PAUSE: 2.3]
        Far above the gondola... the giant helium envelope holds the ship steady in the sky. [PAUSE: 2.4]
        While distant propellers hum a deep, muffled note through the timber frame. [PAUSE: 2.3]
        Below the slanted glass... an unbroken sea of silver clouds stretches to the horizon. [PAUSE: 2.4]
        Floating smoothly through the upper night... with nowhere to hurry. [PAUSE: 1.6]
    """,
    "departure_2": """
        The lounge lamps are dimmed to a faint copper glow... so you can see the sky outside. [PAUSE: 2.3]
        You rest your legs on the padded ottoman... [PAUSE: 1.8]
        And tuck a warm wool throw around your waist. [PAUSE: 2.2]
        The airship glides above the weather... where the air is calm and completely smooth. [PAUSE: 2.4]
        Through the double-paned glass... moonlight turns the cloud tops below into rolling hills of snow. [PAUSE: 2.5]
        Only a low, soothing vibration reaches your chair... [PAUSE: 2.0]
        Holding you suspended between the clouds and the stars. [PAUSE: 1.6]
    """,
    "departure_3": """
        Inside the wooden gondola... the night watch is quiet and still. [PAUSE: 2.2]
        You settle into the corner booth beside the wide viewing pane. [PAUSE: 2.0]
        Resting your elbow on the smooth walnut sill. [PAUSE: 2.3]
        Outside... the great ship drifts forward at an unhurried walking pace. [PAUSE: 2.3]
        No bumps... no turns... and no turbulence. [PAUSE: 2.2]
        Just the endless silver cloud deck below... and the steady warmth of the cabin around you. [PAUSE: 2.0]
    """,
    "drift_01": """
        Beneath the slanted window... an endless field of moonlit clouds rolls slowly past. [PAUSE: 2.3]
        Glowing like pale silver wool. [PAUSE: 1.5]
    """,
    "drift_02": """
        Far out on the wing strut... a distant engine pod hums a deep, unchanging note. [PAUSE: 2.3]
        Muffled by the thick cabin walls. [PAUSE: 1.5]
    """,
    "drift_03": """
        The shadow of the great airship... glides silently across the white cloud tops below. [PAUSE: 2.3]
        Smooth and unhurried. [PAUSE: 1.5]
    """,
    "drift_04": """
        Along the slanted window... a polished brass rail catches a thin line of copper lamplight. [PAUSE: 2.3]
        Steady in the dim lounge. [PAUSE: 1.5]
    """,
    "drift_05": """
        The nose of the gondola rises half a degree... [PAUSE: 1.8] and settles smoothly back on course. [PAUSE: 2.0]
    """,
    "drift_06": """
        Wisps of high cirrus mist... brush past the outer pane like silent feathers. [PAUSE: 2.3]
        Dissolving into the moonlight. [PAUSE: 1.5]
    """,
    "drift_07": """
        Across the carpeted lounge... empty leather chairs rest in deep, quiet shadow. [PAUSE: 2.3]
        Facing the wide night sky. [PAUSE: 1.5]
    """,
    "drift_08": """
        Through a narrow gap in the clouds far below... a tiny cluster of town lights glimmers once... [PAUSE: 2.4]
        And disappears beneath the white blanket. [PAUSE: 1.5]
    """,
    "drift_09": """
        The dark sky above the cloud deck... looks like deep blue velvet dusted with stars. [PAUSE: 2.3]
        Clear... and completely still. [PAUSE: 1.5]
    """,
    "drift_10": """
        Warm air rises gently from the brass floor grate beneath the window. [PAUSE: 2.2]
        Keeping the glass clear of frost. [PAUSE: 1.5]
    """,
    "drift_11": """
        The great buoyant hull overhead... carries the cabin without a trace of effort. [PAUSE: 2.3]
        Floating on the cool night air. [PAUSE: 1.5]
    """,
    "drift_12": """
        In the corner alcove... a globe lamp casts a soft amber circle on the walnut paneling. [PAUSE: 2.3]
        Never flickering. [PAUSE: 1.5]
    """,
    "drift_13": """
        Towering cloud banks in the distance... look like quiet snow-covered mountains under the moon. [PAUSE: 2.4]
        Drifting slowly to the rear. [PAUSE: 1.5]
    """,
    "drift_14": """
        Your chair absorbs the faint, steady purr of the airship frame. [PAUSE: 2.2]
        Like a deep, restful sigh. [PAUSE: 1.5]
    """,
    "drift_15": """
        The ship passes through the top of a silver cloud ridge... [PAUSE: 2.0]
        Wrapping the windows in soft, milky mist for a few quiet seconds. [PAUSE: 2.0]
    """,
    "drift_16": """
        Then the mist parts... [PAUSE: 1.6] and the open starlit sky returns above the cloud sea. [PAUSE: 2.0]
    """,
    "drift_17": """
        On the small walnut side table... an empty glass rests completely motionless. [PAUSE: 2.2]
        Not a ripple on its surface. [PAUSE: 1.5]
    """,
    "drift_18": """
        High-altitude air whispers softly along the smooth outer skin of the gondola. [PAUSE: 2.3]
        Barely audible inside. [PAUSE: 1.5]
    """,
    "drift_19": """
        Moonlight paints long, slanted rectangles across the thick wool carpet. [PAUSE: 2.2]
        Resting still beside your feet. [PAUSE: 1.5]
    """,
    "drift_20": """
        All the storms and roads of the earth... lie miles below the soft cloud floor. [PAUSE: 2.3]
        Unable to reach you here. [PAUSE: 1.5]
    """,
    "drift_21": """
        The wooden ribs of the lounge... give a tiny, gentle settle in the steady air current. [PAUSE: 2.3]
        Safe and solid. [PAUSE: 1.5]
    """,
    "drift_22": """
        Out on the tail fin... a small red position light glows steadily against the night. [PAUSE: 2.3]
        Unblinking and calm. [PAUSE: 1.5]
    """,
    "drift_23": """
        The heavy wool throw over your knees... rises and falls with your slow breathing. [PAUSE: 2.3]
        Warm and unhurried. [PAUSE: 1.5]
    """,
    "drift_24": """
        Valleys of soft grey shadow... fold between the moonlit swells of the cloud deck. [PAUSE: 2.3]
        Drifting silently underneath. [PAUSE: 1.5]
    """,
    "drift_25": """
        The pitch of the distant propellers... stays locked on one low, drowsy chord. [PAUSE: 2.3]
        Carrying you through the night. [PAUSE: 1.5]
    """,
    "drift_26": """
        Frost crystals form a tiny lace border... along the outer edge of the window frame. [PAUSE: 2.3]
        Sparkling faintly in the silver light. [PAUSE: 1.5]
    """,
    "drift_27": """
        Down the curved corridor... the lower cabins are dark and hushed. [PAUSE: 2.2]
        Still and undisturbed... for the night. [PAUSE: 1.5]
    """,
    "drift_28": """
        The horizon ahead is a single, soft line where silver clouds meet dark stars. [PAUSE: 2.3]
        Open and peaceful. [PAUSE: 1.5]
    """,
    "drift_29": """
        Your head sinks deeper into the winged leather headrest... [PAUSE: 2.0]
        Supported on both sides. [PAUSE: 1.5]
    """,
    "drift_30": """
        The airship glides on through the upper quiet... [PAUSE: 2.0]
        With the whole night sky to drift across. [PAUSE: 1.5]
    """,
    "lucid_seed_1": """
        As the airship floats above the silver clouds... [PAUSE: 2.2]
        Your body sleeps deeply... while a calm awareness rests inside the dream. [PAUSE: 2.4]
        Knowing softly... [PAUSE: 1.8] that you are dreaming. [PAUSE: 1.8]
    """,
    "lucid_seed_2": """
        Whenever you look out over this sea of clouds later tonight... [PAUSE: 2.2]
        You will know gently that you are inside a dream... [PAUSE: 2.0]
        Floating safely... and deeply asleep. [PAUSE: 1.8]
    """,
    "lucid_seed_3": """
        The sky outside has become your dream world. [PAUSE: 2.2]
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
    print(f"Rendering {len(SCRIPTS)} Cloud Airship clips...")
    for name, script in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {out}")
            continue
        print(f" -> {out}")
        render(script, out)
    print("Cloud Airship clips complete!")
