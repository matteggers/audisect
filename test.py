# Initial test
# Use whisper to analyze a file located within a set folder
# Then wait for the transcript and run it through another model for tonality and rhythm.
# output these to a csv, with first column being tonality, second being rhythm for each sentence, and third being
# the indicating keyword, and the fourth being the actual sentence.
# need a list of keywords for each emotion and run through another model/recognition script


import os
import whisper
from glob import glob # may refactor w this, idk yet.
# Make a note to user that if on mac, pasting "" into notes auto corrects to em dash. Need a different text editor
# yt-dlp -f bestaudio -x --audio-format wav "URL"


# had to fix macOS ssl certificate trust bc python 13.3 /Applications/Python\ 3.13/Install\ Certificates.command

model = whisper.load_model("tiny") # add user changeable CLI

def create_output_directory(outputFolder): 
    try:
        os.mkdir(outputFolder)
        print(f"Folder '{outputFolder} created successfully")
    except FileExistsError:
        print(f"Folder '{outputFolder} already exists")
    except OSError as e:
        print(f"Error creating folder: {e}")
    
    return os.path.dirname(outputFolder)


# Locates audio files and adds their absolute path to a list
def find_audio_files(directory, extensions={".wav",".mp3",".m4a",".mp4"}):
    filePaths = []
    for (root, dirs, files) in os.walk(directory, topdown=True):
        for name in files:
            if any(name.endswith(ext) for ext in extensions):
                fullPath = os.path.join(root, name)
                filePaths.append(fullPath)
    return filePaths
        
        
# Checks whether a text file exists in the output directory.
def does_file_exist(file, outputDirectory):
    fullFilePath = os.path.join(outputDirectory, file)
    if os.path.exists(fullFilePath):
        return True
    else:
        return False
    

# Transcribes untranscribed files
def transcribe(allFiles, outputDirectory): # Nothing returned  
    for file in allFiles:
        fileExists = does_file_exist(file, outputDirectory)
        
        if fileExists is True:
            print(f"{os.path.basename(file)} has already been transcribed")
        else:
            print(f"TRANSCRIBING : {file}")
            result = model.transcribe(file, fp16 = False) # false bc mac
    
            head, tail = os.path.split(file)
            tail = tail.split(".")
            tailBase = tail[0]

            outputFileName = tailBase + ".txt"
            outputFile = os.path.join(outputDirectory, outputFileName)
            with open(outputFile, "w") as f:
                f.write(result["text"])


outputFolder = "outputFolder"
audio_directory = "INSERT FOLDER PATH HERE"
allFiles = find_audio_files(audio_directory)
outputDirectory = os.path.join(os.getcwd(), outputFolder)
outputDirectory = os.path.abspath(outputDirectory)

create_output_directory(outputFolder)
allFiles = find_audio_files(audio_directory)
transcribe(allFiles, outputDirectory)
