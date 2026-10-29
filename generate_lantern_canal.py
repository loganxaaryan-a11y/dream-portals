import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
OUTPUT_DIR = "audio/lantern_canal"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS = {
    # --- 3 ROTATING DEPARTURES ---
    "departure_1": """
        You step down onto the flat cypress deck... of the covered canal barge. [PAUSE: 2.2]
        And duck beneath the arched roof of woven bamboo. [PAUSE: 2.3]
        Inside the low cabin... a thick cotton mattress is spread with dry linen sheets and plump pillows. [PAUSE: 2.4]
        You lie back under the canopy... looking out through the open wooden eaves at the water level. [PAUSE: 2.4]
        At the bow... a single paper lantern hangs from a curved wood hook... casting a warm amber reflection on the canal. [PAUSE: 2.5]
        With a soft, liquid dip of the rear sculling oar... the boat pushes smoothly away from the mossy stone steps. [PAUSE: 2.5]
        Gliding down the quiet water lane... between warm stone walls and sleeping gardens. [PAUSE: 1.8]
    """,
    "departure_2": """
        The summer night air under the bamboo roof... is warm, still, and fragrant with water lilies. [PAUSE: 2.4]
        You rest your head on the low bolster pillow... [PAUSE: 1.8]
        Pulling a light cotton quilt across your waist. [PAUSE: 2.2]
        Just inches below the cypress gunwale... the dark canal water laps with a gentle, rhythmic hush. [PAUSE: 2.4]
        Every few seconds... the wooden oar at the stern dips... [PAUSE: 1.8] and sends the barge gliding effortlessly forward. [PAUSE: 2.4]
        Along both banks... warm paper lanterns glow under the eaves of old timber houses... [PAUSE: 2.3]
        Drifting slowly past as you float down the quiet waterway. [PAUSE: 1.6]
    """,
    "departure_3": """
        Inside the wooden canopy of the barge... you are completely shaded and hidden from the night sky. [PAUSE: 2.3]
        You stretch out on the soft floor cushions... listening to the crickets singing in the mossy canal walls. [PAUSE: 2.4]
        The flat bottom of the boat slides over the calm water without a ripple or a jar. [PAUSE: 2.3]
        Outside the side window frame... reflections of amber lanterns stretch across the dark surface like ribbons of honey. [PAUSE: 2.5]
        There are no locks to wait for... and no turns to steer. [PAUSE: 2.0]
        Only the slow, endless current carrying the boat through the quiet night. [PAUSE: 1.6]
    """,

    # --- 30 STANDALONE MICRO-DRIFTS ---
    "drift_01": """
        Long, trailing fronds of a weeping willow... brush softly across the woven bamboo roof above you. [PAUSE: 2.4]
        And trail their tips through the dark water behind. [PAUSE: 1.5]
    """,
    "drift_02": """
        The barge glides beneath a low, arched bridge of ancient grey stone... [PAUSE: 2.3]
        Turning the lap of the water into a soft, hollow echo for a few seconds. [PAUSE: 1.8]
    """,
    "drift_03": """
        At the stern... the wooden oar dips smoothly into the canal... [PAUSE: 2.0]
        And lifts with a quiet trickle of water drops. [PAUSE: 1.6]
    """,
    "drift_04": """
        Warm red and amber paper lanterns... hang along the stone quay outside. [PAUSE: 2.2]
        Their reflections wavering gently in the wake of the boat. [PAUSE: 1.5]
    """,
    "drift_05": """
        In the damp moss between the canal stones... night crickets trill a steady, drowsy chorus. [PAUSE: 2.3]
        Drifting softly across the water. [PAUSE: 1.5]
    """,
    "drift_06": """
        Round green lotus leaves... float near the bank... [PAUSE: 1.8]
        Rocking gently as the bow wave slips past them. [PAUSE: 1.8]
    """,
    "drift_07": """
        The scent of warm cypress wood... damp stone... and night-blooming jasmine fills the cabin. [PAUSE: 2.4]
        Calm and unhurried. [PAUSE: 1.5]
    """,
    "drift_08": """
        Through the wooden window frame... old whitewashed garden walls glide slowly to the rear. [PAUSE: 2.3]
        Topped with dark clay roof tiles. [PAUSE: 1.5]
    """,
    "drift_09": """
        The paper lantern on the bow... swings half an inch with the glide of the hull. [PAUSE: 2.2]
        Painting warm gold circles on the dark water ahead. [PAUSE: 1.5]
    """,
    "drift_10": """
        A tiny green frog on the mossy bank... gives a single, low croak in the dark. [PAUSE: 2.3]
        And settles back into the reeds. [PAUSE: 1.5]
    """,
    "drift_11": """
        Beneath your cotton mattress... the flat cypress planks transmit the cool, liquid glide of the canal. [PAUSE: 2.4]
        Smooth as silk. [PAUSE: 1.5]
    """,
    "drift_12": """
        Stone steps lead down into the dark water along the bank... [PAUSE: 2.0]
        Empty and glistening in the lantern glow. [PAUSE: 1.6]
    """,
    "drift_13": """
        Pale pink cherry petals... rest scattered on the surface of the slow current. [PAUSE: 2.3]
        Floating alongside the boat like tiny boats of their own. [PAUSE: 1.5]
    """,
    "drift_14": """
        The barge emerges from beneath a wide wooden footbridge... [PAUSE: 2.0]
        Back into the open, starlit stretch of the canal. [PAUSE: 1.8]
    """,
    "drift_15": """
        Wooden shutters on the passing canal houses... are closed and latched for the night. [PAUSE: 2.3]
        Only a faint line of amber light showing through the slats. [PAUSE: 1.5]
    """,
    "drift_16": """
        A warm night breeze moves down the waterway... [PAUSE: 2.0]
        Stirring the silk tassel beneath the bow lantern. [PAUSE: 1.6]
    """,
    "drift_17": """
        Ripples from the bow... tap a soft, hollow rhythm against the stone embankment. [PAUSE: 2.3]
        Fading behind the stern. [PAUSE: 1.5]
    """,
    "drift_18": """
        Under the arched bamboo roof... the shadows are deep, warm, and restful. [PAUSE: 2.2]
        Sheltering your eyes from the sky. [PAUSE: 1.5]
    """,
    "drift_19": """
        Where a narrow side canal branches off into the dark... [PAUSE: 2.0]
        A row of floating candle lanterns drifts still on the water. [PAUSE: 1.8]
    """,
    "drift_20": """
        The wooden oar pivot gives a soft, oiled creak... [PAUSE: 1.8]
        Followed by the gentle push of the current. [PAUSE: 1.8]
    """,
    "drift_21": """
        Bamboo stalks in a courtyard garden... lean out over the stone wall. [PAUSE: 2.2]
        Rustling softly as the barge slips underneath. [PAUSE: 1.5]
    """,
    "drift_22": """
        In the dark water beside the hull... the reflection of the full moon slides smoothly along with you. [PAUSE: 2.4]
        Unbroken and calm. [PAUSE: 1.5]
    """,
    "drift_23": """
        Your breathing falls into the same unhurried pace... as the dip and glide of the oar. [PAUSE: 2.3]
        Push... and drift. [PAUSE: 1.5]
    """,
    "drift_24": """
        Old wooden mooring posts rise from the water near the bank... [PAUSE: 2.0]
        Wrapped in soft green river moss. [PAUSE: 1.6]
    """,
    "drift_25": """
        A thin ribbon of warm mist... floats just inches above the surface of the canal. [PAUSE: 2.3]
        Glowing amber where it touches the lantern light. [PAUSE: 1.5]
    """,
    "drift_26": """
        The cotton quilt feels light and dry against your shoulders... [PAUSE: 2.0]
        Holding the gentle warmth of the summer night. [PAUSE: 1.6]
    """,
    "drift_27": """
        Another low stone arch passes overhead... [PAUSE: 1.8]
        Wrapping the boat in a cool, quiet shadow before opening out again. [PAUSE: 2.0]
    """,
    "drift_28": """
        The canal widens into a calm, mirror-still basin bordered by dark pines. [PAUSE: 2.3]
        Where the water barely whispers against the wood. [PAUSE: 1.5]
    """,
    "drift_29": """
        Every lantern reflection on the water... blurs into a soft golden path. [PAUSE: 2.2]
        Leading effortlessly through the dark. [PAUSE: 1.5]
    """,
    "drift_30": """
        The wooden barge glides on down the quiet canal... [PAUSE: 2.0]
        Rocking you gently into deep, peaceful sleep. [PAUSE: 1.6]
    """,

    # --- 3 ROTATING LUCID SEEDS ---
    "lucid_seed_1": """
        As the wooden barge glides between the warm lanterns... [PAUSE: 2.2]
        Your body sleeps deeply... while a calm awareness floats inside the dream. [PAUSE: 2.4]
        Knowing softly... [PAUSE: 1.8] that this quiet canal is now a dream. [PAUSE: 1.8]
    """,
    "lucid_seed_2": """
        Whenever you see the amber lantern reflections on the water later tonight... [PAUSE: 2.2]
        You will recognize gently that you are dreaming... [PAUSE: 2.0]
        Floating safely... and deeply asleep. [PAUSE: 1.8]
    """,
    "lucid_seed_3": """
        The canal outside has melted into your dream world. [PAUSE: 2.2]
        And you can drift along it peacefully... [PAUSE: 1.8] knowing it is all a dream. [PAUSE: 1.8]
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
    print(f"Rendering {len(SCRIPTS)} Lantern Canal clips...")
    for name, script in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {out}")
            continue
        print(f" -> {out}")
        render(script, out)
    print("Lantern Canal clips complete!")
