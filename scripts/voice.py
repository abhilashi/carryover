#!/usr/bin/env python3
"""Carryover CLI voice I/O helper.

The "call" without a phone number: it speaks a prompt, records your spoken
answer from the local mic (auto-stops on silence), transcribes it, and prints
ONLY the transcript to stdout so the calling skill can capture it.

Subcommands
-----------
  voice.py check            Verify mic + speech-to-text are usable. Exit 0 if voice
                            mode is fully available, non-zero (with a reason on
                            stderr) otherwise — the skill falls back to typing.
  voice.py speak "text"     Speak text aloud (macOS `say`, or OpenAI TTS).
  voice.py ask "question"   Speak the question, record the answer, transcribe it,
                            print the transcript to stdout.

Environment
-----------
  OPENAI_API_KEY        Required for speech-to-text (and for OpenAI TTS).
  CARRYOVER_TTS         "say" (default, macOS, free) | "openai" (needs key).
  CARRYOVER_STT_MODEL   default: gpt-4o-mini-transcribe
  CARRYOVER_TTS_VOICE   default: alloy (OpenAI TTS only)
  CARRYOVER_VAD_THRESHOLD  override silence threshold (float RMS, e.g. 0.012)

Design rule: stdout carries the transcript and nothing else. All status,
prompts, and errors go to stderr.
"""
import os
import sys
import json
import shutil
import tempfile
import subprocess

SR = 16000  # sample rate for capture / STT


def err(*a):
    print(*a, file=sys.stderr, flush=True)


def have_key():
    return bool(os.environ.get("OPENAI_API_KEY"))


# ----------------------------------------------------------------------------- TTS

def _play(path):
    for player in ("afplay", "ffplay", "mpv"):
        if shutil.which(player):
            args = [player, path]
            if player == "ffplay":
                args = ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path]
            subprocess.run(args, check=False)
            return True
    return False


def speak(text):
    mode = os.environ.get("CARRYOVER_TTS", "say")
    if mode == "openai" and have_key():
        try:
            voice = os.environ.get("CARRYOVER_TTS_VOICE", "alloy")
            mp3 = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
            payload = json.dumps({"model": "tts-1", "voice": voice, "input": text})
            subprocess.run(
                ["curl", "-sS", "https://api.openai.com/v1/audio/speech",
                 "-H", f"Authorization: Bearer {os.environ['OPENAI_API_KEY']}",
                 "-H", "Content-Type: application/json",
                 "-d", payload, "--output", mp3],
                check=True)
            if _play(mp3):
                return
        except Exception as e:  # noqa: BLE001
            err(f"[voice] OpenAI TTS failed ({e}); falling back to `say`")
    # macOS native, free, offline
    if shutil.which("say"):
        subprocess.run(["say", text], check=False)
    else:
        err(f"[voice] (no TTS available) {text}")


# ----------------------------------------------------------------------------- STT

def record(max_seconds=60, start_timeout=8.0, silence_limit=1.6):
    """Record from the default mic until ~silence_limit seconds of silence after
    speech begins. Returns a numpy float32 array, or None if no speech detected."""
    import numpy as np
    import sounddevice as sd

    block = int(SR * 0.1)  # 100 ms
    frames, silence_blocks, started, elapsed = [], 0, False, 0.0

    def rms(d):
        return float(np.sqrt(np.mean(d.astype("float64") ** 2)) + 1e-12)

    with sd.InputStream(samplerate=SR, channels=1, dtype="float32",
                        blocksize=block) as stream:
        env = os.environ.get("CARRYOVER_VAD_THRESHOLD")
        if env:
            threshold = float(env)
        else:
            cal = []
            for _ in range(4):  # ~0.4s ambient calibration
                d, _ = stream.read(block)
                cal.append(rms(d))
            threshold = max(float(np.mean(cal)) * 3.0, 0.01)
        err(f"[voice] listening… (threshold={threshold:.4f}, pause when you're done)")
        while True:
            data, _ = stream.read(block)
            frames.append(data.copy())
            elapsed += 0.1
            if rms(data) > threshold:
                started, silence_blocks = True, 0
            elif started:
                silence_blocks += 1
            if started and silence_blocks * 0.1 >= silence_limit:
                break
            if not started and elapsed >= start_timeout:
                return None
            if elapsed >= max_seconds:
                break
    return np.concatenate(frames, axis=0)


def transcribe(audio):
    import soundfile as sf
    wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    sf.write(wav, audio, SR)
    model = os.environ.get("CARRYOVER_STT_MODEL", "gpt-4o-mini-transcribe")
    out = subprocess.run(
        ["curl", "-sS", "https://api.openai.com/v1/audio/transcriptions",
         "-H", f"Authorization: Bearer {os.environ['OPENAI_API_KEY']}",
         "-F", f"model={model}",
         "-F", f"file=@{wav}",
         "-F", "response_format=json"],
        capture_output=True, text=True)
    try:
        return json.loads(out.stdout).get("text", "").strip()
    except Exception:  # noqa: BLE001
        err(f"[voice] transcription error: {out.stdout[:300]} {out.stderr[:300]}")
        return ""


# ----------------------------------------------------------------------------- commands

def cmd_check():
    ok = True
    try:
        import numpy  # noqa: F401
        import soundfile  # noqa: F401
        import sounddevice as sd
        ins = [d for d in sd.query_devices() if d.get("max_input_channels", 0) > 0]
        if not ins:
            err("[voice] no input (microphone) device found")
            ok = False
        else:
            err(f"[voice] mic OK ({ins[0]['name']})")
    except Exception as e:  # noqa: BLE001
        err(f"[voice] audio deps missing ({e}) — run: pip install -r requirements.txt")
        ok = False
    if have_key():
        err("[voice] OPENAI_API_KEY present — speech-to-text available")
    else:
        err("[voice] OPENAI_API_KEY not set — speech-to-text unavailable")
        ok = False
    err("[voice] TTS:", "OpenAI" if os.environ.get("CARRYOVER_TTS") == "openai"
        else ("macOS `say`" if shutil.which("say") else "none"))
    sys.exit(0 if ok else 1)


def cmd_speak(text):
    speak(text)


def cmd_ask(question):
    speak(question)
    audio = record()
    if audio is None:
        err("[voice] no speech detected")
        sys.exit(3)
    text = transcribe(audio)
    if not text:
        err("[voice] empty transcript")
        sys.exit(4)
    err(f"[voice] heard: {text}")
    print(text)  # stdout = transcript only


def main():
    if len(sys.argv) < 2:
        err(__doc__)
        sys.exit(2)
    cmd = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else ""
    if cmd == "check":
        cmd_check()
    elif cmd == "speak":
        cmd_speak(arg)
    elif cmd == "ask":
        cmd_ask(arg)
    else:
        err(f"unknown command: {cmd}")
        sys.exit(2)


if __name__ == "__main__":
    main()
