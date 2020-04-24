import PySimpleGUI as sg
import os
import sys
from subprocess import Popen
import numpy as np

layout = [  [sg.Text('Enter locations')],
            [sg.Text('Backend Python Scripts'), sg.Input(key='-SCRIPTS-'), sg.FileBrowse() ], ##changed sg.FolderBrowse to sg.FileBrowse
            [sg.Text('CNN Model File'), sg.Input(key='-MODEL-'), sg.FileBrowse() ], ##changed sg.FolderBrowse to sg.FileBrowse
            [sg.Text('Image Directory'), sg.Input(key='-TRAP-'), sg.FolderBrowse() ],
            [sg.Button('Ok'), sg.Button('Cancel')]  ]

layout2 = [ [sg.Text('Make sure your computer is charged or charging as the image analysis can take multiple hours!\nThe core image detection engine is provided and developed by Microsofts AI for Earth program.\n\n\nThis process creates a file named out.json, it contains the raw detection data and will be needed later!\n')],
            [sg.Button('Ok'), sg.Button('Cancel')]  ]

layout3 = [ [sg.Text('Begin Visualizing Processing Results (turn fancy numbers [.json] into red squares on camera trap images)')],
            [sg.Text('Backend Python Scripts'), sg.Input(key='-SCRIPTS_visual-'), sg.FileBrowse() ],
            [sg.Text('Output JSON file created from previous step, most likely named: output.json, found in the same folder with your images'), sg.Input(key='-JSON_visual-'), sg.FileBrowse() ], ##changed sg.FolderBrowse to sg.FileBrowse
            [sg.Text('Original Image Folder Location'), sg.Input(key='-DETECT_visual-'), sg.FolderBrowse() ],
            [sg.Text('New Image Folder Location to Create'), sg.Input(key='-RENDER_visual-'), sg.FolderBrowse() ],
            [sg.Text('Confidence Threshold for Detection [Scale of 0 - 1]'), sg.Input(key='-CONFIDENCE_visual-') ],
            [sg.Button('Ok'), sg.Button('Cancel')]  ]

#script, model, and image location input UI pop-up
event, values = sg.Window('Window Title', layout, default_element_size=(20,1), text_justification='right', auto_size_text=False).read(close=True)

if event == 'Ok':
    directory = 'C:\\git\\cameratrapsGUI\\bat'
    with open(os.path.join(directory, 'batchprocessdetections.bat'), 'w') as OPATH:
        OPATH.writelines(['call c:\\Users\\Jonathan\\Miniconda3\\Scripts\\activate.bat cameratraps-detector',
                          '\n',
                          'set PYTHONPATH=c:\\git\\cameratraps;c:\\git\\ai4eutils',
                          '\n',
                          'python',
                          ' ',
                          values['-SCRIPTS-'],
                          ' ',
                          values['-MODEL-'],
                          ' ',
                          values['-TRAP-'],
                          ' ',
                          values['-TRAP-'],
                          '/out.json',
                          ' ',
                          '--recursive'])
    sg.popup('Your locations:', values['-TRAP-'], values['-MODEL-'], values['-SCRIPTS-'])
else:
    sg.popup('Cancelled')
    sys.exit() #Need this to end program if 'cancel' button is selected

#Batch processing UI pop-up
event, process = sg.Window('Window Title', layout2).read(close=True)

if event == 'Ok':
    p = Popen("batchprocessdetections.bat", cwd=r"C:\\git\\cameratrapsGUI\\bat")
    stdout, stderr = p.communicate()
else:
    sg.popup('Cancelled')
    sys.exit() #Need this to end program if 'cancel' button is selected

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
    sys.exit() #Need this to end program if 'cancel' button is selected
