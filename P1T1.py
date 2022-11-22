from pandas import *
import numpy as np

# ------------------------------------initializing given parameters and data--------------------------------------------

# fel set at 80% by default from literature
fel = 0.8

# retrieving weather data
Weather_Data = read_csv('Weather.csv')
T_Data = Weather_Data['T_amb_degree_C'].tolist()
i_Data = Weather_Data[' Irr_W_per_m2'].tolist()

# retrieving building data
Building_Data = read_csv('Buildings.csv')
B_Name = Building_Data['Building'].tolist()
B_Year = Building_Data['Construction_year'].tolist()
B_Area = Building_Data['Heated_ground_surface_m2'].tolist()
B_Qh = Building_Data['Annual_Heating_consumption_kWh'].tolist()
B_El = Building_Data[' Annual_Electric_consumption_kWh'].tolist()

# retrieving building occupancy data
Occupancy_Data = read_csv('Occupancy.csv')
Office_Occ = Occupancy_Data['Office'].tolist()
Canteen_Occ = Occupancy_Data['Canteen'].tolist()
Classroom_Occ = Occupancy_Data['Classroom'].tolist()

# heat gains from people for various spaces in W/sq.m.
Office_Gain = 5
Canteen_Gain = 35
Classroom_Gain = 23.3

# share of each type of rooms in buildings
Office_Share = 0.3
Canteen_Share = 0.05
Classroom_Share = 0.35

days = np.linspace(1, 365, 365)

# calculating the heat gains from people
qpeople = list()
for day in days:
    # Neglecting weekends since no one at school!
    if (day + 1) % 7 == 0 or day % 7 == 0:
        for hour in range(24):
            qpeople.append(0)
    else:
        for hour in range(24):
            qpeople.append(
                (Office_Share * Office_Gain * Office_Occ[hour]) + (Canteen_Share * Canteen_Gain * Canteen_Occ[hour]) + (
                        Classroom_Share * Classroom_Gain * Classroom_Occ[hour]))

# calculating the heat gains from electric devices
qel = list()
for building in range(len(B_Name)):
    el_h = list()
    for day in days:
        # Neglecting weekends since no one at school!
        if (day + 1) % 7 == 0 or day % 7 == 0:
            for hour in range(24):
                el_h.append(0)
        else:
            for hour in range(24):
                # electric devices only turned on between 7h and 21h
                if 7 <= hour < 21:
                    el_h.append(B_El[building] / 3654)
                else:
                    el_h.append(0)
    qel.append(el_h)
