import configparser

config = configparser.ConfigParser()

config.read('test.ini')

Batch_Detector_Loc = config['default']['batch_detector_script_file_location']

print(Batch_Detector_Loc)