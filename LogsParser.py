# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import time
import json
import csv
import signal
import keyboard

terminate = False
drowning = 0

def signal_handling(signum,frame):           
    global terminate                         
    terminate = True

def watch(fileName):
    word = 'INFO:sllurp:saw tag(s)'
    completeLog = ''
    global drowning
    
    fp = open(fileName, 'r')
    fo = open('C:\\Users\\Nauman Ahmed\\Documents\\CS856\\RFID_csv.csv', 'w', newline='')
    writer = csv.writer(fo)
    writer.writerow(['EPC', 'Phase', 'PeakRSSI', 'Last Seen Time Stamp', 'Drowning'])
    
    while True:
        
        if (keyboard.is_pressed('space')): # Activate drowning mode by pressing 'space' key
            drowning = 1
            print('Drowning mode activated: %d' % drowning)
        else:
            drowning = 0
            
        if terminate:  # Program closing sequence
            print("Program Terminating!")
            fo.close()
            break
            
        newline = (fp.readline()).rstrip()  # Strip off line break char
        
        if newline:                                                                  
            if word in newline:
                #start = time.time_ns()
                while True:
                    completeLog += newline
                    newline = (fp.readline()).rstrip()  # Strip off line break char
                    if '}]' in newline:   # This indicates the last line of the complete log
                        break
                
                completeLog += newline
                
                chunks = completeLog.split('[')
                JSONStr = (chunks[1])[:-1] # Second split chunk is the JSON 
                
                # Make modifcations to make it a correct JSON string
                JSONStr = JSONStr.replace("\'", "\"")
                JSONStr = JSONStr.replace("u", "")
                JSONStr = JSONStr.replace("(", "")
                JSONStr = JSONStr.replace(",)", "")
                JSONStr = JSONStr.replace("L,", ",")
                
                # Parse JSON and write to csv file
                data = json.loads(JSONStr)
                print(data)
                writer.writerow([data['EPCData']['EPC'], data['ImpinjPhase'], \
                                 data['PeakRSSI'] ,data['LastSeenTimestampUTC'], drowning])
                
                completeLog = '' 
                
                #end = time.time_ns()
                #print("Log processing time: %d ns" % (end - start))
        else:
            time.sleep(0.05)
            print("No new logs seen!")

def main():
    signal.signal(signal.SIGINT,signal_handling)
    file = 'C:\\Users\\Nauman Ahmed\\Documents\\CS856\\rfid.log'         
    watch(file)
    
main()