# -*- coding: utf-8 -*-

"""
Created on Fri Mar 29 13:36:47 2019

@author: Nauman Ahmed
"""

import numpy as np
import csv
import math
import matplotlib.pyplot as plt

tag1 = 8561
tag2 = 8562

data = np.loadtxt(open('Manav-freestyle.csv', 'rb'), delimiter=',', skiprows=1)

tag_1_array = np.empty([5000, 4])
tag_2_array = np.empty([995, 4])

j = 0
for i in np.linspace(0, 500, num = 5000, endpoint = False):
    tag_1_array[j] = [i, tag1, -100, 0]
    j += 1
    
j = 0
for i in np.linspace(0, 99.5, num = 995, endpoint = False):
    tag_2_array[j] = [i, tag2, -100, 0]
    j += 1

isItfirstrow1 = 1
isItfirstrow2 = 1

firstrow1 = data[0]
firstrow2 = data[0]
  
insert_count1 = 0
insert_count2 = 0

for row in data:
    if row[0] == tag1:
       
        if isItfirstrow1:
            isItfirstrow1 = 0
            firstrow1 = row
        else:
            time_diff = ((row[3] - firstrow1[3])/100000)
            print('tag1: ', time_diff)
            index = math.ceil((time_diff/0.1)) + insert_count1
            new_row = [time_diff, tag1, row[2], row[4]]
            tag_1_array = np.insert(tag_1_array, index, new_row, axis = 0)
            insert_count1 += 1
    
    elif row[0] == tag2:
    
        if isItfirstrow2:
            isItfirstrow2 = 0
            firstrow2 = row
        else:
            time_diff = ((row[3] - firstrow2[3])/100000)
            print('tag2: ', time_diff)
            index = math.ceil((time_diff/0.1)) + insert_count2
            new_row = [time_diff, tag2, row[2], row[4]]
            tag_2_array = np.insert(tag_2_array, index, new_row, axis = 0)
            insert_count2 += 1
            
#plt.plot(tag_1_array[:, 0], tag_1_array[:, 2])
#plt.plot(tag_2_array[:, 0], tag_2_array[:, 2], color = 'r')

f1 = open('Process_data_freestyleManav_tag1.csv', 'w', newline='')
writer1 = csv.writer(f1)
writer1.writerow(['Time_secs', 'EPC', 'PeakRSSI', 'Drowning'])
writer1.writerows(tag_1_array)


f2 = open('Process_data_freestyleManav_tag2.csv', 'w', newline='')
writer2 = csv.writer(f2)
writer2.writerow(['Time_secs', 'EPC', 'PeakRSSI', 'Drowning'])
writer2.writerows(tag_2_array)

f1.close()
f2.close()

