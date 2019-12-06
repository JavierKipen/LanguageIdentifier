import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import shutil

import glob, os


def getListOfWavs(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfWavs(fullPath)
        elif fullPath.endswith('.wav'):
            allFiles.append(fullPath)
    return allFiles
src="C:/Users/Javier/PycharmProjects/TP2Voz/Datasets/en/Trunk/Audio/Main/16kHz_16bit"
destDir="C:/Users/Javier/PycharmProjects/TP2Voz/Datasets/en/wav"
listOfFile = getListOfWavs(src)
for i in range(np.size(listOfFile)):
    oldName = shutil.copy(listOfFile[i], destDir)
    newName=os.path.join(destDir, str(i) + ".wav")
    os.rename(oldName, newName)