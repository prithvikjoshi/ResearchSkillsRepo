import pandas as pd

from P1T1 import qel, qpeople, B_Area, B_Qh, T_Data, i_Data, B_Name
import numpy as np
from pandas import *


def calc_qhour(fkth, fath, ftint, ftext, fksun, fisun, fqp, fqel):
    """Function to calculate the hourly heating demands of a building on EPFL Campus"""
    # fkth = value of building envelope thermal coefficient (kW/sq.m.-K)
    # fath = value of building envelope area (sq. m.)
    # ftint = internal temperature of building, set at 21˚C
    # ftext = external temperature in a given hour
    # fksun = solar heat gain coefficient of the building
    # fisun = solar irradiance in an hour (W/sq.m.)
    # fqp = heat gains due to people in the given hour
    # fqel = heat gains due to electrical appliances in the given hour
    q_hour = fath * (((fkth / 1000) * (ftint - ftext)) - (fksun * (fisun / 1000)) - (fqp / 1000)) - (fel * fqel)
    return q_hour


def calc_ksunavg(fkth, fath, ftint, ftextavg, fisunavg, fqpavg, fqelavg):
    """Function to calculate average ksun values based on mean values of external conditions in Text +- 1˚C range"""
    # fkth: value of building envelope thermal coefficient (kW/sq.m.-K)
    # fath: value of building envelope area (sq. m.)
    # ftint: internal temperature of building, set at 21˚C
    # ftextavg: mean external temperature in a given hour
    # fisunavg: mean solar irradiance in an hour (W/sq.m.)
    # fqpavg: mean heat gains due to people in the given hour
    # fqelavg: mean heat gains due to electrical appliances in the given hour
    fksunavg = (fath * (((fkth / 1000) * (ftint - ftextavg)) - (fqpavg / 1000)) - (fel * fqelavg)) / (
            fath * (fisunavg / 1000))
    return fksunavg


# setting given parameters
fel = 0.8
Tint = 21

# lists for k_th, k_sun and Q_tot values
Kth = list()
Ksun = list()
TotQDem = list()
# list of all hourly building demands (including 0) of all building (list of list)
Q_th = []

# iterating over heated areas of each building
for building in range(len(B_Area)):
    # starting values
    kthleft = 1
    kthright = 12
    # while no convergence
    while abs(kthleft - kthright) > 10 ** -12:
        kthmiddle = (kthright + kthleft) / 2
        Textavg = list()
        Qpavg = list()
        Qelavg = list()
        Iavg = list()
        # iterating over the hourly temperature data
        for hour in range(len(T_Data)):
            # if temp is between 15 and 17deg: heat gains roughly equal heating load (+- 1deg tolerance)
            if 15 <= T_Data[hour] <= 17:
                Textavg.append(T_Data[hour])
                Qpavg.append(qpeople[hour])
                Qelavg.append(qel[building][hour])
                Iavg.append(i_Data[hour])
        tavg = np.mean(Textavg)
        qpavg = np.mean(Qpavg)
        qelavg = np.mean(Qelavg)
        iavg = np.mean(Iavg)
        ksunleft = calc_ksunavg(kthleft, B_Area[building], Tint, tavg, iavg, qpavg, qelavg)
        ksunright = calc_ksunavg(kthright, B_Area[building], Tint, tavg, iavg, qpavg, qelavg)
        ksunmiddle = calc_ksunavg(kthmiddle, B_Area[building], Tint, tavg, iavg, qpavg, qelavg)

        Qdemleft = list()
        Qdemright = list()
        Qdemmiddle = list()
        i = 0
        # iterating over the hourly temperature data
        for hour in range(len(T_Data)):
            i = i + 1
            # heating activated
            if T_Data[hour] < 16 and qel[0][hour] > 0:
                qdemleft = calc_qhour(kthleft, B_Area[building], Tint, T_Data[hour], ksunleft, i_Data[hour], qpeople[hour],
                             qel[building][hour])
                if qdemleft > 0:
                    Qdemleft.append(qdemleft)

                qdemright = calc_qhour(kthright, B_Area[building], Tint, T_Data[hour], ksunright, i_Data[hour], qpeople[hour],
                              qel[building][hour])
                if qdemright > 0:
                    Qdemright.append(qdemright)

                qdemmiddle = calc_qhour(kthmiddle, B_Area[building], Tint, T_Data[hour], ksunmiddle, i_Data[hour], qpeople[hour],
                               qel[building][hour])
                if qdemmiddle > 0:
                    Qdemmiddle.append(qdemmiddle)

        f1left = sum(Qdemleft) - B_Qh[building]
        f1right = sum(Qdemright) - B_Qh[building]
        f1middle = sum(Qdemmiddle) - B_Qh[building]

        if (f1right * f1middle) < 0:
            kthleft = kthmiddle
        elif (f1left * f1middle) < 0:
            kthright = kthmiddle
    kth = kthright
    knew = kthleft
    f1 = 1
    # while no convergence
    while abs(f1) >= 10 ** -6:
        kth = knew
        Textavg = list()
        Qpavg = list()
        Qelavg = list()
        Iavg = list()
        # hourly heating demand (including 0) for each building
        Q_th_building = []

        # iterating over the hourly temperature data
        for hour in range(len(T_Data)):
            # if temp is between 15 and 17deg: heat gains roughly equal heating load (+- 1deg tolerance)
            if 15 <= T_Data[hour] <= 17:
                Textavg.append(T_Data[hour])
                Qpavg.append(qpeople[hour])
                Qelavg.append(qel[building][hour])
                Iavg.append(i_Data[hour])
        tavg = np.mean(Textavg)
        qpavg = np.mean(Qpavg)
        qelavg = np.mean(Qelavg)
        iavg = np.mean(Iavg)
        ksun = calc_ksunavg(kth, B_Area[building], Tint, tavg, iavg, qpavg, qelavg)
        Qdem = list()
        Qdemdash = list()
        for hour in range(len(T_Data)):
            # heating activated and office hours
            if T_Data[hour] < 16 and qel[0][hour] > 0:
                qdem = calc_qhour(kth, B_Area[building], Tint, T_Data[hour], ksun, i_Data[hour], qpeople[hour],
                         qel[building][hour])
                # only heating needs to ba accounted for
                if qdem > 0:
                    Qdem.append(qdem)
                    Q_th_building.append(qdem)
                    Qdemdash.append(B_Area[building] * (Tint - T_Data[hour]))
                else:
                    Q_th_building.append(0)
            else:
                Q_th_building.append(0)
        f1 = sum(Qdem) - B_Qh[building]
        f1dash = sum(Qdemdash)
        knew = kth - (f1 / f1dash)
    TotQDem.append(int(sum(Qdem)))
    Kth.append(float('%.4f' % float(knew)))
    Ksun.append(float('%.4f' % float(ksun)))
    Q_th.append(Q_th_building)

# calculating the thermal properties of the building envelope
mcpair = (2.5 / 3600) * 1152
Uenv = list()
for value in range(len(Kth)):
    uenv = Kth[value] - mcpair
    Uenv.append(float('%.4f' % float(uenv)))

# outputting the results in a dataframe to check against Tab. 1.1 for verification
CSVDict = {'Building': B_Name, 'Heating Demands (kWh)': TotQDem, 'kth [W/m2-K]': Kth, 'ksun': Ksun,
           'Uenv (W/m2-K)': Uenv}

CSVdf = DataFrame(CSVDict)
CSVdf.to_csv('P1T123.csv')

# generating a dataframe with all heating loads of all times of all buildings (including zeros)
df_Q_th = pd.DataFrame(Q_th)
# dataframe with the hourly sum of all buildings heating load (including zeros)
df_Q_th_hourly_sum = df_Q_th.sum()
