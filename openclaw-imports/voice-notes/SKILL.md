---
name: voice-notes
description: Send voice notes and transcribe incoming audio. Use when a user sends a voice note, asks for a voice reply, or wants text read aloud. Combines local Whisper transcription with ElevenLabs TTS.
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["sag","bash"]}}}
---

# Voice Notes

## CRITICAL: How to send voice notes

**DO NOT use the built-in `tts` tool.** It generates audio but `NO_REPLY` blocks delivery — the user will never receive the voice note.

**ALWAYS use `sag` via `exec`**, then include `MEDIA:/path` in your reply text. This is the ONLY method that works for WhatsApp delivery.

### Correct pattern (ALWAYS use this):

```bash
sag -o /tmp/voice-reply.ogg "Your message here"
```

Then in your reply text, include:
```
MEDIA:/tmp/voice-reply.ogg
```

**You MUST include `MEDIA:/path` in your actual text reply.** Do NOT reply with `NO_REPLY` after generating audio — that kills delivery.

### For long messages, split into parts:

If the text is longer than ~500 characters, split into 2-3 shorter voice notes:

```bash
sag -o /tmp/voice-part1.ogg "First part of the message..."
```
Reply with: `MEDIA:/tmp/voice-part1.ogg`

Then:
```bash
sag -o /tmp/voice-part2.ogg "Second part of the message..."
```
Reply with: `MEDIA:/tmp/voice-part2.ogg`

### Voice options

```bash
sag voices              # list all voices
sag -v Daniel "text"    # use specific voice
sag -v Roger "text"     # laid-back casual
sag -v Alice "text"     # clear educator
```

### Expression tags (v3 model)

Add emotion to speech:
- `[whispers]` — quiet, intimate
- `[shouts]` — loud, emphatic
- `[excited]` — energetic
- `[sarcastic]` — dry humor
- `[laughs]` — laughter
- `[sighs]` — exhale
- `[short pause]` — brief pause

Example:
```bash
sag -o /tmp/reply.ogg "[excited] Great news! [short pause] Everything is set up and ready to go."
```

## Transcribe incoming audio (free, local)

When a user sends a voice note (audio/ogg, audio/m4a, etc.), transcribe it locally (free, no API key):

```bash
bash /data/.openclaw/workspace/scripts/transcribe.sh /path/to/audio.ogg
```

**DO NOT use the OpenAI Whisper API** — it has quota errors. Always use the local transcription script above.

Options:
- `--language en` — force English (auto-detects by default)
- `--model tiny` — faster but less accurate (default: base)

If the venv is missing, recreate it:
```bash
python3 -m venv /data/.openclaw/workspace/whisper-venv
/data/.openclaw/workspace/whisper-venv/bin/pip install faster-whisper
```

## Full workflow: receive voice, reply with voice

1. User sends voice note -> audio saved to /tmp or attachment path
2. Transcribe: `bash /data/.openclaw/workspace/scripts/transcribe.sh /path/to/audio.ogg`
3. Process the transcribed text normally
4. Generate voice reply: `sag -o /tmp/voice-reply.ogg "your response"`
5. Reply with: `MEDIA:/tmp/voice-reply.ogg` (plus any text you want to send)

## Troubleshooting

- If sag fails: check `ELEVENLABS_API_KEY` env var
- If transcription is slow: use `--model tiny` for faster results
- Supported audio formats: ogg, mp3, m4a, wav, webm
- **Voice note not delivered?** You probably used the built-in `tts` tool or replied with `NO_REPLY`. Use `sag` via `exec` and include `MEDIA:/path` in your reply text instead.
