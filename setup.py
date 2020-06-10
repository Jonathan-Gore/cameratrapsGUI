import PySimpleGUI as sg
import os
import sys
import configparser

#initializes configparser
config = configparser.ConfigParser()

layout = [  [sg.Text('Enter locations')],

            ##changed sg.FolderBrowse to sg.FileBrowse
            [sg.Text('Backend Python Scripts'), sg.Input(key='-DETECTORSCRIPTS-'), sg.FileBrowse() ],

            [sg.Text('Backend Python Scripts'), sg.Input(key='-VISUALSCRIPTS-'), sg.FileBrowse() ],

            ##changed sg.FolderBrowse to sg.FileBrowse
            [sg.Text('CNN Model File'), sg.Input(key='-MODEL-'), sg.FileBrowse() ],

            [sg.Button('Ok'), sg.Button('Cancel')]  ]

#script, model, and image location input UI pop-up
event, values = sg.Window('Window Title', layout, default_element_size=(20,1), text_justification='right', auto_size_text=False).read(close=True)

Detector_loc = values['-DETECTORSCRIPTS-']
Model_loc = values['-MODEL-']
Visual_loc = values['-VISUALSCRIPTS-']

#config file structure
config['default'] = {
    "Batch_Detector_Script_File_Location" : Detector_loc,
    "Visualization_Script_File_Location" : Visual_loc,
    "Model_Location" : Model_loc
}

if event == 'Ok':
    with open('test.ini', 'w') as configfile:
        config.write(configfile)
    sg.popup('Your locations:', values['-DETECTORSCRIPTS-'], values['-VISUALSCRIPTS-'], values['-MODEL-'])
else:
    sg.popup('Cancelled')

    # Need this to end program if 'cancel' button is selected
    sys.exit()