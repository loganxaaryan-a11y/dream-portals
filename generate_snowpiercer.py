import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
OUTPUT_DIR = "audio/snowpiercer"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS = {
    # --- 3 ROTATING DEPARTURES ---
    "departure_1": """
        You step into the warm wooden observatory car... at the quiet tail of the night train. [PAUSE: 2.3]
        And pull the heavy mahogany door shut behind you. [PAUSE: 2.4]
        Along the curved walls... brass steam radiators purr with a steady, comforting warmth. [PAUSE: 2.4]
        You climb onto the wide corner daybed... and pull the thick down duvet up to your chin. [PAUSE: 2.3]
        Just inches away... behind double-paned glass... a white mountain blizzard swirls through the dark. [PAUSE: 2.5]
        Beneath the heavy floorboards... the wide wheels roll smoothly over the snow-packed rails. [PAUSE: 2.4]
        Thump-thump... [PAUSE: 1.3] thump-thump. [PAUSE: 2.5]
        Inside this glass-domed sanctuary... the air is still... toasted... and completely safe from the storm. [PAUSE: 1.8]
    """,
    "departure_2": """
        The brass wall sconces are turned down to a dim, honeyed glow. [PAUSE: 2.2]
        Warming the dark mahogany ribs of the observation dome. [PAUSE: 2.2]
        You sink back against a stack of firm wool pillows... [PAUSE: 1.8]
        Watching the snow sweep past the curved glass roof overhead. [PAUSE: 2.4]
        Outside... the high mountain pass is buried in deep winter white. [PAUSE: 2.2]
        Inside... the radiator beside your bed breathes a soft, continuous ribbon of heat. [PAUSE: 2.4]
        The heavy carriage sways gently on its winter springs... carrying you effortlessly through the frozen night. [PAUSE: 1.8]
    """,
    "departure_3": """
        Frost patterns edge the outer corners of the thick observation windows... [PAUSE: 2.2]
        While the inner pane feels warm to the touch. [PAUSE: 2.0]
        You wrap yourself in the heavy tartan blanket on the lounge sofa. [PAUSE: 2.2]
        Listening to the muffled rush of the snowstorm outside... and the deep, steady cadence of the tracks below. [PAUSE: 2.5]
        Every draft is sealed out by the heavy rubber gaskets of the dome. [PAUSE: 2.3]
        Leaving you tucked inside a warm pocket of amber light... gliding through the white mountains. [PAUSE: 1.8]
    """,

    # --- 30 STANDALONE MICRO-DRIFTS ---
    "drift_01": """
        Outside the double-paned glass... thick clouds of powder snow swirl in the amber light from your window. [PAUSE: 2.4]
        Vanishing into the dark mountain pass behind the train. [PAUSE: 1.5]
    """,
    "drift_02": """
        Beside the daybed... the brass steam radiator gives a soft, steady hiss of warmth. [PAUSE: 2.3]
        Keeping the cabin air cozy and dry. [PAUSE: 1.5]
    """,
    "drift_03": """
        Deep snow along the track bed... muffles the rhythm of the heavy steel wheels below. [PAUSE: 2.3]
        Turning every rail joint into a soft, low thud. [PAUSE: 1.5]
    """,
    "drift_04": """
        Towering granite peaks... stand like pale grey ghosts against the snowy night sky. [PAUSE: 2.3]
        Sliding slowly past the upper dome. [PAUSE: 1.5]
    """,
    "drift_05": """
        Delicate ice ferns... trace silver patterns along the very bottom edge of the outer glass. [PAUSE: 2.3]
        Glowing faintly in the sconce light. [PAUSE: 1.5]
    """,
    "drift_06": """
        The heavy carriage leans gently into a wide mountain curve... [PAUSE: 2.2]
        Cradling your weight deeper into the mattress. [PAUSE: 1.5]
    """,
    "drift_07": """
        Wind sweeps a veil of fine snow across the curved roof overhead... [PAUSE: 2.2]
        With a muffled, papery brush. [PAUSE: 1.5]
    """,
    "drift_08": """
        Inside the mahogany walls... the timber frame gives a warm, quiet settle. [PAUSE: 2.2]
        Built heavy and strong against the winter cold. [PAUSE: 1.5]
    """,
    "drift_09": """
        Through the swirling flakes outside... dark evergreen trees stand bowed under thick white coats. [PAUSE: 2.4]
        Drifting silently to the rear. [PAUSE: 1.5]
    """,
    "drift_10": """
        The thick down duvet traps a pocket of gentle heat around your shoulders. [PAUSE: 2.2]
        Soft... weightless... and still. [PAUSE: 1.5]
    """,
    "drift_11": """
        The train enters a long stone snow-shed on the mountainside... [PAUSE: 2.2]
        Hushing the wind outside for a few deep, quiet breaths. [PAUSE: 1.8]
    """,
    "drift_12": """
        Heavy velvet drapes hang tied back at the corners of the viewing arch... [PAUSE: 2.2]
        Swaying a fraction of an inch with the motion of the car. [PAUSE: 1.5]
    """,
    "drift_13": """
        Out behind the rear observation rail... the twin red tail lamps glow softly in the blowing snow. [PAUSE: 2.4]
        Marking the peaceful wake of the train. [PAUSE: 1.5]
    """,
    "drift_14": """
        Warm air rising from the floor vents... meets the cool glass in a gentle current. [PAUSE: 2.3]
        Keeping the inner pane crystal clear. [PAUSE: 1.5]
    """,
    "drift_15": """
        Far below in the valley... a frozen river winds like a wide ribbon of smooth white slate. [PAUSE: 2.3]
        Untouched and silent. [PAUSE: 1.5]
    """,
    "drift_16": """
        The brass reading lamp beside your pillow... casts a tiny circle of amber light on the wood grain. [PAUSE: 2.3]
        Steady and unblinking. [PAUSE: 1.5]
    """,
    "drift_17": """
        A gust of mountain wind presses softly against the outer dome... [PAUSE: 2.0]
        While the air inside does not stir at all. [PAUSE: 1.6]
    """,
    "drift_18": """
        Snowdrifts banked high along the rails... glide past like smooth white waves. [PAUSE: 2.3]
        Softening the whole landscape. [PAUSE: 1.5]
    """,
    "drift_19": """
        Beneath the thick wool carpet... the heated floorboards warm the cabin from wall to wall. [PAUSE: 2.3]
        Constant and reassuring. [PAUSE: 1.5]
    """,
    "drift_20": """
        The train glides across a high alpine trestle... [PAUSE: 2.0]
        Floating through the snowy dark above a deep ravine. [PAUSE: 1.8]
    """,
    "drift_21": """
        Flakes of snow catch the warm window light... [PAUSE: 1.8]
        Looking like slow golden moths drifting past in the dark. [PAUSE: 1.8]
    """,
    "drift_22": """
        The rhythm of the wheels... and the soft hiss of the radiator... weave into a single lullaby. [PAUSE: 2.4]
        Steady through the long winter night. [PAUSE: 1.5]
    """,
    "drift_23": """
        Every window seal holds tight and quiet... [PAUSE: 1.8]
        Turning the storm outside into a gentle picture behind glass. [PAUSE: 1.8]
    """,
    "drift_24": """
        High on the mountain ridge... the clouds part briefly to show a pale wash of moonlight on the snow. [PAUSE: 2.4]
        Before the soft white mist closes in again. [PAUSE: 1.5]
    """,
    "drift_25": """
        Your breathing slows to match the gentle rock of the heavy sleeper car. [PAUSE: 2.3]
        Deep... warm... and unhurried. [PAUSE: 1.5]
    """,
    "drift_26": """
        A small brass pressure gauge on the radiator pipe... rests steady in the dim glow. [PAUSE: 2.2]
        Everything working quietly on its own. [PAUSE: 1.5]
    """,
    "drift_27": """
        Fresh powder piles half an inch on the outer window ledge... [PAUSE: 2.0]
        And slides smoothly away in the slipstream. [PAUSE: 1.6]
    """,
    "drift_28": """
        The long train curves gently through a sheltered pine valley... [PAUSE: 2.2]
        Where the snow falls straight down in large, lazy flakes. [PAUSE: 1.6]
    """,
    "drift_29": """
        All the cold of the winter world stays locked outside the thick glass... [PAUSE: 2.3]
        Making your warm bed feel twice as deep. [PAUSE: 1.5]
    """,
    "drift_30": """
        The heavy wheels roll on through the white quiet... [PAUSE: 2.0]
        Carrying your warm room deeper into the night. [PAUSE: 1.6]
    """,

    # --- 3 ROTATING LUCID SEEDS ---
    "lucid_seed_1": """
        As the warm train glides through the snowy mountains... [PAUSE: 2.2]
        Your body sleeps deeply... while a quiet awareness rests inside the dream. [PAUSE: 2.4]
        Knowing softly... [PAUSE: 1.8] that you are dreaming. [PAUSE: 1.8]
    """,
    "lucid_seed_2": """
        Whenever you notice the snow swirling past the glass later tonight... [PAUSE: 2.2]
        You will recognize gently that this warm car is a dream... [PAUSE: 2.0]
        Safe... cozy... and deeply asleep. [PAUSE: 1.8]
    """,
    "lucid_seed_3": """
        The winter night outside has melted into your dream world. [PAUSE: 2.2]
        And you can rest inside the warmth... [PAUSE: 1.8] knowing it is all a dream. [PAUSE: 1.8]
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
    print(f"Rendering {len(SCRIPTS)} Snowpiercer clips...")
    for name, script in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {out}")
            continue
        print(f" -> {out}")
        render(script, out)
    print("Snowpiercer clips complete!")
