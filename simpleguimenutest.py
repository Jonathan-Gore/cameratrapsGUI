import PySimpleGUI as sg
import os
import sys
from subprocess import Popen
import configparser

#initializes configparser
config = configparser.ConfigParser()

#needs these two modifications to the file path to remove "test.ini" from the os path for command prompt can access it.
path = '/'.join((os.path.abspath(__file__).replace('\\', '/')).split('/')[:-1])
config.read(os.path.join(path, 'test.ini'))

config.read('test.ini')

Batch_Detector_Loc = config['default']['batch_detector_script_file_location']
Visual_Output_Loc = config['default']['visualization_script_file_location']
Model_Loc = config['default']['model_location']

#test add for settings window
def detection_settings_window():

    layout = [[sg.Text('The second form is small \nHere to show that opening a window using a window works')],
              [sg.OK()]]

    window = sg.Window('Settings Form', layout)
    event, values = window.read()
    window.close()

#test add for settings window
def visualize_settings_window():

    layout = [[sg.Text('The second form is small \nHere to show that opening a window using a window works')],
              [sg.OK()]]

    window = sg.Window('Settings Form', layout)
    event, values = window.read()
    window.close()

#added in to see if a menu bar can be easily added without major code rewrites
menu_def = [['&File', ['&Properties', 'E&xit' ]]]

#test add for visualization of detector output window
def visualize_detections_window():
    layout3 = [[sg.Text(
        'Begin Visualizing Processing Results (turn fancy numbers [.json] into red squares on camera trap images)')],
               [sg.Text('Backend Python Scripts'), sg.Input(key='-SCRIPTS_visual-'), sg.FileBrowse()],
               [sg.Text('Original Image Folder Location'), sg.Input(key='-DETECT_visual-'), sg.FolderBrowse()],

               #could be used if you don't have space where the original images were offloaded
               #[sg.Text('New Image Folder Location to Create'), sg.Input(key='-RENDER_visual-'), sg.FolderBrowse()],

               [sg.Text('Confidence Threshold for Detection [Scale of 0 - 1]'), sg.Input(key='-CONFIDENCE_visual-')],
               [sg.Button('Confirm File Locations'), sg.Button('Visualize Results')]]

    window = sg.Window("Visualization Form", layout3)
    event, values = window.read()
    window.close()

#test add for image folder selection window (mainish window)
def image_selection_window():

    layout2 = [[sg.Text('Enter locations')],

                #test add of menu
                [sg.Menu(menu_def, tearoff=False, pad=(20,1))],

                ##changed sg.FolderBrowse to sg.FileBrowse
                #[sg.Text('Backend Python Scripts'), sg.Input(key='-SCRIPTS-'), sg.FileBrowse() ],

                ##changed sg.FolderBrowse to sg.FileBrowse
                #[sg.Text('CNN Model File'), sg.Input(key='-MODEL-'), sg.FileBrowse() ],

                [sg.Text('Image Directory'), sg.Input(key='-TRAP-'), sg.FolderBrowse() ],
                [sg.Button('Confirm Image Directory Location')],
                [sg.Button('Start Detecting Images'), sg.Button('Visualize Detection Results')]]

    window = sg.Window("Detect Wildlife in Camera Traps",
                           layout2,
                           default_element_size=(12, 1),
                           grab_anywhere=True,
                           default_button_element_size=(12, 1))


    # ------ Loop & Process image_selection_window ------ #
    while True:
        event, values = window.read()
        if event is None or event == 'Exit':
            return
        print('Event = ', event)

        # ------ Process menu choices/inputs ------ #
        if event == 'Properties':
            detection_settings_window()
        elif event == 'Start Detecting Images':
            p = Popen("batchprocessdetections.bat", cwd="C:/git/cameratrapsGUI/bat", shell=True)
            stdout, stderr = p.communicate()
        elif event == 'Confirm Image Directory Location':
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
        elif event == 'Visualize Detection Results':
            visualize_detections_window()
            while True:
                if event == 'Confirm File Locations':
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
                                          visualization['-DETECT_visual-'],
                                          '/output.json',
                                          ' ',
                                          visualization['-DETECT_visual-'],
                                          '/detections_visualized'
                                          ' ',
                                          '--confidence',
                                          ' ',
                                          visualization['-CONFIDENCE_visual-'],
                                          ' ',
                                          '--images_dir',
                                          ' ',
                                          visualization['-DETECT_visual-']])

                elif event == 'Visualize Results':
                    p = Popen("visualization.bat.bat", cwd="C:\\git\\cameratrapsGUI\\bat", shell=True)
                    stdout, stderr = p.communicate()
                else:
                    break

        else:
            sg.popup('Cancelled')
            # Need this to end program if 'cancel' button is selected
            sys.exit()

image_selection_window()
