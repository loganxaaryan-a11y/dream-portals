import os
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code='a')

os.makedirs("audio/rainforest", exist_ok=True)
os.makedirs("audio/preflight/body_unwind", exist_ok=True)
os.makedirs("audio/preflight/mind_shuffle", exist_ok=True)

# ---------------------------------------------------------
# PORTAL #2: TRAIN TO THE RAINFOREST (True Micro-Modular Pool)
# Sized to measured Kokoro af_nicole @ 0.80x pace (~88.5 wpm)
# ---------------------------------------------------------

RAINFOREST_SCRIPTS = {
    # 3 Rotating Departures (~85-90 words / ~58-62 sec each)
    "departure_1": """
        You step inside the warm wooden sleeper car... and the heavy glass door slides shut behind you.
        The misty platform outside softens into the dark emerald trees.
        You sink onto the wide velvet bench... resting your cheek against the cool window pane.
        Beneath the floorboards, the wheels begin their slow, steady rhythm... clack-clack... clack-clack.
        Above the curved roof, warm tropical rain begins to tap against the metal.
        You are dry, enclosed, and completely safe... with nowhere to arrive... and nothing left to carry.
    """,

    "departure_2": """
        You are lying under a soft wool blanket... inside a dimly lit mahogany berth.
        Outside the thick glass window, the rainforest canopy is dark, quiet, and still.
        A gentle tremor moves through the wooden frame... as the train glides smoothly forward along the rails.
        Heavy raindrops begin to drum against the metal roof overhead... washing the night air clean.
        Every sway of the carriage rocks your body a little deeper into the mattress... warm, sheltered, and unhurried.
    """,

    "departure_3": """
        Inside the quiet observation dome car, the small brass lanterns dim to a warm amber glow.
        You lean back into a deep leather armchair... wrapped in stillness and soft shadow.
        All around the curved glass ceiling, heavy jungle rain falls in a slow, continuous curtain.
        Beneath you, the iron rails hum a low, rhythmic lullaby through the floor.
        The outside world is sealed away behind thick glass... leaving only the rain, the motion, and your quiet breath.
    """,

    # 30 Standalone Micro-Drifts (~15-18 words / ~10-12 sec each)
    # 15 clips/night (~16m total) or 28 clips/night (~28m total)
    "drift_01": "Broad emerald fern fronds brush past the wet window glass... glowing softly in the amber light from your cabin.",
    "drift_02": "Rainwater gathers in slow, heavy beads along the window frame... before sliding silently down the pane.",
    "drift_03": "A faint, warm scent of damp moss and rain-washed cedar drifts gently through the cabin air.",
    "drift_04": "The wheels keep their slow, unbroken rhythm over the rails... rocking your shoulders deeper into the seat.",
    "drift_05": "Pale silver mist curls between the dark tree trunks outside... floating weightlessly above the forest floor.",
    "drift_06": "Above your head, the rain on the metal roof blurs into a warm, continuous velvet hush.",
    "drift_07": "A small brass lamp beside the cushion casts a soft, steady circle of golden warmth across the wood.",
    "drift_08": "Through the high glass canopy, giant raindrops fall from broad banana leaves... in slow, silent motion.",
    "drift_09": "Tiny golden fireflies drift among the wet roots outside... glowing and fading like slow embers in the mist.",
    "drift_10": "The wooden walls of the carriage creak softly... holding you in a warm, dry pocket of quiet.",
    "drift_11": "The train glides across an old stone viaduct... high above a wide, slow-moving jungle river.",
    "drift_12": "Pale white night-orchids hang from the branches near the tracks... still and untouched by the rain.",
    "drift_13": "A gentle vibration hums through the floorboards... loosening the last tension in your hands and feet.",
    "drift_14": "Outside the glass, layers of dark green leaves fold into deeper and deeper shades of indigo shadow.",
    "drift_15": "The air inside the sleeper car stays cool and still... while the warm rain pours endlessly outside.",
    "drift_16": "A veil of silver fog rises from the warm earth... wrapping the carriage in soft, diffused light.",
    "drift_17": "Two luminous blue butterflies rest motionless on the underside of a giant leaf... sheltered from the rain.",
    "drift_18": "The track curves gently through a valley of tall bamboo... swaying in a slow, rhythmic wave.",
    "drift_19": "Condensation forms a soft halo on the inside of the glass... blurring the green world into smooth color.",
    "drift_20": "The low rumble of the wheels softens... as the rails pass over a bed of thick, damp moss.",
    "drift_21": "Warm amber light reflects dimly in the dark window... merging the cozy cabin with the misty trees.",
    "drift_22": "Every breath you exhale matches the slow, steady sway of the carriage gliding through the dark.",
    "drift_23": "Far out in the canopy, a soft sheet of silver rain drifts slowly across the treetops.",
    "drift_24": "The heavy velvet curtains by the window hang in still folds... absorbing every sharp sound.",
    "drift_25": "Water trickles in a gentle, musical stream along the outer gutter of the carriage roof.",
    "drift_26": "Pale moonlight filters through the high mist... turning the wet leaves outside into polished silver.",
    "drift_27": "The train moves without effort or hurry... gliding on an endless track through the quiet green night.",
    "drift_28": "Your eyelids rest heavy and warm... while the sound of the rain carries every thought away.",
    "drift_29": "Thick vines hang like quiet tapestries between the ancient trees... drifting slowly past the glass.",
    "drift_30": "The rhythm of the rails and the hush of the rain blend into one single, peaceful hum.",

    # 3 Rotating Lucid Seeds (~65 words / ~45 sec each)
    "lucid_seed_1": """
        Notice how effortlessly this rainforest drifts past your window.
        The rain on the roof... the warm wood around you... the silver mist between the trees... all of it is resting inside your own quiet awareness.
        As your body sinks deeper into sleep... this gentle awareness remains... ready to drift into the dreamscape on its own.
    """,

    "lucid_seed_2": """
        Everything outside this glass is being painted by your own resting mind.
        There is nothing you need to direct... and nothing you need to hold onto.
        As the carriage rocks you across the border of sleep... let the mist and the glowing leaves become the quiet beginning of your dream.
    """,

    "lucid_seed_3": """
        The sound of the tracks is fading into a soft, distant hum.
        Your body is heavy, warm, and fast asleep... while a quiet spark of awareness watches the emerald mist unfold.
        Let the train carry you smoothly into the dream... weightless, calm, and completely at peace.
    """
}

# ---------------------------------------------------------
# PRE-FLIGHT 1: +3m BODY UNWIND (10 Paced Clips)
# 10 clips (~12s each) + 8s silence gaps = ~3 minutes total
# ---------------------------------------------------------

BODY_UNWIND_CLIPS = [
    "Let your eyes stay softly closed... and take a slow, effortless breath in... letting the weight of the day drop away as you exhale.",
    "Bring your attention to your forehead and the space between your eyebrows... letting the skin smooth out... cool, quiet, and completely unhurried.",
    "Allow your jaw to part slightly... letting your tongue rest softly... as all the tiny muscles around your mouth and cheeks go slack.",
    "Feel the weight of your head sinking deeper into the pillow... supported, heavy, and free from holding anything up.",
    "Let your shoulders drop down away from your ears... melting heavy and warm into the surface beneath your back.",
    "Notice both of your arms... from your upper arms down through your elbows, your wrists, and the tips of your fingers... heavy and still.",
    "Feel your chest and stomach rise and fall on their own... slow, natural, and without any effort at all.",
    "Let the muscles along your spine and lower back soften... sinking another inch deeper into the mattress.",
    "Allow your hips, your thighs, and your knees to let go completely... heavy as warm stone.",
    "Feel the stillness travel down through your calves, your ankles, and the soles of your feet... your entire body warm, heavy, and ready for sleep."
]

# ---------------------------------------------------------
# PRE-FLIGHT 2: +5m MIND SHUFFLE (40 Pure Zero-Thought Objects)
# Dealt 25 per session (~4s clip + 6-10s random gap = ~5m total)
# Zero clocks, zero keys, zero money, zero work, zero sharp motion
# ---------------------------------------------------------

MIND_SHUFFLE_OBJECTS = [
    "A smooth grey river stone... resting on damp moss.",
    "A fluffy white cloud... drifting across a pale lavender sky.",
    "A blue ceramic mug... filled with warm chamomile tea.",
    "A single silver feather... settling onto soft grass.",
    "A ripe yellow lemon... resting on a wooden cutting board.",
    "A pinecone... lying on a bed of dry brown needles.",
    "A clear glass marble... resting on a dark velvet cloth.",
    "A single drop of dew... clinging to a green fern leaf.",
    "A round bowl... carved from smooth olive wood.",
    "A quiet puddle of rainwater... reflecting the evening sky.",
    "A handful of warm white sand... resting in an open palm.",
    "A woven wicker basket... filled with dried lavender stems.",
    "A small white seashell... half-buried in wet shoreline sand.",
    "A curved piece of driftwood... bleached pale silver by the sun.",
    "A wide satin ribbon... folded loosely on a linen sheet.",
    "A green apple... resting on a flat slate tile.",
    "A small porcelain saucer... holding a sprig of fresh mint.",
    "A soft puff of white cotton... resting in the shade.",
    "A smooth wooden button... lying on a knitted wool blanket.",
    "A pale green sea-glass pebble... smoothed by the tide.",
    "A tall river reed... leaning gently over a mirror-still pond.",
    "A piece of soft white chalk... resting on dark slate.",
    "A golden autumn leaf... floating motionless on calm water.",
    "A terracotta plant pot... warmed by the afternoon sun.",
    "A folded square of unbleached linen... on a cedar shelf.",
    "A clear quartz crystal... resting on a bed of dark soil.",
    "A dried lotus pod... lying on a woven bamboo mat.",
    "A smooth piece of white marble... cool in the evening air.",
    "A soft owl feather... resting in a patch of green clover.",
    "A small wooden bowl... filled with ripe red raspberries.",
    "A natural sea sponge... resting on smooth wet stone.",
    "A folded scarf of deep indigo silk... on a cushioned bench.",
    "A single acorn cap... resting on a mossy tree root.",
    "A curved clay roof tile... warm from the sun.",
    "A white porcelain bowl... filled with clear spring water.",
    "A wooden spool... wrapped in soft grey wool yarn.",
    "A pale pink rose petal... resting on a stone garden path.",
    "A smooth beeswax candle... unlit and smelling faintly of honey.",
    "A flat skipping stone... resting at the edge of a quiet lake.",
    "A soft ball of sage-green moss... resting in the crook of a tree."
]

def render_text(text, output_path):
    clean_text = " ".join(line.strip() for line in text.strip().splitlines())
    generator = pipeline(clean_text, voice='af_nicole', speed=0.80, split_pattern=r'\n+')
    audio = [seg for _, _, audio_seg in generator for seg in audio_seg]
    sf.write(output_path, audio, 24000)

if __name__ == "__main__":
    print("1. Rendering Portal #2: Train to the Rainforest (36 clips)...")
    for name, script in RAINFOREST_SCRIPTS.items():
        out = f"audio/rainforest/{name}.wav"
        if os.path.exists(out):
            print(f"   -> skip (already done) {out}")
            continue
        print(f"   -> {out}")
        render_text(script, out)

    print("\n2. Rendering +3m Body Unwind (10 paced clips)...")
    for i, line in enumerate(BODY_UNWIND_CLIPS, 1):
        out = f"audio/preflight/body_unwind/step_{i:02d}.wav"
        if os.path.exists(out):
            print(f"   -> skip (already done) {out}")
            continue
        print(f"   -> {out}")
        render_text(line, out)

    print("\n3. Rendering +5m Mind Shuffle Pool (40 object clips)...")
    for i, obj in enumerate(MIND_SHUFFLE_OBJECTS, 1):
        out = f"audio/preflight/mind_shuffle/obj_{i:02d}.wav"
        if os.path.exists(out):
            print(f"   -> skip (already done) {out}")
            continue
        print(f"   -> {out}")
        render_text(obj, out)

    print("\nDone! All Rainforest and Pre-Flight assets rendered.")
