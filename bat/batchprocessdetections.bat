call c:\Users\Jonathan\Miniconda3\Scripts\activate.bat cameratraps-detector
set PYTHONPATH=c:\git\cameratraps;c:\git\ai4eutils
python C:/git/cameratraps/detection/run_tf_detector_batch.py C:/models/megadetector_v3.pb G:/Datasets/test G:/Datasets/test/out.json --recursive