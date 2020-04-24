import PySimpleGUI as sg
import os
import sys
from subprocess import Popen
import numpy as np

layout3 = [ [sg.Text('Begin Visualizing Processing Results (turn fancy numbers [.json] into red squares on camera trap images)')],
            [sg.Text('Backend Python Scripts'), sg.Input(key='-SCRIPTS_visual-'), sg.FileBrowse() ],
            [sg.Text('Output JSON file created from previous step, most likely named: output.json, found in the same folder with your images'), sg.Input(key='-JSON_visual-'), sg.FileBrowse() ], ##changed sg.FolderBrowse to sg.FileBrowse
            [sg.Text('Original Image Folder Location'), sg.Input(key='-DETECT_visual-'), sg.FolderBrowse() ],
            [sg.Text('New Image Folder Location to Create'), sg.Input(key='-RENDER_visual-'), sg.FolderBrowse() ],
            [sg.Text('Confidence Threshold for Detection [Scale of 0 - 1]'), sg.Input(key='-CONFIDENCE_visual-') ],
            [sg.Button('Ok'), sg.Button('Cancel')]  ]

event, visualization = sg.Window('Window Title', layout3).read(close=True)

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
    sys.exit() #Need this to end program if 'cancel' button is selected
