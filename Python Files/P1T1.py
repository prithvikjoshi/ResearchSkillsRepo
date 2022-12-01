from pandas import *
import numpy as np

# importing sys and os to point to the correct directory when the script finds .csv files
'''import sys, os
os.chdir(sys._MEIPASS)'''
# ------------------------------------initializing given parameters and data--------------------------------------------

# Electricity to heat factor, fel set at 80% by default from given data
fel = 0.8

# Retrieving weather data
Weather_Data = read_csv('Weather.csv')
T_Data = Weather_Data['T_amb_degree_C'].tolist()                        # Temperatures for each hour of the year
i_Data = Weather_Data[' Irr_W_per_m2'].tolist()                         # Irradiance for each hour of the year

# Retrieving building data
Building_Data = read_csv('Buildings.csv')
B_Name = Building_Data['Building'].tolist()                             # Name of the building
B_Year = Building_Data['Construction_year'].tolist()                    # Categorisation by construction year
B_Area = Building_Data['Heated_ground_surface_m2'].tolist()             # Envelope area of building
B_Qh = Building_Data['Annual_Heating_consumption_kWh'].tolist()         # Annual heating demand of the building
B_El = Building_Data[' Annual_Electric_consumption_kWh'].tolist()       # Annual electric demand of the building

# Retrieving building occupancy data
Occupancy_Data = read_csv('Occupancy.csv')
Office_Occ = Occupancy_Data['Office'].tolist()
Canteen_Occ = Occupancy_Data['Canteen'].tolist()
Classroom_Occ = Occupancy_Data['Classroom'].tolist()

# Heat gains from people for various spaces in W/sq.m.
Office_Gain = 5
Canteen_Gain = 35
Classroom_Gain = 23.3

# Share of area of each type of rooms in buildings (0.3 for hallways; remaining 0.7 divided as shown)
Office_Share = 0.3
Canteen_Share = 0.05
Classroom_Share = 0.35

days = np.linspace(1, 365, 365)                             # Initialising list of days in the year

# Calculating the heat gains from people
qpeople = list()                                            # List of hourly heat gains due to people in each building
for day in days:
    # Year begins on a Monday. Neglecting weekends since no one at school!
    if (day + 1) % 7 == 0 or day % 7 == 0:
        for hour in range(24):
            qpeople.append(0)
    else:
        for hour in range(24):
            qpeople.append(
                (Office_Share * Office_Gain * Office_Occ[hour])
                + (Canteen_Share * Canteen_Gain * Canteen_Occ[hour])
                + (Classroom_Share * Classroom_Gain * Classroom_Occ[hour]))

# Calculating the heat gains from electric devices
qel = list()                                        # List of hourly heat gains due to electric appliances in a building
for building in range(len(B_Name)):
    el_h = list()
    for day in days:
        # Year begins on a Monday. Neglecting weekends since no one at school!
        if (day + 1) % 7 == 0 or day % 7 == 0:
            for hour in range(24):
                el_h.append(0)
        else:
            for hour in range(24):
                # Electric devices only turned on between 0700 and 2100; that makes 3654 hours out of 8760 in a year
                if 7 <= hour < 21:
                    el_h.append(B_El[building] / 3654)
                else:
                    el_h.append(0)
    qel.append(el_h)
