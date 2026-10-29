import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
OUTPUT_DIR = "audio/library_elevator"
os.makedirs(OUTPUT_DIR, exist_ok=True)

SCRIPTS = {
    # --- 3 ROTATING DEPARTURES ---
    "departure_1": """
        You step onto the thick wool rug... inside the spacious glass library elevator. [PAUSE: 2.3]
        And the paned walnut doors slide shut with a muffled brush of felt. [PAUSE: 2.4]
        This car is built like a small, private reading room... [PAUSE: 1.8]
        With a deep leather armchair... and a tiny brick hearth glowing in the corner wall. [PAUSE: 2.4]
        You sink into the chair... and pull a knitted wool throw across your lap. [PAUSE: 2.2]
        With a smooth, weightless lift... the brass cables begin raising the car at a slow walking pace. [PAUSE: 2.5]
        On three sides... endless tiers of dim, book-lined balconies glide slowly downward. [PAUSE: 2.3]
        While on the fourth side... night rain taps softly against the tall outer glass of the shaft. [PAUSE: 2.4]
        There is no floor button pressed... [PAUSE: 1.8] just a slow, endless rise through the quiet building. [PAUSE: 1.6]
    """,
    "departure_2": """
        Inside the wooden elevator car... the small hearth fire radiates a dry, gentle warmth. [PAUSE: 2.4]
        Casting soft amber light across the tufted leather bench and the walnut shelves. [PAUSE: 2.3]
        You stretch out on the bench... resting your head on a firm linen cushion. [PAUSE: 2.2]
        Beneath the floor... the counterweight machinery hums a low, soothing note. [PAUSE: 2.3]
        Outside the tall glass pane... rain streaks down against the dark city sky. [PAUSE: 2.2]
        And through the interior windows... level after level of quiet bookshelves drift smoothly past. [PAUSE: 2.4]
        You are enclosed in your own moving study... rising effortlessly through the night. [PAUSE: 1.6]
    """,
    "departure_3": """
        The brass floor dial above the door is unlit... and resting still. [PAUSE: 2.2]
        You settle into the deep wingback chair at the center of the car. [PAUSE: 2.0]
        Listening to the rain on the outer glass... and the low pop of warm cedar embers in the hearth. [PAUSE: 2.5]
        With a barely perceptible lift... the car continues its unhurried ascent through the great library. [PAUSE: 2.4]
        Every balcony that drifts past outside is dark... hushed... and asleep for the night. [PAUSE: 2.3]
        Only the scent of old paper... warm wood... and rain fills the air around you. [PAUSE: 1.8]
    """,

    # --- 30 STANDALONE MICRO-DRIFTS ---
    "drift_01": """
        Another walnut balcony glides slowly downward past the inner glass... [PAUSE: 2.2]
        Rows of leather book spines gleaming faintly in the amber light. [PAUSE: 1.6]
    """,
    "drift_02": """
        In the small corner hearth... a cedar log settles half an inch with a soft, warm crackle. [PAUSE: 2.4]
        Sending a gentle wave of heat across the rug. [PAUSE: 1.5]
    """,
    "drift_03": """
        On the outer wall of the shaft... night rain trails down the tall glass panes. [PAUSE: 2.3]
        Streaking the distant amber streetlights into soft blurs. [PAUSE: 1.5]
    """,
    "drift_04": """
        The heavy counterweight cables... hum a deep, unwavering tone above the walnut ceiling. [PAUSE: 2.3]
        Lifting the room without a jolt. [PAUSE: 1.5]
    """,
    "drift_05": """
        On the small side table beside your chair... an open book rests face up. [PAUSE: 2.2]
        A single cream page lifting slightly in the warm draft... and settling back down. [PAUSE: 1.8]
    """,
    "drift_06": """
        The car passes between two stone arches... [PAUSE: 1.8]
        Bringing a brief, hollow hush before the open atrium returns. [PAUSE: 2.0]
    """,
    "drift_07": """
        Green glass reading lamps on the passing desks outside... [PAUSE: 2.0]
        Glow like quiet emeralds in the dark tiers. [PAUSE: 1.6]
    """,
    "drift_08": """
        The tufted leather behind your shoulders... feels warm and supple from the hearth fire. [PAUSE: 2.3]
        Holding your weight completely. [PAUSE: 1.5]
    """,
    "drift_09": """
        Tall arched windows in the library atrium... drift slowly past across the open hall. [PAUSE: 2.3]
        Streaming with silver rainwater. [PAUSE: 1.5]
    """,
    "drift_10": """
        A rich scent of old parchment... cedar smoke... and beeswax polish hangs still in the car. [PAUSE: 2.4]
        Comforting and dry. [PAUSE: 1.5]
    """,
    "drift_11": """
        Felt guide rollers along the corners of the car... whisper softly against the smooth brass rails. [PAUSE: 2.4]
        Keeping the ascent completely level. [PAUSE: 1.5]
    """,
    "drift_12": """
        Out in the vast central hall... spiral iron staircases wind upward from floor to floor. [PAUSE: 2.3]
        Empty and still in the shadows. [PAUSE: 1.5]
    """,
    "drift_13": """
        A tiny orange spark floats up the back of the brick chimney... [PAUSE: 2.0]
        And vanishes into the warm dark. [PAUSE: 1.6]
    """,
    "drift_14": """
        The knitted wool throw over your knees... rises and falls with each slow breath. [PAUSE: 2.2]
        Heavy and soft. [PAUSE: 1.5]
    """,
    "drift_15": """
        As the car passes a high mezzanine... a row of tall terrestrial globes drifts downward out of sight. [PAUSE: 2.4]
        Their brass rings gleaming dimly. [PAUSE: 1.5]
    """,
    "drift_16": """
        Rain patters a little more steadily against the outer shaft window... [PAUSE: 2.2]
        Making the warm wooden car feel even cozier inside. [PAUSE: 1.6]
    """,
    "drift_17": """
        The walnut floor beneath the rug... gives a tiny, warm creak as the car rises. [PAUSE: 2.3]
        Solid and unhurried. [PAUSE: 1.5]
    """,
    "drift_18": """
        Thousands of quiet books line the walls outside... [PAUSE: 2.0]
        Absorbing every echo in the great building. [PAUSE: 1.6]
    """,
    "drift_19": """
        A heavy velvet curtain drapes beside the inner viewing pane... [PAUSE: 2.2]
        Still and undisturbed. [PAUSE: 1.5]
    """,
    "drift_20": """
        The brass grate in front of the hearth... shines with a steady copper reflection. [PAUSE: 2.3]
        Warming the soles of your feet. [PAUSE: 1.5]
    """,
    "drift_21": """
        Another level of tall wooden card catalogs... slides smoothly past the glass. [PAUSE: 2.3]
        Row after quiet row. [PAUSE: 1.5]
    """,
    "drift_22": """
        In the glass reflection... the glowing embers of your hearth appear to float out in the rainy night. [PAUSE: 2.4]
        Warm light suspended in the dark. [PAUSE: 1.5]
    """,
    "drift_23": """
        A gentle draft from the ceiling vent... stirs the corner of a parchment map on the wall. [PAUSE: 2.3]
        With a dry, papery whisper. [PAUSE: 1.5]
    """,
    "drift_24": """
        High overhead... the skylight roof of the library is still lost in the upper shadows. [PAUSE: 2.3]
        Leaving endless room to rise. [PAUSE: 1.5]
    """,
    "drift_25": """
        The low hum of the lift mechanism... blends with the rain and the dying embers. [PAUSE: 2.3]
        Forming a single, sleepy chord. [PAUSE: 1.5]
    """,
    "drift_26": """
        Wide reading tables on the passing floors... rest bare and polished under the dim sconces. [PAUSE: 2.3]
        Waiting in the quiet night. [PAUSE: 1.5]
    """,
    "drift_27": """
        Your hands rest heavy on the rounded leather armrests... [PAUSE: 2.0]
        Completely relaxed. [PAUSE: 1.5]
    """,
    "drift_28": """
        Drops of rain gather on the outer brass mullion... [PAUSE: 2.0]
        And slide down the glass in a slow silver thread. [PAUSE: 1.6]
    """,
    "drift_29": """
        The embers in the brick hearth sink into a deep, cherry-red glow... [PAUSE: 2.3]
        Radiating steady heat without a sound. [PAUSE: 1.5]
    """,
    "drift_30": """
        Floor after quiet floor drifts downward into the dark... [PAUSE: 2.2]
        As the warm car carries you smoothly upward into sleep. [PAUSE: 1.6]
    """,

    # --- 3 ROTATING LUCID SEEDS ---
    "lucid_seed_1": """
        As the glass room rises through the quiet library... [PAUSE: 2.2]
        Your body sleeps deeply... while a calm spark of awareness stays awake inside the dream. [PAUSE: 2.4]
        Knowing softly... [PAUSE: 1.8] that you are dreaming. [PAUSE: 1.8]
    """,
    "lucid_seed_2": """
        Whenever you see these endless shelves drifting past later tonight... [PAUSE: 2.2]
        You will recognize gently that you are dreaming... [PAUSE: 2.0]
        Warm... safe... and deeply asleep. [PAUSE: 1.8]
    """,
    "lucid_seed_3": """
        The library around you has opened into the dream world. [PAUSE: 2.2]
        And you can rest inside this warm room... [PAUSE: 1.8] knowing it is all a dream. [PAUSE: 1.8]
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
    print(f"Rendering {len(SCRIPTS)} Library Elevator clips...")
    for name, script in SCRIPTS.items():
        out = os.path.join(OUTPUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {out}")
            continue
        print(f" -> {out}")
        render(script, out)
    print("Library Elevator clips complete!")
