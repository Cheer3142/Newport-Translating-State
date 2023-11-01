'''
import time
import datetime
import json
import os
from PIL import Image, ImageTk
import cv2
import serial
'''

import time
import PortModule
import AnalogInput
from collections import deque

'''
Command List (Axis = 1)
OR = search for home
MF = Power OFF
MO = Power ON
BQ = Enable/disable DIO jog mode
EP = Enter program mode             ****
QP = exit program entry mode        ****
EX = execute compiled program #1    ****
WS = wait for stop

Move:
ST = Stop motion
JW = Set jog low speed
VA = Set Velocity

Query:
ID = Get stage model and serial number
DP = Get target position
DV = Get working speed
TP = Get position
TS = Get controller status
TV = Get velocity
'''

def port_search():
    # Call "PortModule"
    a = PortModule.serial_ports()
    return a

def select_port(label):
    global Actuator
    Actuator = PortModule.ConnectPort(label)         

    for i in range(20):
        return_word =  query("ID?", str(i))
        # b'SNB169273'
        if return_word:
            # print(return_word)
            
            break
    
    print("------ Done ------")
    return i

def write(com, option):
    time.sleep(0.1)
    Actuator.write("{}{}\n\r".format(option, com).encode())
    print("{}{}\n\r".format(option, com).encode())
        
    
# Define a function to write/read commands to the actuator    
def query(com, option):
    time.sleep(0.1)
    Actuator.write("{}{}\n\r".format(option, com).encode())

    try:
        time.sleep(0.1)
        resp = Actuator.readline().split()[-1]
        print(resp)
        return resp
    except:
        print("Query Error: ", com)
        return False

def lst_com(lst, axe):
    for com in lst:
        write(com, axe)
        time.sleep(0.1)

port_available = port_search()
print(port_available)
if len(port_available) == 0:
    print("No Port")
    exit()

selected_port = int(input("Your Port's index: "))
axe = select_port(port_available[selected_port])
data_buffer = [deque(maxlen=AnalogInput.num_samples), deque(maxlen=AnalogInput.num_samples)]
time_buffer = deque(maxlen=AnalogInput.num_samples)

'''
Spec:
    speed = 1.8 mm/s
    Sampling rate = 50k Hz
'''

# "XX", "EP"
# Actuator.write("QP\n\r".encode())
# query("XM", 1)
# write("EX", i)
obs_velocity    = 1.8
distance        = 10
stcom_lst   = ["MO", "OR", "VA10", "PA+45", "WS", "VA{}".format(obs_velocity)]
back        = ["PR-10", "WS"]
forth       = ["PR+10", "WS"]

lst_com(stcom_lst, axe)                          # Start at +35
wtime = distance/obs_velocity
time.sleep(2)

# Move forth form +35 to +45 
write("PR-{}".format(distance), axe)         # +10
st = time.time()
while True:
    try:
        data_buffer, time_buffer = AnalogInput.read(data_buffer, time_buffer)
        if time.time() - st > wtime:
            break
    except (KeyboardInterrupt, SystemExit):
        print("Exit by Keyboard Interrupt")
        AnalogInput.task.stop()
        AnalogInput.task.close()
        AnalogInput.plt.ioff()  # Turn off interactive mode
        break
    
# Close connection
print('---------- CLose Port ----------')
Actuator.close()































