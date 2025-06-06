# Initial test
# Use whisper to analyze a file located within a set folder
# Then wait for the transcript and run it through another model for tonality and rhythm.
# output these to a csv, with first column being tonality, second being rhythm for each sentence, and third being
# the indicating keyword, and the fourth being the actual sentence.
# need a list of keywords for each emotion and run through another model/recognition script


import os
import whisper
# Make a note to user that if on mac, pasting "" into notes auto corrects to em dash. Need a different text editor
# yt-dlp -f bestaudio -x --audio-format wav "URL"

# FIXME, can use exit_ok=true in try section, remove fileexists error
def create_output_directory(outputFolder): 
    try:
        os.mkdir(outputFolder)
        print(f"Folder '{outputFolder}' created successfully")
    except FileExistsError:
        print(f"Folder '{outputFolder}' already exists")
    except OSError as e:
        print(f"Error creating folder: {e}")
    
    return os.path.abspath(outputFolder)


extensions = {".wav",".mp3",".m4a",".mp4"}
# Locates audio files and adds their absolute path to a list - FIXME roughly redundant with does_file_exist. possible future change
def add_files_to_list(directory, extensions):
    filePaths = []
    for (root, dirs, files) in os.walk(directory, topdown=True):
        for name in files:
            if any(name.endswith(ext) for ext in extensions):
                fullPath = os.path.join(root, name)
                filePaths.append(fullPath)
    return filePaths
        
        
# Checks whether a text file exists in the output directory.
def does_file_exist(file, outputDirectory):
    fileName = file_splitter(file)
    fullFilePath = os.path.join(outputDirectory, fileName)
    fullFilePath = fullFilePath + '.txt'
    print(f"full file path: {fullFilePath}")

    # FIXME IT NEEDS TO CHECK IF IT IS A TXT FILE
    #SPLIT FILE, check in output directory
  
    if os.path.exists(fullFilePath):
        return True
    else:
        return False
    
def file_splitter(file):
    _, tail = os.path.split(file)
    tail = tail.split('.')
    tailBase = tail[0]
    return tailBase

# takes fileName (w extension) and writes the content of the transcription to it
def write_to_file(outputDirectory, outputFileName, modelResult):
    outputFile = os.path.join(outputDirectory, outputFileName)
    
    with open(outputFile, "w") as f:
        f.write(modelResult["text"])

# Transcribes untranscribed files
def transcribe(allFiles, outputDirectory, model_size): # Nothing returned 
    
    model = whisper.load_model(model_size) # add user changeable CLI
     
    for file in allFiles:
        print(f"within transcribe(), outputdirectory: {outputDirectory}")
        fileExists = does_file_exist(file, outputDirectory)
        
        if fileExists is True:
            print(f"{os.path.basename(file)} has already been transcribed")
        else:
            print(f"TRANSCRIBING : {file}")
            result = model.transcribe(file, fp16 = False) # false bc mac
    
            name = file_splitter(file)

            outputFileName = name + ".txt" # Eventually will want timestamped transcriptions, FIXME
            
            write_to_file(outputDirectory, outputFileName, result)


def run_transcription(audio_directory, outputFolder, model_size):
    outputDirectory = os.path.join(os.getcwd(), outputFolder)
    outputDirectory = os.path.abspath(outputDirectory)
    create_output_directory(outputFolder)
    allFiles = add_files_to_list(audio_directory, extensions)
    transcribe(allFiles, outputDirectory, model_size)
