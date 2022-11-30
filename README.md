# ResearchSkillsRepo

The easiest way to run the programme "P1T123.py" is to run an executable created for Mac OS (in folder "For MACOS") and for Windows (in folder "For Windows"). These can be found in path For Windows (or For MACOS) -> P1T123 -> P1T123.
This will run the code sequence in terminal and generate the result file, P1T123.csv in the same path.

If you wish to open the files in an editor, the root folder has these files along with the csv data files.

Python libraries used:
numpy
pandas

Supporting data files required to run the codes:
Buildings.csv
Occupancy.csv
Weather.csv
Please mae=ke sure these files are in the same folder as the python files.

Python scripts:
P1T1.py
P1T123.py

Two user-defined functions framed in P1T123.py:
calc_qhour: Function to calculate the hourly heating demands of a building on EPFL Campus
calc_ksunavg: Function to calculate average ksun values based on mean values of external conditions in Text +- 1˚C range

This repo is a part of the Project in course ME-454 Modeling of Energy Systems given by Prof. François Maréchal at EPFL. The aim of the project was to design an energy efficient heating system for the campus. As the first step, current heating demands are examined to determine various parameters of buildings that will be required further in the study. k_th is the building envelope thermal conductivity (kW/sq.m.-K) and k_sun the solar irradiance factor. These are aimed at being found for each of the 24 buildings on campus with the script on this repo.

The file P1T1.py analyses the demand and building occupancy profiles to chart down hourly heat gains due to people and electric appliances.

P1T123.py is the successor of this file, which utilises the available data to calculate values of k_th, k_sun and hence the overall heat transfer coefficients of buildings using bisection and newton's numerical schemes. The results are printed to a csv file, P1T123.csv.

For running the code, please open P1T123.py and run it. P1T1.py does not need to be executed separately since P1T123.py runs it to derive the precursor data from it.

The results can then be viewed in P1T123.csv.

Good luck running the files!