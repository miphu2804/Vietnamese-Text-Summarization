import logging
from typing import List, Dict, Any

from src.engine.STT import SpeechToText
from src.engine.summarizer import TextToSummarizer
from src.app_config import app_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnifiedService:
    """Unified service for Vietnamese Speech-to-Text and Text-to-Summary processing"""

    def __init__(self, stt_model_name: str = None):
        """Initialize speech pipeline with STT and text summarization services"""
        self.stt_model_name = stt_model_name or app_config.STT_MODEL_NAME or "khanhld/chunkformer-ctc-large-vie"
        self.stt_service = SpeechToText(self.stt_model_name)
        self.summarizer = TextToSummarizer()

    def check_format(self, audio_path: str) -> str:
        """Check and convert audio to WAV format if needed"""
        if not audio_path.lower().endswith('.wav'):
            return self.stt_service.convert_to_wav(audio_path)
        return audio_path

    def transcribe_and_summarize(self, audio_path: str) -> Dict[str, Any]:
        """Complete pipeline: Transcribe audio to text, then summarize the transcribed text"""
        wav_path = self.check_format(audio_path)
        transcription = self.stt_service.transcribe(audio_path=wav_path)
        summary = self.summarizer.summarize(transcription)

        return {
            "transcription": transcription,
            "summary": summary,
            "original_audio_path": audio_path
        }

    def batch_transcribe_and_summarize(self, audio_paths: List[str]) -> List[Dict[str, Any]]:
        """Batch pipeline: Transcribe multiple audio files and summarize each"""
        wav_paths = [self.check_format(path) for path in audio_paths]
        transcriptions = self.stt_service.batch_transcribe(audio_paths=wav_paths)
        results = []

        for i, transcription in enumerate(transcriptions):
            try:
                summary = self.summarizer.speak(transcription)

                results.append({
                    "transcription": transcription,
                    "summary": summary,
                    "original_audio_path": audio_paths[i],
                    "index": i
                })
            except Exception as e:
                results.append({
                    "transcription": transcription,
                    "summary": None,
                    "original_audio_path": audio_paths[i],
                    "index": i,
                    "error": str(e)
                })

        return results

    def transcribe_audio(self, audio_path: str) -> str:
        """Transcribe audio to text only"""
        wav_path = self.check_format(audio_path)
        return self.stt_service.transcribe(audio_path=wav_path)

    def summarize_text(self, text: str) -> str:
        """Summarize text only using seq2seq model"""
        return self.summarizer.summarize(text)


if __name__ == "__main__":
    unified_service = UnifiedService()

    # Test with a news video file (change to your actual file path)
    video_file = "/home/miphu/Downloads/[VTV1 Bản tin Thời sự 16h ngày 19⧸11⧸2021] Phát triển ngân hàng số trong tiến trình.mp4"  # or .mp3, .m4a, etc.

    try:
        print(f"Processing news file: {video_file}")
        result = unified_service.transcribe_and_summarize(video_file)

        print("\n=== TRANSCRIPTION ===")
        print(result['transcription'])

        print("\n=== SUMMARY ===")
        print(result['summary'])

        print(f"\nOriginal file: {result['original_audio_path']}")

    except FileNotFoundError:
        print(f"File not found: {video_file}")
        print("Please update the path to your news video/audio file")
    except Exception as e:
        print(f"Error processing file: {e}")