# BScThesis

"Emotion detection from video file/files".

This code was written for the conduction of my BSc thesis in AUEB.

The output if this program was used in the following publication: https://dl.acm.org/doi/abs/10.1145/3461615.3485418

To run the code is required to have setup a python environment. I recommend downloading Anaconda (https://www.datacamp.com/community/tutorials/installing-anaconda-windows).

Make sure you have the following packages installed in your environment: (If you use Anaconda, I have included the required commands)

sys
conda install -c conda-forge r-sys

os
conda install -c jmcmurray os

csv
conda install -c anaconda csvkit

ntpath
conda install -c menpo pathlib

shutil
conda install -c conda-forge pytest-shutil

subprocess
conda install -c omnia subprocess32

xlsxwriter
conda install -c conda-forge xlsxwriter

cv2
conda install -c conda-forge opencv

matplotlib
conda install -c conda-forge matplotlib

deepface
pip install deepface

moviepy
conda install -c conda-forge moviepy

tkinter
conda install -c anaconda tk

Afterwards, follow the video instructions (ADD LINK).

Some IMPORTANT notes about the program:

* The video files which you want to input must be in a separate folder that has nothing else inside.

* The results are written in the same folder as the program.

* It is normal to take a long time to run.

* In the first run it will download some extra things, so it will take a little longer. You must have 2-3 GB available on your main drive.

* Sometimes if it runs for a long time it crashes. In this case you can find the results it has produced so far in the program folder. You can take them and run it again for the remaining videos.
