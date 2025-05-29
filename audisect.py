from transcriber import run_transcription, create_output_directory
from sentimentAnalyzer import add_files_to_list, analysis_wrapper
import sentimentAnalyzer
import os
import click

@click.command()
@click.option("--input", prompt="Location of audio files", help="Where your audio files are stored")
#@click.option("--output", prompt="Output folder name", help="Folder where text transcriptions will be stored")
@click.option("--size", default="medium", help="Whisper model size.")


def main(input, size):
    outputFolder = "transcriptions"
    currentDirectory = os.getcwd()
    textDirectory = create_output_directory("data")
    transcriptionDirectory = os.path.join(currentDirectory, outputFolder)
    print(f"textDirectory: {textDirectory}")
    run_transcription(input, outputFolder, size)
    print("transcription ran")
    textFiles = add_files_to_list(transcriptionDirectory, extensions={'.txt'})
    print(f"textFiles added to list: {textFiles}")
    analysis_wrapper(textFiles)
    
 
if __name__ == "__main__":
    main()

# currently only using a standard txt file for output. Add the file that includes seconds - specify seconds so we can track negativity at certain milestones (or use nltk for paragraphs)