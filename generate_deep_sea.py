import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
OUTPUT_DIR = "audio/deep_sea"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS = {
    "departure_1": """
        You step into the circular lounge of the deep sea observatory. [PAUSE: 2.2]
        And the heavy pressure door seals with a soft, muffled thud. [PAUSE: 2.4]
        Around the room... a thick dome of curved acrylic opens onto the dark ocean floor. [PAUSE: 2.3]
        You stretch out on the wide felted daybed at the center of the dome. [PAUSE: 2.0]
        Pulling a heavy wool blanket over your shoulders. [PAUSE: 2.3]
        Hundreds of feet above the glass... the surface waves are completely forgotten. [PAUSE: 2.4]
        Down here... the water is calm... dark... and impossibly still. [PAUSE: 2.3]
        Only a low, comforting hum from the air scrubbers fills the warm room. [PAUSE: 1.6]
    """,
    "departure_2": """
        The interior lights of the dome are dimmed to a deep twilight blue. [PAUSE: 2.2]
        Blending seamlessly with the dark water beyond the thick viewing arch. [PAUSE: 2.3]
        You rest your head against the bolstered cushion... [PAUSE: 1.8]
        Feeling the solid stone sea-mount anchoring the chamber below. [PAUSE: 2.4]
        Outside the curved window... a slow deep-water current glides silently past. [PAUSE: 2.3]
        Carrying tiny specks of glowing marine snow through the dark. [PAUSE: 2.3]
        You are warm... dry... and completely sheltered at the bottom of the quiet sea. [PAUSE: 1.6]
    """,
    "departure_3": """
        Along the circular floor... a ring of muted amber floor lights marks the edge of the carpet. [PAUSE: 2.3]
        You sink into the deep curved sofa facing the main viewing window. [PAUSE: 2.0]
        Letting your hands rest relaxed in your lap. [PAUSE: 2.2]
        The thick acrylic arch holds back the entire weight of the ocean without a sound. [PAUSE: 2.4]
        Leaving the air inside still... warm... and unhurried. [PAUSE: 2.2]
        Outside... the blue-black water moves in slow, weightless currents. [PAUSE: 2.3]
        With nothing to disturb the deep night. [PAUSE: 1.6]
    """,
    "drift_01": """
        Outside the curved dome... a translucent jellyfish drifts upward in the slow current. [PAUSE: 2.3]
        Pulsing with a faint, sleepy blue glow. [PAUSE: 1.5]
    """,
    "drift_02": """
        Fine specks of marine snow... float lazily past the thick window pane. [PAUSE: 2.2]
        Like dust motes in a dim room. [PAUSE: 1.5]
    """,
    "drift_03": """
        The deep ocean current presses smoothly against the outer arch... [PAUSE: 2.0]
        With a low, unchanging hush. [PAUSE: 1.8]
    """,
    "drift_04": """
        A ribbon of green bioluminescence... trails slowly through the dark water outside. [PAUSE: 2.3]
        Fading softly as it drifts away. [PAUSE: 1.5]
    """,
    "drift_05": """
        Inside the lounge... the air ventilation system breathes a steady, warm whisper. [PAUSE: 2.3]
        Constant and reassuring. [PAUSE: 1.5]
    """,
    "drift_06": """
        Across the sandy sea floor outside... a soft blue spotlight fades into the dark distance. [PAUSE: 2.4]
        Revealing smooth ripples in the silt. [PAUSE: 1.5]
    """,
    "drift_07": """
        Tall fronds of deep-water kelp... sway from side to side in the dark tide. [PAUSE: 2.3]
        Bending and returning... in one unhurried sweep. [PAUSE: 1.5]
    """,
    "drift_08": """
        The curved ceiling of the dome... reflects the faint turquoise shimmer of the water. [PAUSE: 2.3]
        Moving like slow silk overhead. [PAUSE: 1.5]
    """,
    "drift_09": """
        Hundreds of feet above... all the noise of the surface world is completely erased. [PAUSE: 2.3]
        Replaced by deep, heavy stillness. [PAUSE: 1.5]
    """,
    "drift_10": """
        A tiny comb jelly glides past the glass... [PAUSE: 1.8]
        Rippling with a soft rainbow of muted light. [PAUSE: 2.0]
    """,
    "drift_11": """
        Beneath the plush carpet... the heavy steel foundation rests solid on the ocean bedrock. [PAUSE: 2.3]
        Unmoving and secure. [PAUSE: 1.5]
    """,
    "drift_12": """
        Your breathing settles into the same slow pace... as the drifting sea plants outside. [PAUSE: 2.3]
        Unhurried... and weightless. [PAUSE: 1.5]
    """,
    "drift_13": """
        Out in the blue-black water... a school of tiny silver fish turns in a single, silent arc. [PAUSE: 2.4]
        Catching the dim glow from the dome. [PAUSE: 1.5]
    """,
    "drift_14": """
        The felted cushions around you... hold a gentle, dry warmth. [PAUSE: 2.2]
        While the deep sea outside stays cool and dark. [PAUSE: 1.5]
    """,
    "drift_15": """
        Along the base of the window... smooth basalt rocks rest untouched in the quiet silt. [PAUSE: 2.3]
        Still and unchanging... in the deep dark. [PAUSE: 1.5]
    """,
    "drift_16": """
        A cloud of tiny glowing plankton... swirls gently against the outer curve of the dome. [PAUSE: 2.3]
        Drifting upward into the dark. [PAUSE: 1.5]
    """,
    "drift_17": """
        On the wall console... a single depth gauge glows in a muted amber font. [PAUSE: 2.2]
        Steady and silent. [PAUSE: 1.5]
    """,
    "drift_18": """
        The water outside is so dark and clear... it feels like floating in deep night sky. [PAUSE: 2.3]
        Surrounded by slow underwater stars. [PAUSE: 1.5]
    """,
    "drift_19": """
        A gentle warmth radiates from the curved baseboard along the viewing wall. [PAUSE: 2.2]
        Keeping the lounge cozy and still. [PAUSE: 1.5]
    """,
    "drift_20": """
        Two pale moon jellies drift past one another... [PAUSE: 1.8]
        Moving effortlessly with the deep tide. [PAUSE: 2.0]
    """,
    "drift_21": """
        Every muscle in your neck and shoulders... softens into the deep cushion beneath you. [PAUSE: 2.3]
        Held by the quiet pressure of the deep. [PAUSE: 1.5]
    """,
    "drift_22": """
        Far out beyond the floodlight... a faint spark of blue light blooms once in the dark... [PAUSE: 2.3]
        And melts back into the sea. [PAUSE: 1.5]
    """,
    "drift_23": """
        The thick acrylic pane feels cool and solid... inches from your shoulder. [PAUSE: 2.2]
        Keeping the world outside at peace. [PAUSE: 1.5]
    """,
    "drift_24": """
        Fine sand grains slide half an inch down a small dune on the ocean floor. [PAUSE: 2.3]
        And come to rest again. [PAUSE: 1.5]
    """,
    "drift_25": """
        The low hum of the observatory... blends with the deep water hush outside. [PAUSE: 2.3]
        Forming a single, soothing bed of sound. [PAUSE: 1.5]
    """,
    "drift_26": """
        Shades of indigo and deep navy... fold slowly into one another beyond the arch. [PAUSE: 2.3]
        With no sharp edges anywhere. [PAUSE: 1.5]
    """,
    "drift_27": """
        The heavy wool blanket rests warmly across your chest... [PAUSE: 1.8]
        Rising and falling in the dim blue light. [PAUSE: 2.0]
    """,
    "drift_28": """
        A slow underwater eddy... carries a trail of silver specks across the top of the dome. [PAUSE: 2.3]
        Drifting out of sight. [PAUSE: 1.5]
    """,
    "drift_29": """
        Everything down here moves with the deep ocean tide... along the sandy floor. [PAUSE: 2.3]
        Nowhere to go... and nothing to do. [PAUSE: 1.5]
    """,
    "drift_30": """
        The blue glow outside dims a shade deeper... [PAUSE: 1.8]
        Cradling the silent dome in the dark water. [PAUSE: 2.0]
    """,
    "lucid_seed_1": """
        As the glowing currents drift past the dome... [PAUSE: 2.0]
        Your body sleeps deeply... while a calm awareness floats inside the dream. [PAUSE: 2.4]
        Knowing softly... [PAUSE: 1.8] that this deep ocean is now a dream. [PAUSE: 1.8]
    """,
    "lucid_seed_2": """
        Whenever you notice these slow blue lights later tonight... [PAUSE: 2.2]
        You will recognize gently that you are dreaming... [PAUSE: 2.0]
        Safe... weightless... and deeply asleep. [PAUSE: 1.8]
    """,
    "lucid_seed_3": """
        The deep sea around the dome has melted into your dream. [PAUSE: 2.2]
        And you can rest inside the quiet water... [PAUSE: 1.8] knowing it is all a dream. [PAUSE: 1.8]
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
    print(f"Rendering {len(SCRIPTS)} Deep Sea clips...")
    for name, script in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {out}")
            continue
        print(f" -> {out}")
        render(script, out)
    print("Deep Sea clips complete!")
