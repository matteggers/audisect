import whisper
from pathlib import Path
# Make a note to user that if on mac, pasting "" into notes auto corrects to em dash. Need a different text editor
# yt-dlp -f bestaudio -x --audio-format wav "URL"

extensions = {".wav",".mp3",".m4a",".mp4"}
# Locates audio files and adds their absolute path to a list - FIXME roughly redundant with does_file_exist. possible future change
def add_files_to_list(directory, extensions):
    filePaths = []
    for (root, dirs, files) in Path(directory).walk():
        for name in files:
            if any(name.endswith(ext) for ext in extensions):
                fullPath = Path(root).joinpath(name)
                filePaths.append(fullPath)
    return filePaths
        
        
# Checks whether a text file exists in the output directory.
def does_file_exist(file, outputDirectory):
    fileName = file_splitter(file)
    fullFilePath = Path(outputDirectory).joinpath(fileName)
    fullFilePath = fullFilePath.with_suffix('.txt')
    print(f"full file path: {fullFilePath}")
    
    return True if Path(fullFilePath).exists() else False
    
def file_splitter(file):
    return Path(file).stem

# takes fileName (w extension) and writes the content of the transcription to it
def write_to_file(outputDirectory, outputFileName, modelResult):
    outputFile = Path(outputDirectory) / outputFileName
    
    with open(outputFile, "w") as f:
        f.write(modelResult["text"])

# Transcribes untranscribed files
def transcribe(allFiles, outputDirectory, model_size):
    
    model = whisper.load_model(model_size) 
     
    for file in allFiles:
        print(f"within transcribe(), outputdirectory: {outputDirectory}")
        fileExists = does_file_exist(file, outputDirectory)
        
        if fileExists is True:
            print(f"{Path(file).name} has already been transcribed")
        else:
            print(f"TRANSCRIBING : {file}")
            result = model.transcribe(file, fp16 = False) # false bc mac -> FIXME need fixing
    
            name = file_splitter(file)

            outputFileName = name + ".txt" # Eventually will want timestamped transcriptions, FIXME
            
            write_to_file(outputDirectory, outputFileName, result)


def run_transcription(audio_directory, outputFolder, model_size):
    outputDirectory = Path(Path.cwd()) / outputFolder
    outputDirectory = outputDirectory.resolve()
    allFiles = add_files_to_list(audio_directory, extensions)
    transcribe(allFiles, outputDirectory, model_size)
