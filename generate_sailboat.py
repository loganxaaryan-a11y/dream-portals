import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
OUTPUT_DIR = "audio/sailboat"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS = {
    "departure_1": """
        You step down the companionway stairs... into the warm teak cabin of the sailboat. [PAUSE: 2.2]
        And slide the wooden hatch closed above your head. [PAUSE: 2.4]
        The night breeze stays outside... leaving the cabin air still and cozy. [PAUSE: 2.2]
        You stretch out on the wide cushioned berth along the hull. [PAUSE: 1.8]
        Pulling a heavy cotton blanket up to your shoulders. [PAUSE: 2.4]
        Just inches from your pillow... calm bay water laps softly against the thick cedar planks. [PAUSE: 2.5]
        A slow, gentle cradle... [PAUSE: 1.8] rocking a few inches to the left... [PAUSE: 1.8] and a few inches to the right. [PAUSE: 2.4]
        The boat is safely on its night mooring... with nowhere left to steer. [PAUSE: 1.6]
    """,
    "departure_2": """
        Inside the low wooden cabin... a single brass oil lamp glows at its lowest wick. [PAUSE: 2.3]
        Casting a warm honey light across the curved ribs of the hull. [PAUSE: 2.2]
        You rest your head on the firm canvas pillow... [PAUSE: 1.8]
        Looking out through the round brass porthole beside the berth. [PAUSE: 2.4]
        Outside the thick glass... the dark water of the sheltered cove is almost flat. [PAUSE: 2.2]
        Every slow swell lifts the hull... [PAUSE: 1.8] and sets it back down with a muffled hush. [PAUSE: 2.5]
        You are dry... sheltered below deck... [PAUSE: 1.8] floating on deep, quiet water. [PAUSE: 1.6]
    """,
    "departure_3": """
        The sails are furled and tied... resting quietly under their heavy canvas covers above. [PAUSE: 2.3]
        Down here in the cabin... the world is small... warm... and enclosed. [PAUSE: 2.2]
        You sink into the corner of the cushioned settee. [PAUSE: 1.8]
        Feeling the slow, buoyant lift of the tide beneath the keel. [PAUSE: 2.4]
        Small ripples tap a gentle, irregular rhythm against the outer planking. [PAUSE: 2.3]
        Never hurried... and never loud. [PAUSE: 2.0]
        All the weight of the day stays back on the distant shore. [PAUSE: 1.6]
    """,
    "drift_01": """
        Through the round brass porthole... pale starlight shimmers on the dark surface of the bay. [PAUSE: 2.3]
        Breaking into slow silver ribbons. [PAUSE: 1.5]
    """,
    "drift_02": """
        Beneath your berth... cool bay water glides past the thick cedar hull. [PAUSE: 2.2]
        With a muffled, liquid whisper. [PAUSE: 1.5]
    """,
    "drift_03": """
        The wooden cabin tilts a fraction of an inch... [PAUSE: 1.8] and slowly settles back to level. [PAUSE: 2.2]
        Like a slow, deep breath. [PAUSE: 1.5]
    """,
    "drift_04": """
        Faint blue bioluminescence... drifts past the glass porthole in the dark tide. [PAUSE: 2.3]
        Glowing softly... and fading into the deep water. [PAUSE: 1.5]
    """,
    "drift_05": """
        Across the narrow table... the gimballing lamp sways smoothly in its brass ring. [PAUSE: 2.3]
        Keeping its warm light completely level. [PAUSE: 1.5]
    """,
    "drift_06": """
        A tiny wave slips under the bow... [PAUSE: 1.8] sending a soft hush all the way down the hull. [PAUSE: 2.0]
    """,
    "drift_07": """
        The scent of old cedar wood... and clean salt air... hangs still inside the cabin. [PAUSE: 2.3]
        Calm and familiar. [PAUSE: 1.5]
    """,
    "drift_08": """
        Far across the sheltered cove... a single harbor lantern glows amber on the dark point. [PAUSE: 2.4]
        Steady across a mile of flat water. [PAUSE: 1.5]
    """,
    "drift_09": """
        The heavy hemp mooring line... gives a deep, muffled stretch in the slow current. [PAUSE: 2.3]
        Holding the boat securely in place. [PAUSE: 1.5]
    """,
    "drift_10": """
        Moonlight enters the high skylight hatch... [PAUSE: 1.8] painting a pale square on the teak floorboards. [PAUSE: 2.0]
    """,
    "drift_11": """
        As the hull rocks... that square of moonlight slides two inches across the floor... [PAUSE: 2.2]
        And drifts back again. [PAUSE: 1.5]
    """,
    "drift_12": """
        Coiled rope rests neatly on the wooden bench... [PAUSE: 1.8] untouched in the dim amber glow. [PAUSE: 2.0]
    """,
    "drift_13": """
        Outside the porthole... dark eelgrass sways lazily beneath the clear night water. [PAUSE: 2.3]
        Moving with the slow incoming tide. [PAUSE: 1.5]
    """,
    "drift_14": """
        The thick wooden ribs of the boat... give a tiny, warm settle around you. [PAUSE: 2.2]
        Built to hold back the sea. [PAUSE: 1.5]
    """,
    "drift_15": """
        Ripples of reflected moonlight... dance slowly across the white painted ceiling above your berth. [PAUSE: 2.4]
        Silent... and weightless. [PAUSE: 1.5]
    """,
    "drift_16": """
        A light night mist drifts across the surface of the bay... [PAUSE: 2.0]
        Softening the distant tree line on the shore. [PAUSE: 1.8]
    """,
    "drift_17": """
        The heavy lead keel deep beneath the cabin... keeps every motion slow and grounded. [PAUSE: 2.3]
        Never tipping too far. [PAUSE: 1.5]
    """,
    "drift_18": """
        Water trickles softly along the outer waterline... [PAUSE: 1.8] just beside your ear. [PAUSE: 2.0]
    """,
    "drift_19": """
        On the wooden bulkhead... the brass barometer needle rests completely still. [PAUSE: 2.2]
        Pointing to calm, settled weather. [PAUSE: 1.5]
    """,
    "drift_20": """
        Your weight sinks deeper into the mattress... each time the boat settles into a trough. [PAUSE: 2.4]
        Carried by the dark water. [PAUSE: 1.5]
    """,
    "drift_21": """
        In the galley corner... every cup and plate rests tucked inside its wooden rack. [PAUSE: 2.2]
        Quiet for the night. [PAUSE: 1.5]
    """,
    "drift_22": """
        A cluster of green glowing plankton... swirls past the round glass pane. [PAUSE: 2.3]
        Like slow underwater stars. [PAUSE: 1.5]
    """,
    "drift_23": """
        The heavy cotton blanket holds your body warmth... [PAUSE: 1.8] while the cabin air stays cool on your cheek. [PAUSE: 2.0]
    """,
    "drift_24": """
        Out on the dark water... circular ripples spread from a single drop of dew. [PAUSE: 2.3]
        Widening until they vanish. [PAUSE: 1.5]
    """,
    "drift_25": """
        The wooden rudder beneath the stern... rests still in the slack tide. [PAUSE: 2.2]
        With nothing to guide. [PAUSE: 1.5]
    """,
    "drift_26": """
        Low hills around the bay... stand like dark, protective shoulders against the night sky. [PAUSE: 2.3]
        Keeping the wind far overhead. [PAUSE: 1.5]
    """,
    "drift_27": """
        Each gentle rock of the cabin... loosens a little more tension from your shoulders. [PAUSE: 2.3]
        Over... and over. [PAUSE: 1.5]
    """,
    "drift_28": """
        The brass porthole ring... gleams dimly with a single point of amber lamplight. [PAUSE: 2.2]
        Steady in the dark. [PAUSE: 1.5]
    """,
    "drift_29": """
        Deep water below the keel... stretches down into cool, silent darkness. [PAUSE: 2.3]
        Holding the boat effortlessly afloat. [PAUSE: 1.5]
    """,
    "drift_30": """
        The tide reaches its quiet turn... [PAUSE: 1.8] and the bay becomes smooth as dark mirror glass. [PAUSE: 2.0]
    """,
    "lucid_seed_1": """
        As the cabin rocks on the dark tide... [PAUSE: 2.0]
        Your body drifts into deep sleep... while a quiet part of your mind stays gently aware. [PAUSE: 2.4]
        Knowing that this calm water... [PAUSE: 1.8] is now a dream. [PAUSE: 1.8]
    """,
    "lucid_seed_2": """
        Whenever you feel this slow, gentle rocking later tonight... [PAUSE: 2.2]
        You will recognize softly that you are dreaming... [PAUSE: 2.0]
        Free to float... and deeply asleep. [PAUSE: 1.8]
    """,
    "lucid_seed_3": """
        The bay outside has melted into the dream world. [PAUSE: 2.2]
        You can rest inside it peacefully... [PAUSE: 1.8] aware that you are dreaming. [PAUSE: 1.8]
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
    print(f"Rendering {len(SCRIPTS)} Sailboat clips...")
    for name, script in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {out}")
            continue
        print(f" -> {out}")
        render(script, out)
    print("Sailboat clips complete!")
