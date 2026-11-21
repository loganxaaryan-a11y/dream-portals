import os, re, math, random, ast, traceback
import numpy as np
import soundfile as sf
from kokoro import KPipeline

SAMPLE_RATE = 24000
BASE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE, "audio", "attic_library_blend_test")
os.makedirs(OUT_DIR, exist_ok=True)
BLEND_PATH = os.path.join(BASE, "voice-test-2026-11-20", "17_blend_nicole70_heart30_082.pt")
SPEED = 0.86
FADE_MS = 150
ROOM_TONE_RMS_DBFS = -45.0
PAUSE_SCALE = 0.85
# NO bed, NO player LP, NO gain bake (gain=1.0)

src = open(os.path.join(BASE, "generate_attic_library.py")).read()
tree = ast.parse(src)
SCRIPTS = None
for node in tree.body:
    if isinstance(node, ast.Assign) and any(getattr(t, 'id', '') == 'SCRIPTS' for t in node.targets):
        SCRIPTS = ast.literal_eval(node.value); break
assert SCRIPTS and len(SCRIPTS) == 36

def cosine_fade(a, fade_ms=FADE_MS):
    fs = int(SAMPLE_RATE * fade_ms / 1000.0)
    if len(a) < fs * 2: return a
    a = a.copy()
    ramp = 0.5 - 0.5 * np.cos(np.linspace(0, math.pi, fs))
    a[:fs] *= ramp.astype(np.float32); a[-fs:] *= ramp[::-1].astype(np.float32)
    return a

try:
    from scipy.signal import lfilter
    def one_pole_lowpass(x, fc, fs=SAMPLE_RATE):
        alpha = 1.0 - math.exp(-2.0 * math.pi * fc / fs)
        return lfilter([alpha], [1, -(1-alpha)], x.astype(np.float64)).astype(np.float32)
    print("scipy lfilter available", flush=True)
except Exception as e:
    print(f"no scipy ({e})", flush=True)
    def one_pole_lowpass(x, fc, fs=SAMPLE_RATE):
        alpha = 1.0 - math.exp(-2.0 * math.pi * fc / fs)
        y = np.empty_like(x, dtype=np.float64); acc = 0.0
        for i in range(len(x)):
            acc += alpha * (float(x[i]) - acc); y[i] = acc
        return y.astype(np.float32)

def make_room_tone(n_samples, rng):
    if n_samples <= 0: return np.zeros(0, dtype=np.float32)
    white = rng.standard_normal(n_samples).astype(np.float64)
    brown = np.cumsum(white)
    brown = brown - np.linspace(brown[0], brown[-1], n_samples)
    brown = one_pole_lowpass(brown.astype(np.float32), 400.0).astype(np.float64)
    rms = np.sqrt(np.mean(brown**2)) or 1.0
    target = 10 ** (ROOM_TONE_RMS_DBFS / 20.0)
    return (brown / rms * target).astype(np.float32)

def valid_wav(path):
    try:
        info = sf.info(path); return info.samplerate == 24000 and info.frames > 0
    except Exception: return False

def parse_sentences(marked):
    """Return (sentences, between_pauses_orig, final_pause_orig_or_None, mid_converted_count)
    Sentence = text up to terminal . ! ? (not ...) followed by a [PAUSE:] marker, or end of script.
    Mid-sentence [PAUSE:] (prev text ends with ... or no terminal punct) -> converted to ' ... ' text, no splice.
    """
    tokens = re.split(r'(\[PAUSE:\s*\d+(?:\.\d+)?\])', marked.strip())
    sentences, pauses = [], []
    current = ""
    mid_converted = 0
    final_pause = None
    for tok in tokens:
        tok = tok.strip()
        if not tok: continue
        m = re.match(r'\[PAUSE:\s*(\d+(?:\.\d+)?)\]', tok)
        if m:
            orig = float(m.group(1))
            prev = current.strip()
            is_terminal = prev.endswith(('.', '!', '?')) and not prev.endswith('...')
            if is_terminal and prev:
                sentences.append(prev); pauses.append(orig); current = ""
            else:
                # mid-sentence: convert to ellipsis text
                if prev and not prev.endswith('...'):
                    current = prev + " ... "
                else:
                    current = prev + " "
                mid_converted += 1
        else:
            clean = " ".join(tok.splitlines()).strip()
            if clean:
                current = (current + " " + clean).strip() if current.strip() else clean
    if current.strip():
        sentences.append(current.strip())
    # pauses list: one per sentence boundary encountered; if last pause was after final sentence, it's in pauses with len==len(sentences)
    if len(pauses) == len(sentences) and sentences:
        final_pause = pauses.pop()  # trailing pause after last sentence
    # pad missing between-pauses with default 1.9
    while len(pauses) < max(0, len(sentences) - 1):
        pauses.append(1.9)
    return sentences, pauses, final_pause, mid_converted

def render(pipe, marked, out, clip_name):
    sentences, pauses_orig, final_pause, mid_conv = parse_sentences(marked)
    rng = np.random.default_rng(abs(hash(clip_name)) % (2**32))
    jitter_rng = random.Random(clip_name)
    parts = [make_room_tone(int(SAMPLE_RATE * 0.25), rng)]
    pause_log = []
    for i, sent in enumerate(sentences):
        gen = pipe(sent, voice=BLEND_PATH, speed=SPEED, split_pattern=r'\n+')
        arr = [seg for _, _, seg in gen for seg in seg]
        if not arr: raise RuntimeError(f"empty audio {clip_name} sent{i}: {sent[:60]!r}")
        parts.append(cosine_fade(np.array(arr, dtype=np.float32)))
        if i < len(pauses_orig):
            scaled = pauses_orig[i] * PAUSE_SCALE * jitter_rng.uniform(0.85, 1.15)
            pause_log.append((pauses_orig[i], round(scaled, 2)))
            parts.append(make_room_tone(int(SAMPLE_RATE * scaled), rng))
    if final_pause is not None:
        scaled = final_pause * PAUSE_SCALE * jitter_rng.uniform(0.85, 1.15)
        pause_log.append((final_pause, round(scaled, 2)))
        parts.append(make_room_tone(int(SAMPLE_RATE * scaled), rng))
    parts.append(make_room_tone(int(SAMPLE_RATE * 0.35), rng))
    sf.write(out, np.concatenate(parts), SAMPLE_RATE)
    return sentences, pause_log, mid_conv

def main():
    print(f"Blend exists={os.path.exists(BLEND_PATH)} scripts={len(SCRIPTS)} -> {OUT_DIR}", flush=True)
    # parse check first (no pipeline) — print sentence/pause counts for all
    for name, script in SCRIPTS.items():
        s, p, f, mc = parse_sentences(script)
        print(f"PARSE {name}: sentences={len(s)} between_pauses={len(p)} final={f} mid_converted={mc}", flush=True)
    print("Loading pipeline...", flush=True)
    pipe = KPipeline(lang_code='a')
    print("Pipeline loaded.", flush=True)
    done, skipped, failed = 0, 0, []
    report = []
    for name, script in SCRIPTS.items():
        out = os.path.join(OUT_DIR, f"{name}.wav")
        if valid_wav(out):
            print(f" -> skip existing {name}", flush=True); skipped += 1; continue
        try:
            print(f" -> {name}", flush=True)
            sents, plog, mc = render(pipe, script, out, name)
            info = sf.info(out); dur = info.frames / info.samplerate
            print(f"    OK {dur:.2f}s sentences={len(sents)} pauses={plog} mid_converted={mc}", flush=True)
            report.append((name, len(sents), len(plog), round(dur,2), mc))
            done += 1
        except Exception as e:
            print(f"    FAIL {name}: {e}", flush=True); traceback.print_exc(); failed.append(name)
    print(f"DONE rendered={done} skipped={skipped} failed={failed}", flush=True)
    for r in report: print(f"REPORT {r}", flush=True)

if __name__ == "__main__":
    main()
