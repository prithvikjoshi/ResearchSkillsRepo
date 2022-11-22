from pandas import *
import numpy as np


def f(fkth, fath, ftint, ftext, fksun, fisun, fqp, fqel):
    """
    equation for the estimation of internal heat gains
    :param fkth: k_th
    :param fath: heated area
    :param ftint: set internal temperature
    :param ftext: given external temperature
    :param fksun: k_sun
    :param fisun: irradiance
    :param fqp: heat gains due to people
    :param fqel: heat gains due to electric devices
    :return: q_hour, the hourly internal heat gains
    """
    q_hour = fath * (((fkth / 1000) * (ftint - ftext)) - (fksun * (fisun / 1000)) - (fqp / 1000)) - (fel * fqel)
    return q_hour


# ------------------------------------initializing given parameters and data--------------------------------------------

# fel can be set par default to 80 percent
fel = 0.8

# reading given data
Weather_Data = read_csv('Weather.csv')
T_Data = Weather_Data['T_amb_degree_C'].tolist()
i_Data = Weather_Data[' Irr_W_per_m2'].tolist()

# retrieving the building data
Building_Data = read_csv('Buildings.csv')
B_Name = Building_Data['Building'].tolist()
B_Year = Building_Data['Construction_year'].tolist()
B_Area = Building_Data['Heated_ground_surface_m2'].tolist()
B_Qh = Building_Data['Annual_Heating_consumption_kWh'].tolist()
B_El = Building_Data[' Annual_Electric_consumption_kWh'].tolist()

# retrieving the occupancy data
Occupancy_Data = read_csv('Occupancy.csv')
Office_Occ = Occupancy_Data['Office'].tolist()
Canteen_Occ = Occupancy_Data['Canteen'].tolist()
Classroom_Occ = Occupancy_Data['Classroom'].tolist()

# heat gain from people for various spaces
Office_Gain = 5
Canteen_Gain = 35
Classroom_Gain = 23.3

# share of various spaces of all spaces
Office_Share = 0.3
Canteen_Share = 0.05
Classroom_Share = 0.35

days = np.linspace(1, 365, 365)

# calculating the heat gains from people
qpeople = list()
for day in days:
    # accounting for weekends
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
        # accounting for weekends
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

# results from calculation?
kth = 4.149946286413131
ksun = 0.07473836302481052
Tint = 21

Qdem = list()
building = 2

# calculating the internal heat gains
for hour in range(len(T_Data)):
    # if temperature < 16deg and electric heat gains > 0
    if T_Data[hour] < 16 and qel[building][hour] > 0:
        qdem = f(kth, B_Area[building], Tint, T_Data[hour], ksun, i_Data[hour], qpeople[hour],
                 qel[building][hour])
        # cooling can be neglected
        if qdem > 0:
            Qdem.append(qdem)
