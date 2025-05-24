# Initial test
# Use whisper to analyze a file located within a set folder
# Then wait for the transcript and run it through another model for tonality and rhythm.
# output these to a csv, with first column being tonality, second being rhythm for each sentence, and third being
# the indicating keyword, and the fourth being the actual sentence.
# need a list of keywords for each emotion and run through another model/recognition script

import os
import whisper


# Code Snippet:
# Locate folder that has audio files
# Enter folder that has audio files
# Create folders for the output
# Open them into whisper
# Transcribe them into whisper
# Place the output into a subfolder within the output folder titled for each video
# Why nested like this? Keeps files segmented for individual analysis if desired.

# Make a note to user that if on mac, pasting "" into notes auto corrects to em dash. Need a different text editor
# yt-dlp -f bestaudio -x --audio-format wav "https://www.youtube.com/watch?v=EdgjJNAphUo"


# had to fix macOs ssl certificate trust bc python 13.3 /Applications/Python\ 3.13/Install\ Certificates.command

model = whisper.load_model("tiny") # add user changeable CLI


# OUTPUT FOLDER
outputFolder = "outputFolder"

# TODO Make this a function with more robust error handling
try:
    os.mkdir(outputFolder)
    print(f"Folder '{outputFolder} created successfully")
except FileExistsError:
    print(f"Folder '{outputFolder} already exists")
except OSError as e:
    print(f"Error creating folder: {e}")

outputDirectory = os.path.join(os.getcwd(), outputFolder)
outputDirectory = os.path.abspath(outputDirectory)


audio_directory = ""

def find_audio_files(directory, extensions={".wav",".mp3",".m4a",".mp4"}):
    filePaths = []
    for (root, dirs, files) in os.walk(directory, topdown=True):
        for name in files:
            if any(name.endswith(ext) for ext in extensions):
                fullPath = os.path.join(root, name)
                filePaths.append(fullPath)
    return filePaths
        
    
allFiles = find_audio_files(audio_directory)


for file in allFiles:
    print(f"TRANSCRIBING : {file}")
    result = model.transcribe(file, fp16 = False) # false bc mac
    
    head, tail = os.path.split(file)
    tail = tail.split(".")
    tailBase = tail[0]

    outputFileName = tailBase + ".txt"
    outputFile = os.path.join(head, outputFileName)
    
    with open(outputFile, "w") as f:
        f.write(result["text"])

