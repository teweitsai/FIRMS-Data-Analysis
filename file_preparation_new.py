# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 08:20:52 2015

@author: Wolf
"""
from Tkinter import *

import pandas as pd
import numpy as np

import tkFileDialog, os

def load_csv():
    
    global file_name    

    returned_values['filename'] = tkFileDialog.askopenfilename()
    filepath = returned_values.get('filename')
    
    info_csv = pd.read_csv(filepath)
    info_csv = pd.DataFrame.as_matrix(info_csv)

    # Generate the file name
    num_file, num_index = info_csv.shape
    file_name = []
    for ii in range(0,num_file):
    
        temp = 'lock'
        for jj in range(0,num_index):
            temp = temp + '_' + str(info_csv[ii][jj].astype('int64'))

        file_name.append(temp)       

def load_data():
    
    global data_x, data_y, dirname
    
    returned_values['filename'] = tkFileDialog.askopenfilename()
    filepath = returned_values.get('filename')
    dirname = os.path.dirname(filepath)
    
    # Get the position and signal
    data_signal = np.fromfile(filepath, sep = " ")
    n = data_signal.size   # Check the length of data
    data_base = data_signal.reshape((n/2,2))   # Reshape the data to a matrix 
    data_positon_base = np.array(data_base[:,0]) # Position
    data_base = np.array(data_base[:,1])         # Signal
    
    # Remove the data of zero position
    itemindex = np.where(data_positon_base!=0)
    data_x = data_positon_base[itemindex]
    data_y = data_base[itemindex]
    
    
def generate_file(dirname, file_name, data_x, data_y):
        
    temp = np.array(np.diff(data_x)<0, dtype = int) # The "int" type is helpful
                                                    # for the consistency.
    # Enforce the consistency
    temp0 = np.concatenate((np.array([0]), temp[0:temp.size-1]), axis=0)
    temp = (temp+temp0)/2
    
    # Get the local max and min
    temp1 = np.diff(temp) 
    
    temp_max = np.where(temp1 == 1)[0] + 1  # local max, "+1" is for the 
                                            # compensation from the 'diff' function.
    temp_min = np.where(temp1 == -1)[0]     # local min 
    
    # Remove the similar value (space = 20)
    transitions = np.sort(np.append(temp_min,temp_max)) 
    transitions = unique_extreme(transitions,20)    
    
    for ii in range(0,len(file_name)):

        temp_lock_x = data_x[transitions[1+2*ii]:transitions[2+2*ii]]
        temp_lock_y = data_y[transitions[1+2*ii]:transitions[2+2*ii]]
    
        data_xy = np.array([temp_lock_x, temp_lock_y])
        np.savetxt(dirname + '/' + file_name[ii], data_xy.T)  
        
def unique_extreme(x,n):   
    temp = []
    for ii in range(1,x.size): 
        if (x[ii]-x[ii-1])>n:
            temp = np.append(temp,x[ii-1])
    temp = np.append(temp,x[x.size-1])
    temp = temp.astype('int64')
    return temp    

# Parameters
returned_values = {}   # This is to get the path of file
data_x = None
data_y = None
file_name = {}
dirname = {}

# Begin the GUI interface
root = Tk()
root.title('File Preparation')

# Button to function
# Load the csv file to give the file names for each measurement 
button_load_csv = Button(text = 'Load csv file', command = load_csv)
button_load_csv.pack()

# Load the data of measurement
button_load_data = Button(text = 'Load data file', command = load_data)
button_load_data.pack()

# Generate individual measurement file
button_generate_file = Button(text = 'Generate individual files', 
                              command = lambda: generate_file(dirname, file_name, 
                                                              data_x, data_y))
button_generate_file.pack()

# Quit the GUI
button_quit = Button(text = 'Quit', command = root.destroy)
button_quit.pack()

# Execute the GUI
root.mainloop()



