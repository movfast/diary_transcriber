"""
Voice Transcriber
-----------------
Records audio from the microphone, transcribes it locally using OpenAI Whisper,
and saves the result as a diary entry in Notion.
"""

import os
from datetime import date

import whisper
import sounddevice as sd
import scipy.io.wavfile as wav
from dotenv import load_dotenv
from notion_client import Client

load_dotenv()


class VoiceTranscriber:
    """Records speech, transcribes it with Whisper, and saves it to Notion."""

    SAMPLE_RATE = 44100
    WHISPER_MODEL = "medium"
    LANGUAGE = "no"  # Change to "en" for English, or remove for auto-detect

    def __init__(self):
        self.notion = Client(auth=os.environ["DIARY_UPDATER_TOKEN"])
        self.page_id = os.environ["NOTION_PAGE_ID"]

    # ──────────────────────────────────────────────
    # Recording
    # ──────────────────────────────────────────────

    def record_audio(self, duration: int = 30, filename: str = "entry.wav") -> str:
        """Record audio from the microphone for a given number of seconds."""
        print(f"Recording for {duration} seconds... Speak now!")
        audio = sd.rec(
            int(duration * self.SAMPLE_RATE),
            samplerate=self.SAMPLE_RATE,
            channels=1
        )
        sd.wait()
        wav.write(filename, self.SAMPLE_RATE, audio)
        print("Recording done!")
        return filename

    # ──────────────────────────────────────────────
    # Transcription
    # ──────────────────────────────────────────────

    def transcribe(self, filename: str) -> str:
        """Transcribe an audio file using Whisper."""
        print("Transcribing...")
        model = whisper.load_model(self.WHISPER_MODEL)
        result = model.transcribe(filename, language=self.LANGUAGE)
        text = result["text"].strip()
        print(f"Transcribed: {text}")
        return text

    # ──────────────────────────────────────────────
    # Notion
    # ──────────────────────────────────────────────

    def write_diary_entry(self, entry_text: str) -> None:
        """Append a transcribed diary entry to the Notion page."""
        today = date.today().strftime("%B %d, %Y")
        self.notion.blocks.children.append(
            block_id=self.page_id,
            children=[
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": today}}]
                    },
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": entry_text}}]
                    },
                },
            ],
        )
        print(f"Diary entry saved to Notion for {today}!")

    # ──────────────────────────────────────────────
    # Main flow
    # ──────────────────────────────────────────────

    def run(self) -> None:
        """Run the full record -> transcribe -> save flow."""
        duration = int(input("How many seconds do you want to record? (default 30): ") or 30)

        audio_file = self.record_audio(duration=duration)
        transcript = self.transcribe(audio_file)

        print("\n--- Your transcribed entry ---")
        print(transcript)

        confirm = input("\nSave this to Notion? (y/n): ")
        if confirm.lower() == "y":
            self.write_diary_entry(transcript)
        else:
            print("Entry discarded.")


if __name__ == "__main__":
    VoiceTranscriber().run()