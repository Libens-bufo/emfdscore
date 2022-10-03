
#For the interface
import tkinter as tk
from tkinter import filedialog

#These are the typical data science libraries needed for eMFDScore
import pandas as pd 
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from emfdscore.scoring import score_docs 


########################
# Functions
########################

# Pandas reads in the csv selected or the default
def readInput():
    input = pd.read_csv(inPath.get() or 'emfdscore/template_input.csv', header=None)
    return input
    
# Function for the score button that passes options to the eMFDScore script
def score_args():
    template_input = readInput()
    num_docs = len(template_input)

    setOutputFilenameVar(filename)

    scoreOptionsVar_ = ''
    if (scoreOptionsVar.get() == 'gdelt.ngrams'):
        scoreOptionsVar_ = 'gdelt'
    else:
        scoreOptionsVar_ = scoreOptionsVar.get()

    DICT_TYPE = dictTypeVar.get() or 'emfd'
    PROB_MAP = probMapVar.get() or 'all'
    SCORE_METHOD = scoreOptionsVar.get() or 'bow'
    OUT_METRICS = sentimentOptionsVar.get() or 'sentiment'
    OUT_CSV_PATH = outputFileNameVar.get() or 'default-file-output.csv'
    
    df = score_docs(template_input,DICT_TYPE,PROB_MAP,SCORE_METHOD,OUT_METRICS,num_docs)
    df.to_csv(OUT_CSV_PATH, index=False)

# Browse for a file to score
def browseFiles():
    global filename
    filename = tk.filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a CSV File to score",
                                          filetypes = (("CSV files",
                                                        "*.csv"),
                                                       ("all files",
                                                        "*.*")))
    inPath.set(filename)

    trimmedFilename = trimFilename(filename)
    setStatusBar(trimmedFilename)

# Updates status bar with selected file name
def setStatusBar(trimmedFilename):
    statusBar = tk.Label(statusFrame, text = "File:" + (trimmedFilename or ' No file selected'), relief='sunken', anchor='w') #Status bar
    statusBar.grid(column=0,row=4,columnspan=3, sticky='we')

# Trims down filename so it will fit in the status bar
def trimFilename(filename):
    limit = 40
    array = list(filename)
    trimmedFilename = ''

    if len(filename) < limit:
        return filename
    
    for i in range(len(array) - 1, 0, -1):
        if len(trimmedFilename) < limit:
            trimmedFilename = array[i] +trimmedFilename 

    return " ..." + trimmedFilename
        

# Sets the proper output filename
def setOutputFilenameVar(filename):
    filenameSplitList = filename.split('/') # Last index of this is our filename (e.g. filename.csv)

    outputFileNameVar.set(filenameSplitList[-1].split('.')[0] # 0-index of of filename split at '.' is simply the filename.
                          + '-' + dictTypeVar.get()           # Then the current options are concatenated to it.
                          + '-' + probMapVar.get() 
                          + '-' + scoreOptionsVar.get()
                          + '-' +  sentimentOptionsVar.get() 
                          + '.csv')

########################
# GUI
########################
    
# Create main window
root = tk.Tk()
root.title("eMFD Score")
root.iconbitmap('icons/osprey.ico')
root.geometry("335x210")


#######################
# Dict Type
#######################

dictTypeVar = tk.StringVar()
dictTypeOptions = [
  ('extended Moral Foundations Dictionary (eMFD)', 'emfd'),
  ('Moral Foundations Dictionary 2.0','mfd2'),
  ('original Moral Foundations Dictionary', 'mfd')
]

# Dictionary Type Frame
dictTypeFrame = tk.LabelFrame(root, text="Dictionary Type")
dictTypeFrame.grid(column=0, row = 0, padx=10)


# Dictionary type radio buttons
for size in dictTypeOptions:
    
  r = tk.Radiobutton(
      dictTypeFrame,
      text=size[0],
      value=size[1],
      variable=dictTypeVar
  )
  
  r.grid(sticky='w')
# Set default
dictTypeVar.set('emfd')

#######################
# Probability Map
#######################

probMapVar = tk.StringVar()
probMapOptions = ['all','single']

#O ptions Frame (Hold three options: Probmap, Scoring method, sentiment)
probMapFrame = tk.LabelFrame(root, text="Options")
probMapFrame.grid(column = 0, row = 1)


# Probability map radio buttons
probMapDrop = tk.OptionMenu(probMapFrame, probMapVar, *probMapOptions)
probMapDrop.grid(column=0, row=0, sticky='w',padx=13,pady=1)

# Set Default
probMapVar.set('all')

########################
# Scoring Method
########################

# Scoring Options and Variable
scoreOptions = ['bow', 'pat', 'wordlist', 'gdelt.ngrams']
scoreOptionsVar = tk.StringVar()

# Creates menu
scoreOptionsDrop = tk.OptionMenu(probMapFrame, scoreOptionsVar, *scoreOptions )
scoreOptionsDrop.grid(column=1,row=0, padx=13,pady=1)
scoreOptionsVar.set('bow')

########################
# Sentiment
########################
sentimentOptions= ['sentiment', 'vice-virtue']
sentimentOptionsVar = tk.StringVar()

sentimentOptionsDrop = tk.OptionMenu(probMapFrame, sentimentOptionsVar, *sentimentOptions )
sentimentOptionsVar.set('sentiment')
sentimentOptionsDrop.grid(column=2, row=0, padx=12,pady=1)

#######################
# Select Input CSV File
#######################

# Frame for file select
fileFrame = tk.LabelFrame(root)
fileFrame.grid(column=0, pady=5)

# Variable holding filename that will be passed to the eMFD Score script
outputFileNameVar = tk.StringVar()

browsebutton = tk.Button(fileFrame, text = 'Browse', command = browseFiles)
browsebutton.grid(sticky='w',column=0,row=0)

inPath = tk.StringVar()

########################
# Choose output directory and set output filename
########################

# Feature removed

########################
# Status Bar
########################

# Frame where the label lives
statusFrame = tk.Frame(root) 

# Without these lines, the label would not stretch across (sticky) the window
statusFrame.grid_rowconfigure(0, weight=1)
statusFrame.grid_columnconfigure(0, weight=1)

# Create status bar (label)
statusBarText = 'No File Selected'
statusBar = tk.Label(statusFrame, text = 'No file selected', relief='sunken', anchor='w') 

# Position status bar
statusBar.grid(column=0,row=4,columnspan=3, sticky='we')
statusFrame.grid(column=0, columnspan=3, sticky='we')


####################
#Score Button
####################

scoreButton = tk.Button(fileFrame, text='Score', command=lambda:score_args())
scoreButton.grid(column =1, row=0, pady=3)

# Begin event loop
tk.mainloop()

