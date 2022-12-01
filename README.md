# ResearchSkillsRepo

This repo is a part of the Project in course ME-454 Modeling of Energy Systems given by Prof. François Maréchal at EPFL. The aim of the project is to design an energy efficient heating system for the campus. As the first step, current heating demands are examined to determine various parameters of buildings that will be required further in the study. The set of codes included in this repo give these parameters as the output.

k_th is the building envelope thermal conductivity (W/sq.m.-K) and k_sun the solar irradiance factor.

## Cloning the Repo to your Machine

git commands can be used to clone the repository to your machine. Make sure you have git installed, and then run git bash with the following command:

git clone https://github.com/prithvikjoshi/ResearchSkillsRepo.git

The repo should then start getting integrated to the directory that you bashed to. (For e.g. Documents)

## Running the Code

The folder "Python Files" includes two python files, P1T1.py and P1T123.py. In addition, three csv data files viz. Buildings.csv, Occupancy.csv, and Weather.csv can be found in this folder. P1T123.py imports some calculated lists from P1T1.py, and hence is the only main code to be run to obtain the results. A csv file, P1T123.csv will be created upon successful execution of the codes and be saved in the same folder.

Steps to follow:
1. Open Command Prompt (or Terminal) on your machine.

2. Change the directory to point to the repo's Python Files folder.
For e.g. if it is in Documents, run:\
cd C:/Users/**"Username"**/Documents/ResearchSkillsRepo/"Python Files"

3. Install the required dependencies first by running:\
pip install -r requirements.txt\
(Note: if you face an error stating that pip can not be found as a cmdlet, you need to add python.exe to path. Please see the bottom of the file to get directions to do so.)

4. Once the dependencies are installed, run the program by executing:\
python P1T123.py\
(Note: If your machine has an older version of Python and Python 3.x, you might have to use command python3 instead of python)

In a few seconds of computation time, the file P1T123.csv should get formed in the folder with the results. k_th, k_sun and U values are the ones generated by the code.


## Details of how the Code Runs

The file P1T1.py analyses the demand and building occupancy profiles to chart down hourly heat gains due to people and electric appliances.

P1T123.py is the successor of this file, which utilises the available data to calculate values of k_th, k_sun and hence the overall heat transfer coefficients of buildings using bisection and newton's numerical schemes. The results are printed to a csv file, P1T123.csv.


## Executable Files for easy running

For ease of access, executable files have been made for Windows and UNIX based users (Mac and Linux). One can go to the respective folder, either For Windows or For MACOS, then P1T123 and then execute the application file named P1T123. This will generate a csv file P1T123.csv in the folder as a result.


## Library, Functions, and Data file Specifications

Python libraries used:
numpy
pandas

Supporting data files required to run the codes:
Buildings.csv
Occupancy.csv
Weather.csv

Python scripts:
P1T1.py
P1T123.py

Two user-defined functions framed in P1T123.py:
calc_qhour: Function to calculate the hourly heating demands of a building on EPFL Campus
calc_ksunavg: Function to calculate average ksun values based on mean values of external conditions in Text +- 1˚C range


## Add Python to Path

A simple tutorial to do so can be found at https://realpython.com/add-python-to-path/


## Contributors

Prithvi Joshi\
Florien Strebl\
Markus Grönblad

## License

The content of this repository is released under the MIT License and is made available to use for users under the Open Source terms of agreement.


## Acknowledgements

Gratitude to the Real Python team (https://realpython.com/) for making tutorials available for widespread reference.