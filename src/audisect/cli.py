import click
from pathlib import Path
import logging
from .pipeline import Pipeline
import warnings
import platform
import typer
import shutil
# FIXME Remove the warning through update
warnings.filterwarnings(
    "ignore",
    message=".*encoder_attention_mask is deprecated and will be removed in version 4.55.0 for RobertaSdpaSelfAttention.forward.*"
)


def _has(cmd: str) -> bool:
    return shutil.which(cmd) is not None

def _linux_only():
    if platform.system() != "Linux":
        typer.secho("This script is designed to run on Linux systems only.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    """Audisect"""
    pass

@click.command("run")
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

def run_cmd(input_dir: Path, output_dir: Path, model_size: str):
    """Run pipeline"""
    _linux_only()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    input_dir = input_dir.resolve()
    output_dir = Path(output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    logging.info("Starting pipeline. input=%s output=%s model_size=%s",
                 input_dir, output_dir, model_size)

    pipeline = Pipeline(
        input_dir=input_dir,
        output_dir=output_dir,
        model_size=model_size,
    )
    pipeline.run()

# Check sys requirements
@click.command("doctor")
def doctor_cmd():
    _linux_only()
    valid_sys = True
    
    if _has("ffmpeg"):
        click.echo("ffmpeg: CHECK", fg="green")
    else:
        click.secho("ffmpeg: NOT FOUND", fg="red")
        valid_sys = False
    
    try:
        import whisper; click.echo("whisper: CHECK", fg="green")
    except Exception as e:
        click.secho(f"whisper: NOT FOUND ({e})", fg="red")
        valid_sys = False  
    
    try:
        import torch; click.echo("torch: CHECK", fg="green")
    except Exception as e:
        click.secho(f"torch: NOT FOUND ({e})", fg="red")
        valid_sys = False 
        
    try:
        import transformers; click.echo("transformers: CHECK", fg="green")
    except Exception as e:
        click.secho(f"transformers: NOT FOUND ({e})", fg="red")
        valid_sys = False
    
    try: 
        import pandas; click.echo("pandas: CHECK", fg="green")
    except Exception as e:
        click.secho(f"pandas: NOT FOUND ({e})", fg="red")
        valid_sys = False
    
    try: 
        import numpy; click.echo("numpy: CHECK", fg="green")
    except Exception as e:
        click.secho(f"numpy: NOT FOUND ({e})", fg="red")
        valid_sys = False
    
    try:
        import vaderSentiment; click.echo("vaderSentiment: CHECK", fg="green")
    except Exception as e:
        click.secho(f"vaderSentiment: NOT FOUND ({e})", fg="red")
        valid_sys = False
        
    try:
        import nltk; click.echo("nltk: CHECK", fg="green")
    except Exception as e:
        click.secho(f"nltk: NOT FOUND ({e})", fg="red")
        valid_sys = False
        
        
    if valid_sys:
        click.secho("System is ready to run Audisect!", fg="green")
    else:
        click.secho("System is NOT ready to run Audisect. Please install the missing components.", fg="red")
        raise typer.Exit(code=1)
    

cli.add_command(run_cmd)

def main(): 
    cli()

if __name__ == "__main__":
    main()