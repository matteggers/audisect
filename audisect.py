from transcriber import run_transcription
from sentimentAnalyzer import add_files_to_list, analysis_wrapper
import sentimentAnalyzer
import click
from pathlib import Path

@click.command()
@click.option("--input", prompt="Location of audio files", help="Where your audio files are stored")
@click.option("--size", default="medium", help="Whisper model size.")

def main(input, size):
    # where script lives (docker necessary)
    script_dir = Path(__file__).parent.resolve()

    # should implement this in other parts of script, makes it so much easier lol
    transcription_dir = script_dir / "transcriptions"
    data_dir = script_dir / "data"

    transcription_dir.mkdir(exist_ok=True)
    data_dir.mkdir(exist_ok=True)

    print(f"Text directory: {data_dir}")
    print(f"Transcription directory: {transcription_dir}")
    print(f"Input audio path: {input}")
    print(f"Model size: {size}")

    # Transcribe
    run_transcription(input, str(transcription_dir), size)
    print("Transcription completed")

    # Analyze
    text_files = add_files_to_list(str(transcription_dir), extensions={'.txt'})
    print(f"Text files found: {text_files}")
    analysis_wrapper(text_files)

if __name__ == "__main__":
    main()
