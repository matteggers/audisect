from test import run_transcription, create_output_directory
from sentimentAnalyzer import find_files
from sentimentAnalyzer import analysis_wrapper
import sentimentAnalyzer
import os

import click

@click.command()
@click.option("--input", prompt="Location of audio files", help="Where your audio files are stored")
#@click.option("--output", prompt="Output folder name", help="Folder where text transcriptions will be stored")
@click.option("--size", default="medium", help="Whisper model size.")


def main(input, output, size):
    run_transcription(input, "transcriptions", size)
    textDirectory = create_output_directory(output)
    textFiles = find_files(textDirectory, extensions={'.txt'})
    analysis_wrapper(textFiles)
    
    

    
    
    
    
    
if __name__ == "__main__":
    main()

# currently only using a standard txt file for output. Add the file that includes seconds - specify seconds so we can track negativity at certain milestones (or use nltk for paragraphs)