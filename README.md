# diary_transcriber
Voice-to-Notion diary tool — records speech, transcribes locally with Whisper, and saves entries to Notion.

# 🎙️ Voice Transcriber

A command-line tool that records your voice, transcribes it locally using OpenAI Whisper, and saves the result as a diary entry in Notion.

No cloud transcription — everything runs on your own machine.

---

## Features

- **Live microphone recording** — choose how many seconds to record
- **Local transcription** — powered by OpenAI Whisper, no data sent to external servers
- **Multilingual** — configured for Norwegian by default, easily changed to any language
- **Notion integration** — saves transcribed entries with today's date directly to your Notion page
- **Review before saving** — see the transcription before deciding to save it

---

## Tech Stack

- [Python 3.10+](https://www.python.org/)
- [OpenAI Whisper](https://github.com/openai/whisper) — local speech-to-text
- [sounddevice](https://python-sounddevice.readthedocs.io/) — microphone recording
- [SciPy](https://scipy.org/) — audio file handling
- [Notion API](https://developers.notion.com/) — diary storage
- [python-dotenv](https://pypi.org/project/python-dotenv/) — environment variable management

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/voice-transcriber.git
cd voice-transcriber
```

### 2. Install system dependencies

**Mac:**
```bash
brew install ffmpeg portaudio
```

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg portaudio19-dev
```

**Windows:**
```bash
winget install ffmpeg
```

### 3. Install Python dependencies

```bash
pip install openai-whisper sounddevice scipy notion-client python-dotenv
```

### 4. Set up your API keys

Create a `.env` file in the project root:

```
DIARY_UPDATER_TOKEN=your_notion_integration_token
NOTION_PAGE_ID=your_notion_page_id
```

**Getting your keys:**
- **Notion integration token** → [notion.com/my-integrations](https://www.notion.com/my-integrations) (create an Internal integration)
- **Notion page ID** → the 32-character string at the end of your Notion page URL

### 5. Connect Notion

Open your Notion page, click **···** → **Add connections** → select your integration.

### 6. Run the app

```bash
python transcriber_diary.py
```

---

## How It Works

1. Run the script and choose how many seconds to record
2. Speak into your microphone
3. Whisper transcribes your speech locally on your machine
4. Review the transcription in the terminal
5. Confirm to save it to Notion, or discard it

---

## Configuration

You can adjust these settings at the top of `VoiceTranscriber`:

| Setting | Default | Description |
|---|---|---|
| `WHISPER_MODEL` | `medium` | Whisper model size: `tiny`, `base`, `small`, `medium`, `large` |
| `LANGUAGE` | `no` | Language code for transcription. Use `en` for English, or remove for auto-detect |
| `SAMPLE_RATE` | `44100` | Audio sample rate in Hz |

Larger Whisper models are more accurate but slower. `medium` is a good balance for most use cases.

---

## Project Structure

```
diary-transcriber/
├── transcriber_diary.py   # Main application
├── .env                   # API keys (never commit this!)
├── .gitignore
└── README.md
```

---

## Security

Never commit your `.env` file. Make sure your `.gitignore` includes:

```
.env
```

---

## License

MIT
