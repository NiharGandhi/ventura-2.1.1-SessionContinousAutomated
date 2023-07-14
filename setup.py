import sys
from cx_Freeze import setup, Executable
import os

# Dependencies
build_exe_options = {
    'packages': ['cv2', 'face_recognition', 'numpy', 'datetime', 'os', 'csv', 'pyttsx3', 'PyQt5', 'firebase_admin'],
    'include_files': ['user_interface/', 'resource.qrc', 'face_enc', 'ventura-5d1fe-firebase-adminsdk-q6x4i-2a488de72f.json']
}

# Create the executable
executables = [
    Executable(
        'mainwindow.py',
        base=None,
        icon='icon.ico'  # Replace with the path to your application icon file
    )
]

# Setup configuration
setup(
    name='Ventura - Automated',
    version='2.1.1',
    description='Ventura- Face Recognition - Automated Continous Entries',
    options={'build_exe': build_exe_options},
    executables=executables
)

# Rename the output file
output_dir = os.path.join('build', 'exe.win-amd64-3.10')  # Replace with the appropriate output directory
output_file = os.path.join(output_dir, 'mainwindow.exe')  # Replace with the desired output file name
new_output_file = os.path.join(output_dir, 'Ventura-Automated.exe')  # Replace with the desired new output file name
os.rename(output_file, new_output_file)