import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
OUTPUT_DIR = "audio/lighthouse_watch"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS = {
    "departure_1": """
        You climb the spiral stone stair into the lighthouse watch-room. [PAUSE: 2.3]
        And the heavy iron door seals shut against the coastal night. [PAUSE: 2.3]
        Thick granite walls insulate the circular chamber from the wind outside. [PAUSE: 2.2]
        You recline on a wide, wool-upholstered daybed built into the curved window alcove. [PAUSE: 2.4]
        Pulling a heavy woven blanket over your chest. [PAUSE: 2.2]
        High above the crashing surf... the great brass Fresnel lens rotates in absolute silence. [PAUSE: 2.4]
        Casting a slow, hypnotic beam of warm gold light out across the foggy sea, slowly, again and again. [PAUSE: 2.5]
        You are warm, dry, and high above the world... cradled in solid stone. [PAUSE: 1.8]
    """,
    "departure_2": """
        The watch-room is lit only by the amber glow of the copper control panel. [PAUSE: 2.3]
        You rest your head against the bolstered bolster... [PAUSE: 1.8]
        Watching the thick sea fog swirl softly against the curved windowpanes. [PAUSE: 2.3]
        Far below the granite cliff... ocean swells roll rhythmically against the rocks. [PAUSE: 2.4]
        Muffled by distance into a deep, comforting rumble. [PAUSE: 2.2]
        The oil lamps hum a quiet, steady note as the brass gear train turns overhead. [PAUSE: 2.4]
        Nothing can reach you up here... in the warm stone tower. [PAUSE: 1.6]
    """,
    "departure_3": """
        Inside the timber-paneled alcove... the air smells of old pine, paraffin, and salt air. [PAUSE: 2.3]
        You settle deep into the cushions of the guest daybed. [PAUSE: 2.0]
        Letting your hands rest flat against the quilt. [PAUSE: 2.2]
        Outside the thick glass... the night sea stretches away into absolute darkness. [PAUSE: 2.3]
        While inside... everything is snug, warm, and entirely unhurried. [PAUSE: 2.2]
        You close your eyes to the rhythmic sweep of the light... and let the ocean rock you. [PAUSE: 1.6]
    """,
    "drift_01": """
        High above the room, the great brass lens makes one slow rotation... [PAUSE: 2.2]
        Sweeping a warm golden arm of light across the sea fog. [PAUSE: 1.6]
    """,
    "drift_02": """
        Far down at the base of the granite cliff... a heavy ocean swell breaks against the shore. [PAUSE: 2.3]
        Rolling back with a long, soft hiss. [PAUSE: 1.5]
    """,
    "drift_03": """
        Against the thick curved windowpanes... tendrils of cool sea fog drift past. [PAUSE: 2.2]
        Soft and gray in the dark. [PAUSE: 1.5]
    """,
    "drift_04": """
        Inside the guest alcove, a small cast-iron radiator warms softly... [PAUSE: 2.3]
        And settles into a steady, dry heat. [PAUSE: 1.5]
    """,
    "drift_05": """
        The oiled gear teeth of the rotating lantern turn with a soft, oiled purr. [PAUSE: 2.3]
        Mechanical perfection in the dark. [PAUSE: 1.5]
    """,
    "drift_06": """
        Solid granite walls two feet thick hold back the coastal gale... [PAUSE: 2.2]
        Turning the storm outside into a low, distant sigh. [PAUSE: 1.5]
    """,
    "drift_07": """
        A faint amber reflection passes across the ceiling boards overhead... [PAUSE: 2.2]
        Completes its circle... and returns again. [PAUSE: 1.6]
    """,
    "drift_08": """
        Down on the dark water, distant soft surf rolls gently against the shore... [PAUSE: 2.2]
        So soft it is barely heard above the surf. [PAUSE: 1.5]
    """,
    "drift_09": """
        Your daybed absorbs the solid, motionless weight of the stone tower. [PAUSE: 2.3]
        Firm and unshakable. [PAUSE: 1.5]
    """,
    "drift_10": """
        A single droplet of condensation traces a vertical line down the window frame... [PAUSE: 2.3]
        Catching the amber light. [PAUSE: 1.5]
    """,
    "drift_11": """
        The rhythmic rise and fall of the ocean swells outside... [PAUSE: 2.0]
        Matches the slow, deep cadence of your breathing. [PAUSE: 1.6]
    """,
    "drift_12": """
        Along the curved stone sill, an old brass spyglass rests in its velvet cradle. [PAUSE: 2.3]
        Untouched and quiet. [PAUSE: 1.5]
    """,
    "drift_13": """
        The sea fog thickens outside the glass, blurring the horizon into a soft milk-white wall. [PAUSE: 2.4]
        Cozy and enclosed. [PAUSE: 1.5]
    """,
    "drift_14": """
        Warm air rises from the floor vent beside the cot... [PAUSE: 2.0]
        Holding the chill of the ocean at bay. [PAUSE: 1.6]
    """,
    "drift_15": """
        The great light completes another silent circle overhead... [PAUSE: 2.0]
        Illuminating the mist for a mile around the tower. [PAUSE: 1.6]
    """,
    "drift_16": """
        Your shoulders sink another inch into the bolstered pillow... [PAUSE: 2.0]
        Released from the day's fatigue. [PAUSE: 1.6]
    """,
    "drift_17": """
        Out on the black water, white foam crests vanish into the night foam... [PAUSE: 2.2]
        Unseen by anyone except the tower. [PAUSE: 1.5]
    """,
    "drift_18": """
        The heavy wool blanket keeps you dry and warm in the high stone room. [PAUSE: 2.3]
        Protected from the wind. [PAUSE: 1.5]
    """,
    "drift_19": """
        A slow, deep wave rolls into the coastal bay below... [PAUSE: 2.0]
        Rattling nothing, disturbing nothing. [PAUSE: 1.6]
    """,
    "drift_20": """
        The steady pulse of the rotating beacon keeps time with the quiet night. [PAUSE: 2.3]
        Predictable and calm. [PAUSE: 1.5]
    """,
    "drift_21": """
        Inside the watch-room, the smell of warm pine and salt air settles into stillness. [PAUSE: 2.3]
        Deeply grounding. [PAUSE: 1.5]
    """,
    "drift_22": """
        The distant surf beats a slow, heavy drum against the cliff foot... [PAUSE: 2.2]
        So rhythmic it feels like a heartbeat. [PAUSE: 1.5]
    """,
    "drift_23": """
        A stray gust of wind brushes the copper weather-vane on the copper roof peak... [PAUSE: 2.3]
        A brief, hollow murmur high above. [PAUSE: 1.5]
    """,
    "drift_24": """
        The amber reflection passes across the cedar wainscoting once more... [PAUSE: 2.2]
        Fading smoothly into shadow. [PAUSE: 1.5]
    """,
    "drift_25": """
        Your eyelids grow heavy as the tower holds you above the restless sea. [PAUSE: 2.3]
        Safe and warm. [PAUSE: 1.5]
    """,
    "drift_26": """
        The fog wraps tighter around the upper lantern room... [PAUSE: 2.0]
        Isolating your little alcove in a cocoon of light and stone. [PAUSE: 1.6]
    """,
    "drift_27": """
        Another wave spends its energy on the rocks below, sighing into the foam. [PAUSE: 2.3]
        Fading away to nothing. [PAUSE: 1.5]
    """,
    "drift_28": """
        The warmth of the blankets seals around you like an invisible shield. [PAUSE: 2.3]
        Nothing left to watch. [PAUSE: 1.5]
    """,
    "drift_29": """
        The copper gear train hums its low, mechanical lullaby in the dark. [PAUSE: 2.3]
        Carrying you closer to sleep. [PAUSE: 1.5]
    """,
    "drift_30": """
        The lighthouse watch-room stands firm against the coastal fog... [PAUSE: 2.0]
        Guarding your rest through the night. [PAUSE: 1.6]
    """,
    "lucid_seed_1": """
        As the golden light sweeps across the foggy sea... [PAUSE: 2.2]
        Your body sleeps deeply... while a calm awareness rests inside the dream. [PAUSE: 2.4]
        Knowing softly... [PAUSE: 1.8] that you are dreaming. [PAUSE: 1.8]
    """,
    "lucid_seed_2": """
        Whenever you notice the golden beam rotating later tonight... [PAUSE: 2.2]
        You will recognize gently that this lighthouse tower is a dream... [PAUSE: 2.0]
        Safe... warm... and deeply asleep. [PAUSE: 1.8]
    """,
    "lucid_seed_3": """
        The stone watch-room has folded quietly into your dream world. [PAUSE: 2.2]
        And you can rest above the quiet ocean... [PAUSE: 1.8] knowing it is all a dream. [PAUSE: 1.8]
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
    print(f"Rendering {len(SCRIPTS)} Lighthouse Watch clips...")
    for name, script in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {out}")
            continue
        print(f" -> {out}")
        render(script, out)
    print("Lighthouse Watch clips complete!")
