from test import run_transcription #dont forget to change this name lol


###### Program Structure ######

# Transcribe files
# Run VADER and ML analysis
# Add to pandas dataframe
outputFolder = "outputFolder"
audio_directory = "/Users/mattheweggers/repos/audisect/audioFiles" # FIXME Replace with INSERT AUDIO FOLDER HERE


def main():
    run_transcription(audio_directory, outputFolder)
    
    
    
if __name__ == "__main__":
    main()