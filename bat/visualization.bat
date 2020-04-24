call c:\Users\Jonathan\Miniconda3\Scripts\activate.bat cameratraps
set PYTHONPATH=c:\git\cameratraps;c:\git\ai4eutils
python C:/git/cameratraps/visualization/visualize_detector_output.py G:/Datasets/test/out.json G:/Datasets/test --confidence 0.9 --images_dir G:/Datasets/test