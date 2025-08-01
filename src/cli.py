import click
from pathlib import Path
import logging
from .pipeline import Pipeline
import warnings

# FIXME Remove the warning through update
warnings.filterwarnings(
    "ignore",
    message=".*encoder_attention_mask is deprecated and will be removed in version 4.55.0 for RobertaSdpaSelfAttention.forward.*"
)

@click.command()
@click.option(
    "--input", "-i",
    "input_dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    prompt="Location of audio files",
    help="Directory containing audio files to process."
)
@click.option(
    "--output", "-o",
    "output_dir",
    type=click.Path(file_okay=False, path_type=Path),
    default="output",
    show_default=True,
    help="Directory to write transcripts, sentiment, and logs."
)
@click.option(
    "--size", "-s",
    "model_size",
    default="medium",
    show_default=True,
    help="Whisper model size to use for transcription."
)

def main(input_dir: Path, output_dir: Path, model_size: str):
    # Entry point: find audio files, transcribe, analyze sentiment, and save results.


    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    input_dir = input_dir.resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    logging.info("Starting pipeline. input=%s output=%s model_size=%s",
                 input_dir, output_dir, model_size, )

    pipeline = Pipeline(
        input_dir=input_dir,
        output_dir=output_dir,
        model_size=model_size,
    )
    pipeline.run()

if __name__ == "__main__":
    main()