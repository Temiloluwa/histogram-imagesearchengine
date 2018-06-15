## 3D Histogram Imagesearch Engine

A simple imagesearch engine using OpenCV and Numpy

### Dependencies

This program was developed in a conda environment on a windows machine.
The following simple guidelines can serve as a guide for installing OpenCV:

- Install the latest version of Anaconda
- Open the Anaconda command line
- Install a virtual environment for Anaconda
- Use conda install to install open cv3 on the new environment 
- Ensure the new environment name is included in the update command (conda install -n <new environment> -c menpo opencv3)
- Activate the new environment

The following website can serve as a reference: https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/20/conda/

### Running The Program
The program is run supplying arguments from the commandline to the searcher.py file.
The following flags and positional arguments are required to run the program:

- flag '-b' or '-bins', comma seperated values to indicate number of bins per channel. Example: 8,12,3
- flag '-d' or '--dataset', path name of the dataset containing images: Example: imagesearch or imagesearch/dataset
- flag '-i' or '--img', path name of query image for the search: Example: seaworld.jpg
- flag '-f' or '--feat', a filename ending in .csv for storing feature vectors of dataset: Example: featureVector.csv

Example: python searcher.py -b 8,12,3 -d imagesearch -i seaworld.jpg -f featureVector.csv