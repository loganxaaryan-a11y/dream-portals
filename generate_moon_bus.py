import os
import soundfile as sf
from kokoro import KPipeline

# Initialize Kokoro pipeline (American English)
pipeline = KPipeline(lang_code='a')

# Output directory for our first portal
OUTPUT_DIR = "audio/moon_bus"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# PORTAL #1: BUS TO THE MOON (Modular Script Library)
# ---------------------------------------------------------
SCRIPTS = {
    "departure": """
        The doors of the midnight bus fold shut behind you... with a soft, pressurized sigh.
        Outside, the streetlights of the sleeping city are already blurring into warm amber ribbons.
        You sink deep into the wide velvet seat by the window.
        The air inside the cabin is cool, quiet, and still.
        Beneath your feet... you feel the deep, steady hum of the lunar engines... warming up.
        There is nowhere you need to steer... nothing you need to remember.
        As the bus tilts gently upward... lifting off the pavement... your shoulders drop... and your eyelids grow heavy.
    """,

    "drift_1": """
        Outside the wide glass window... the last layer of silver night-clouds parts like silk curtains.
        Below the bus, the Earth curves away... glowing in deep ocean blues and quiet, golden constellations of tiny towns.
        The cabin lights dim to a soft, twilight indigo.
        Every breath you take matches the slow, weightless glide of the wheels through the dark.
    """,

    "drift_2": """
        Resting on the small tray table beside you... is a warm porcelain cup of starlight tea.
        Slow spirals of silver steam curl upward into the quiet air... carrying a faint scent of rain and vanilla.
        The warmth radiates softly against your hands... loosening every muscle in your fingers... your wrists... your arms.
    """,

    "drift_3": """
        Far out to the left of the bus... a school of translucent, glowing whales drifts past in slow motion.
        They swim effortlessly through the dark ether between the stars... their long tails moving like ribbons under water.
        You watch them pass in complete silence... feeling just as weightless... just as unhurried.
    """,

    "drift_4": """
        The bus glides onto an invisible highway of pale moonlight... stretching forward into the calm horizon.
        Across the aisle, the empty velvet seats glow softly in the silver reflection.
        A faint, soothing vibration travels through the armrest... humming a slow, rhythmic lullaby through your entire body.
    """,

    "drift_5": """
        Through the panoramic roof glass above your seat... a slow curtain of lavender nebula dust drifts over the bus.
        Tiny sparks of soft light tap silently against the windshield... like warm summer fireflies in deep space.
        Your mind grows quieter with every mile... drifting further from today... and deeper into the stillness.
    """,

    "drift_6": """
        Ahead in the distance... the pale, quiet curve of the Moon grows larger in the front windshield.
        Its craters look like soft valleys of velvet gray and silver sand... peaceful, ancient, and completely silent.
        You sink an inch deeper into the cushions... letting the gentle motion carry you the rest of the way.
    """,

    "lucid_seed": """
        Notice how effortless it is... to simply watch this world unfold around you.
        The bus... the silver light outside the glass... all of it is being painted by your own quiet mind.
        You are safe inside your body... and your mind is drifting into a dream.
        Soon, when this bus comes to a gentle stop... you will remember that you are dreaming... free to step off into the silver light... and explore wherever you wish.
    """
}

print("Generating 'Bus to the Moon' audio clips with Kokoro-82M...")

for clip_name, text in SCRIPTS.items():
    clean_text = " ".join(line.strip() for line in text.strip().splitlines())
    print(f" -> Rendering {clip_name}.wav ...")

    # 'af_nicole' is Kokoro's softest, breathiest whisper-like voice.
    # speed=0.80 slows the cadence down to ~85 words per minute for sleep induction.
    generator = pipeline(clean_text, voice='af_nicole', speed=0.80, split_pattern=r'\n+')

    audio_segments = []
    for _, _, audio in generator:
        audio_segments.extend(audio)

    output_path = os.path.join(OUTPUT_DIR, f"{clip_name}.wav")
    sf.write(output_path, audio_segments, 24000)

print(f"\nDone! All 8 modular clips saved inside '{OUTPUT_DIR}/'.")
