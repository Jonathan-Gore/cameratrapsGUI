call C:\Users\Jonathan\Miniconda3\Scripts\activate.bat cameratraps-detector
set PYTHONPATH=c:\git\cameratraps;c:\git\ai4eutils
python C:\git\cameratraps\detection\run_tf_detector_batch.py C:\models\megadetector_v3.pb G:\Datasets\Test G:\Datasets\Test\out.json --recursive

cmd /k