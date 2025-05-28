from test import run_transcription #dont forget to change this name lol


###### Program Structure ######

# Transcribe files
# Run VADER and ML analysis
# Add to pandas dataframe
outputFolder = "outputFolder"
audio_directory = "" # FIXME Replace with changeable path in some CLI


def main():
    run_transcription(audio_directory, outputFolder)
    
    
    
    
if __name__ == "__main__":
    main()


# Considerations
# Put everything in one dataframe? - Yeah, DS will split it on their own 
# One dataframe per text file. Give the option to run it with one


#TODO
#Save data to a Dataframe
# Run the analysis for many videos
# use plotly to plot the negativity of each video
# Go one step further and plot the negativity per minute (need another output in the transcription function)