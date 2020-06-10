import PySimpleGUI as sg
import os
import sys
from subprocess import Popen
import numpy as np
import csv

import configparser

#initializes configparser
config = configparser.ConfigParser()
config.read('test.ini')

Batch_Detector_Loc = config['default']['batch_detector_script_file_location']
Visual_Output_Loc = config['default']['visualization_script_file_location']
Model_Loc = config['default']['model_location']

#test add for settings window
def settings_window():

    layout = [[sg.Text('The second form is small \nHere to show that opening a window using a window works')],
              [sg.OK()]]

    window = sg.Window('Second Form', layout)
    event, values = window.read()
    window.close()

#added in to see if a menu bar can be easily added without major code rewrites
menu_def = [['&File', ['&Properties', 'E&xit' ]]]

layout = [  [sg.Text('Enter locations')],

            #test add of menu
            [sg.Menu(menu_def, tearoff=False, pad=(20,1))],

            ##changed sg.FolderBrowse to sg.FileBrowse
            #[sg.Text('Backend Python Scripts'), sg.Input(key='-SCRIPTS-'), sg.FileBrowse() ],

            ##changed sg.FolderBrowse to sg.FileBrowse
            #[sg.Text('CNN Model File'), sg.Input(key='-MODEL-'), sg.FileBrowse() ],

            [sg.Text('Image Directory'), sg.Input(key='-TRAP-'), sg.FolderBrowse() ],
            [sg.Button('Ok'), sg.Button('Cancel')]  ]

layout2 = [ [sg.Text('Make sure your computer is charged or charging as the image analysis can take multiple hours!\nThe core image detection engine is provided and developed by Microsofts AI for Earth program.\n\n\nThis process creates a file named out.json, it contains the raw detection data and will be needed later!\n')],
            [sg.Button('Ok'), sg.Button('Cancel')]  ]

layout3 = [ [sg.Text('Begin Visualizing Processing Results (turn fancy numbers [.json] into red squares on camera trap images)')],
            [sg.Text('Backend Python Scripts'), sg.Input(key='-SCRIPTS_visual-'), sg.FileBrowse() ],

            ##changed sg.FolderBrowse to sg.FileBrowse
            [sg.Text('Output JSON file created from previous step, most likely named: output.json, found in the same folder with your images'), sg.Input(key='-JSON_visual-'), sg.FileBrowse() ],

            [sg.Text('Original Image Folder Location'), sg.Input(key='-DETECT_visual-'), sg.FolderBrowse() ],
            [sg.Text('New Image Folder Location to Create'), sg.Input(key='-RENDER_visual-'), sg.FolderBrowse() ],
            [sg.Text('Confidence Threshold for Detection [Scale of 0 - 1]'), sg.Input(key='-CONFIDENCE_visual-') ],
            [sg.Button('Ok'), sg.Button('Cancel')]  ]

#script, model, and image location input UI pop-up
event, values = sg.Window('Window Title', layout, default_element_size=(20,1), text_justification='right', auto_size_text=False).read(close=True)

#sequence = [str(data[0]), str(data[1])]

if event == 'Ok':
    directory = 'C:\\git\\cameratrapsGUI\\bat'
    with open(os.path.join(directory, 'batchprocessdetections.bat'), 'w') as OPATH:
        OPATH.writelines(['call c:\\Users\\Jonathan\\Miniconda3\\Scripts\\activate.bat cameratraps-detector',
                          '\n',
                          'set PYTHONPATH=c:\\git\\cameratraps;c:\\git\\ai4eutils',
                          '\n',
                          'python',
                          ' ',
                          Batch_Detector_Loc,
                          ' ',
                          Model_Loc,
                          ' ',
                          values['-TRAP-'],
                          ' ',
                          values['-TRAP-'],
                          '/out.json',
                          ' ',
                          '--recursive'])
    sg.popup('Your locations:', values['-TRAP-'], Batch_Detector_Loc, Model_Loc)

#test add for properties to open settings window
elif event == 'Properties':
    settings_window()
else:
    sg.popup('Cancelled')

    #Need this to end program if 'cancel' button is selected
    sys.exit()

#if event == 'Ok':
#    directory = 'C:\\git\\cameratrapsGUI\\bat'
#    with open(os.path.join(directory, 'batchprocessdetections.bat'), 'w') as OPATH:
#        OPATH.writelines(['call c:\\Users\\Jonathan\\Miniconda3\\Scripts\\activate.bat cameratraps-detector',
#                          '\n',
#                          'set PYTHONPATH=c:\\git\\cameratraps;c:\\git\\ai4eutils',
#                          '\n',
#                          'python',
#                          ' ',
#                          data[0],
#                          ' ',
#                          data[1],
#                          ' ',
#                          values['-TRAP-'],
#                          ' ',
#                          values['-TRAP-'],
#                          '/out.json',
#                          ' ',
#                          '--recursive'])
#    sg.popup('Your locations:', values['-TRAP-'], values['-MODEL-'], values['-SCRIPTS-'])
#else:
#    sg.popup('Cancelled')

    # Need this to end program if 'cancel' button is selected
#    sys.exit()

#Batch processing UI pop-up
event, process = sg.Window('Window Title', layout2).read(close=True)

if event == 'Ok':
    p = Popen("batchprocessdetections.bat", cwd=r"C:\\git\\cameratrapsGUI\\bat")
    stdout, stderr = p.communicate()
else:
    sg.popup('Cancelled')
    # Need this to end program if 'cancel' button is selected
    sys.exit()

#Visualization UI Pop-up
event, visualization = sg.Window('Window Title', layout3).read(close=True)

#creating a .bat file that will call the visualization (check) script from the local cameratraps git folder with user inputed values
if event == 'Ok':
    directory = 'C:\\git\\cameratrapsGUI\\bat'
    with open(os.path.join(directory, 'visualization.bat'), 'w') as OPATH:
        OPATH.writelines(['call c:\\Users\\Jonathan\\Miniconda3\\Scripts\\activate.bat cameratraps',
                          '\n',
                          'set PYTHONPATH=c:\\git\\cameratraps;c:\\git\\ai4eutils',
                          '\n',
                          'python',
                          ' ',
                          visualization['-SCRIPTS_visual-'],
                          ' ',
                          visualization['-JSON_visual-'],
                          ' ',
                          visualization['-RENDER_visual-'],
                          ' ',
                          '--confidence',
                          ' ',
                          visualization['-CONFIDENCE_visual-'],
                          ' ',
                          '--images_dir',
                          ' ',
                          visualization['-DETECT_visual-']])
    #sg.popup('Your locations:', visualization['-TRAP-'], values['-MODEL-'], values['-SCRIPTS-'])
else:
    sg.popup('Cancelled')

    # Need this to end program if 'cancel' button is selected
    sys.exit()
