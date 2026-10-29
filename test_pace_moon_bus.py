import os, re
import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')
SAMPLE_RATE = 24000
os.makedirs("audio/moon_bus", exist_ok=True)

PACE_TEST_SCRIPTS = {
    "departure": """
        The doors of the midnight bus fold shut behind you... with a soft, pressurized sigh. [PAUSE: 2.2]
        Outside, the streetlights of the sleeping city are already blurring into warm amber ribbons. [PAUSE: 2.0]
        You sink deep into the wide velvet seat by the window. [PAUSE: 1.8]
        The air inside the cabin is cool, quiet, and still. [PAUSE: 2.0]
        Beneath your feet... you feel the deep, steady hum of the lunar engines... warming up. [PAUSE: 2.2]
        There is nowhere you need to steer... nothing you need to remember. [PAUSE: 2.0]
        As the bus tilts gently upward... lifting off the pavement... your shoulders drop... and your eyelids grow heavy. [PAUSE: 1.8]
    """,
    "drift_1": """
        Outside the wide glass window... the last layer of silver night-clouds parts like silk curtains. [PAUSE: 2.2]
        Below the bus, the Earth curves away... glowing in deep ocean blues and quiet, golden constellations of tiny towns. [PAUSE: 2.0]
        The cabin lights dim to a soft, twilight indigo. [PAUSE: 1.8]
        Every breath you take matches the slow, weightless glide of the wheels through the dark. [PAUSE: 1.5]
    """,
    "drift_2": """
        Resting on the small tray table beside you... is a warm porcelain cup of starlight tea. [PAUSE: 2.0]
        Slow spirals of silver steam curl upward into the quiet air... carrying a faint scent of rain and vanilla. [PAUSE: 2.2]
        The warmth radiates softly against your hands... loosening every muscle in your fingers... your wrists... your arms. [PAUSE: 1.8]
    """,
    "drift_3": """
        Far out to the left of the bus... a school of translucent, glowing whales drifts past in slow motion. [PAUSE: 2.2]
        They swim effortlessly through the dark ether between the stars... their long tails moving like ribbons under water. [PAUSE: 2.0]
        You watch them pass in complete silence... feeling just as weightless... just as unhurried. [PAUSE: 1.8]
    """,
    "drift_4": """
        The bus glides onto an invisible highway of pale moonlight... stretching forward into the calm horizon. [PAUSE: 2.0]
        Across the aisle, the empty velvet seats glow softly in the silver reflection. [PAUSE: 2.0]
        A faint, soothing vibration travels through the armrest... humming a slow, rhythmic lullaby through your entire body. [PAUSE: 1.8]
    """,
    "drift_5": """
        Through the panoramic roof glass above your seat... a slow curtain of lavender nebula dust drifts over the bus. [PAUSE: 2.2]
        Tiny sparks of soft light tap silently against the windshield... like warm summer fireflies in deep space. [PAUSE: 2.0]
        Your mind grows quieter with every mile... drifting further from today... and deeper into the stillness. [PAUSE: 1.8]
    """,
    "drift_6": """
        Ahead in the distance... the pale, quiet curve of the Moon grows larger in the front windshield. [PAUSE: 2.0]
        Its craters look like soft valleys of velvet gray and silver sand... peaceful, ancient, and completely silent. [PAUSE: 2.2]
        You sink an inch deeper into the cushions... letting the gentle motion carry you the rest of the way. [PAUSE: 1.8]
    """,
    "lucid_seed": """
        Notice how effortless it is... to simply watch this world unfold around you. [PAUSE: 2.2]
        The bus... the silver light outside the glass... all of it is being painted by your own quiet mind. [PAUSE: 2.0]
        You are safe inside your body... and your mind is drifting into a dream. [PAUSE: 2.2]
        Soon, when this bus comes to a gentle stop... you will remember that you are dreaming... free to step off into the silver light... and explore wherever you wish. [PAUSE: 1.8]
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

if __name__ == "__main__":
    print("Rendering 8 paced Moon Bus clips...")
    for name, script in PACE_TEST_SCRIPTS.items():
        out = f"audio/moon_bus/{name}.wav"
        print(f" -> {out}")
        render(script, out)
    print("Moon paced clips complete!")
