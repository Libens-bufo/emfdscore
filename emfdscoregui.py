
#For the interface
import tkinter as tk
from tkinter import W, filedialog

#These are the typical data science libraries needed for eMFDScore
import pandas as pd 
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from emfdscore.scoring import score_docs 


########################
# Functions
########################

#Pandas reads in the csv selected or the default
def readInput():
    input = pd.read_csv(inPath.get() or 'emfdscore/template_input.csv', header=None)
    return input
    
def score_args():
    template_input1 = readInput()
    num_docs = len(template_input1)

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
    
    df = score_docs(template_input1,DICT_TYPE,PROB_MAP,SCORE_METHOD,OUT_METRICS,num_docs)
    df.to_csv(OUT_CSV_PATH, index=False)


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

    statusBar = tk.Label(statusFrame, text = "Path:" + (trimmedFilename or 'No file selected'), relief='sunken', anchor=W) #Status bar
    statusBar.grid(column=0,row=4)

def trimFilename(filename):
    
    limit = 25
    array = list(filename)
    trimmedFilename = ''

    if len(filename) < limit:
        return filename
    
    for i in range(len(array) - 1, 0, -1):
        if len(trimmedFilename) < limit:
            trimmedFilename = array[i] +trimmedFilename 

    return "..." + trimmedFilename
        


    

def setOutputFilenameVar(filename):
    filenameSplitList = filename.split('/')
    outputFileNameVar.set(filenameSplitList[-1].split('.')[0] 
                          + '-' + dictTypeVar.get() 
                          + '-' + probMapVar.get() 
                          + '-' + scoreOptionsVar.get()
                          + '-' +  sentimentOptionsVar.get() 
                          + '.csv')

########################
# GUI
########################
    
#Create main window
root = tk.Tk()
root.title("eMFD Score")
root.iconbitmap('osprey.ico')
root.geometry("335x235")

#root.columnconfigure(index = 3, weight = 4)
#######################
#Dict Type
#######################

dictTypeVar = tk.StringVar()
dictTypeOptions = [
  ('extended Moral Foundations Dictionary (eMFD)', 'emfd'),
  ('Moral Foundations Dicitonary 2.0','mfd2'),
  ('original Moral Foundations Dictionary', 'mfd')
]

#Dictionary Type Frame
dictTypeFrame = tk.LabelFrame(root, text="Dictionary Type")
#dictTypeFrame.pack(fill="both")
dictTypeFrame.grid(column=0, row = 0, padx=10)


#Dictionary type radio buttons
for size in dictTypeOptions:
    
  r = tk.Radiobutton(
      dictTypeFrame,
      text=size[0],
      value=size[1],
      variable=dictTypeVar
  )
  #r.pack(fill='x', padx=5, pady=5)
  r.grid(sticky='w')
#Set default
dictTypeVar.set('emfd')

#######################
#Probability Map
#######################

probMapVar = tk.StringVar()
probMapOptions = ['all','single']

#Options Frame (Hold three options: Probmap, Scoring method, sentiment)
probMapFrame = tk.LabelFrame(root, text="Options")
probMapFrame.grid(column = 0, row = 1)


#Probability map radio buttons
probMapDrop = tk.OptionMenu(probMapFrame, probMapVar, *probMapOptions)
probMapDrop.grid(column=0, row=0, sticky='w',padx=13,pady=1)

#Set Default
probMapVar.set('all')

########################
# Scoring Method
########################

#Scoring Options and Variable
scoreOptions = ['bow', 'pat', 'wordlist', 'gdelt.ngrams']
scoreOptionsVar = tk.StringVar()

#Creates menu
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
#Select Input CSV File
#######################

#Frame for file select
fileFrame = tk.LabelFrame(root)
fileFrame.grid(column=0)

#Variable holding filename that will be passed to the eMFD Score script
outputFileNameVar = tk.StringVar()

browsebutton = tk.Button(fileFrame, text = 'Browse for input file ', command = browseFiles)
browsebutton.grid(sticky='w',column=0,row=0)

inPath = tk.StringVar()
entry1 = tk.Entry(fileFrame, textvariable = inPath)
entry1.grid(column=1,row=0)

########################
#Choose output directory and set output filename
########################

#Feature removed

########################
# Status Bar
########################

statusFrame = tk.LabelFrame(root).grid(column=0) #Frame where the label lives

filePath = tk.StringVar()
filePath.set(inPath.get() or " ")

statusBar = tk.Label(statusFrame, text = "Path:" + 'No file selected', relief='sunken', anchor=W) #Status bar

statusBar.grid(column=0,row=4)


####################
#Score Button
####################

scoreButton = tk.Button(root, text='Score', command=lambda:score_args())
scoreButton.grid(column =0, row=3, pady=3)

#Begin event loop
tk.mainloop()

