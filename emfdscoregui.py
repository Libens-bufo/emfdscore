import tkinter as tk
from tkinter import filedialog

import pandas as pd 
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from emfdscore.scoring import score_docs 

#template_input = pd.read_csv('emfdscore/template_input.csv', header=None)
#template_input.head()


def readInput():
    input = pd.read_csv(inPath.get() or 'emfdscore/template_input.csv', header=None)
    return input
    
# def score_output():
#     num_docs = len(template_input)
#     DICT_TYPE = 'emfd'
#     PROB_MAP = 'all'
#     SCORE_METHOD = 'bow'
#     OUT_METRICS = 'sentiment'
#     OUT_CSV_PATH = 'test-1.csv'

#     df = score_docs(template_input,DICT_TYPE,PROB_MAP,SCORE_METHOD,OUT_METRICS,num_docs)
#     df.to_csv(OUT_CSV_PATH, index=False)
    
def score_args():
    #setOutputFileName()
    template_input1 = readInput()
    num_docs = len(template_input1)

    DICT_TYPE = dictTypeVar.get() or 'emfd'
    PROB_MAP = probMapVar.get() or 'all'
    SCORE_METHOD = scoreOptionsVar.get() or 'bow'
    OUT_METRICS = sentimentOptionsVar.get() or 'sentiment'
    OUT_CSV_PATH = outputFileNameVar.get() or 'default-file-output.csv'
    scoreOptionsVar_ = ''
    if (scoreOptionsVar.get() == 'gdelt.ngrams'):
        scoreOptionsVar_ = 'gdelt'
    else:
        scoreOptionsVar_ = scoreOptionsVar.get()
        
    filenameSplitList = filename.split('/')
    inputFileNameVar.set(filenameSplitList[-1])
    outputFileNameVar.set(filenameSplitList[-1].split('.')[0] 
                          + '-' + dictTypeVar.get() 
                          + '-' + probMapVar.get() 
                          + '-' + scoreOptionsVar.get()
                          + '-' +  sentimentOptionsVar.get() 
                          + '.csv')

    df = score_docs(template_input1,DICT_TYPE,PROB_MAP,SCORE_METHOD,OUT_METRICS,num_docs)
    df.to_csv(OUT_CSV_PATH, index=False)



#remove
import pathlib
 
# current working directory
#print(pathlib.Path().absolute())


##TODO:
###
###File i/o
######Select output dir
###Generate CL arg
###Status Bar with paths
###Make files not have to be in root

#Defaults
# dictType = 'emfd'
# PROB_MAP = 'all'
# SCORE_METHOD = 'bow'
# OUT_METRICS = 'sentiment'
# OUT_CSV_PATH = 'all-sent.csv'

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

#######Frame for file select
fileFrame = tk.LabelFrame(root)
fileFrame.grid(column=0)

#Variable holding filename that will be passed to the eMFD Score script
inputFileNameVar = tk.StringVar()
outputFileNameVar = tk.StringVar()

def browseFiles():
    global filename
    filename = tk.filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a CSV File to score",
                                          filetypes = (("CSV files",
                                                        "*.csv"),
                                                       ("all files",
                                                        "*.*")))
    filenameSplitList = filename.split('/')
    inputFileNameVar.set(filenameSplitList[-1])
    outputFileNameVar.set(filenameSplitList[-1].split('.')[0] 
                          + '-' + dictTypeVar.get() 
                          + '-' + probMapVar.get() 
                          + '-' + scoreOptionsVar.get()
                          + '-' +  sentimentOptionsVar.get() 
                          + '.csv')
    inPath.set(filename)

    

browsebutton = tk.Button(fileFrame, text = 'Browse for input file ', command = browseFiles)
browsebutton.grid(sticky='w',column=0,row=0)

inPath = tk.StringVar()
entry1 = tk.Entry(fileFrame, textvariable = inPath)
entry1.grid(column=1,row=0)
########################
#Choose output directory and set output filename
########################


###############  
#Current Options
################
# currentOptionsFrame = tk.LabelFrame(root, text="Current options")
# currentOptionsFrame.grid()
# def updateFunc():
    
#     label1= tk.Label(
#     currentOptionsFrame,
#     text=outputFileNameVar.get()+ filename)
#     label1.grid(row=1)
  
#     return  

# updateButton= tk.Button(currentOptionsFrame, text="updateFunc()", command=lambda: updateFunc())
# updateButton.grid(row=0)
####################
#Score Button
####################

scoreButton = tk.Button(root, text='Score', command=lambda:score_args())
scoreButton.grid(pady=3)

#Begin event loop
tk.mainloop()

