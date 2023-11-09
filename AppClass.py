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
- OR = search for home
- MF = Power OFF
- MO = Power ON
- BQ = Enable/disable DIO jog mode
- EP = Enter program mode             ****
- QP = exit program entry mode        ****
- EX = execute compiled program #1    ****
- WS = wait for stop

Move:
- ST = Stop motion
- JW = Set jog low speed
- VA = Set Velocity

Query:
- ID = Get stage model and serial number
- DP = Get target position
- DV = Get working speed
- TP = Get position
- TS = Get controller status          
- TV = Get velocity
- MD = Read motion done status
'''

def move_done():
    while True:
        ts_md   = query("MD?", axe)
        if Done:
            break
        time.sleep(1)

def port_search():
    # Call "PortModule"
    a = PortModule.serial_ports()
    return a

def select_port(label):
    global Actuator
    Actuator = PortModule.ConnectPort(label)         

    for i in range(20):
        return_word =  query("ID?", str(i))
        if return_word:
            print(return_word) # b'SNB169273'
            break
    
    print("------ Done ------")
    return str(i)

def write(com, option):
    Actuator.write("{}{}\n\r".format(option, com).encode())
    print("{}{}\n\r".format(option, com).encode())
    time.sleep(0.1)
        
    
# Define a function to write/read commands to the actuator    
def query(com, option):
    if option.isnumeric():
        Actuator.write("{}{}\n\r".format(option, com).encode())
    print("{}{}\n\r".format(option, com).encode())
    time.sleep(0.1)

    try:
        resp = Actuator.readline().split()[-1]
        print(resp)
        return resp
    except:
        raise Exception("Query Error: ", com)
        print("Query Error: ", com)
        return False

def lst_com(lst, axe):
    for com in lst:
        write(com, axe)
        time.sleep(0.1)
'''
Spec:
    speed = 1.8 mm/s
    Sampling rate = 50k Hz
"XX", "EP"
Actuator.write("QP\n\r".encode())
query("XM", 1)
write("EX", i)
'''

# Port Search
print("Port Search.....")
port_available = port_search()
print(port_available)
if len(port_available) == 0:
    print("No Port")
    exit()

# Initialize Parameters
selected_port = int(input("Your Port's index (zero start): "))
axe = select_port(port_available[selected_port])

# Initialize variables for data storage and plotting
data_buffer = [deque(maxlen=AnalogInput.num_samples), deque(maxlen=AnalogInput.num_samples)]
time_buffer = deque(maxlen=AnalogInput.num_samples)
obs_velocity    = 0.1
distance        = 10
wtime = distance/obs_velocity

# Start Command List    (Start at +45)
stcom_lst   = ["MO", "OR", "VA10", "PA+35", "WS", "VA{}".format(obs_velocity)]   

# Back and Forth COmmand List
back        = "PR-10"
forth       = "PR+10"

# Running
print("Running Task.....")
lst_com(stcom_lst, axe)                          

'''
Status Check
- TS = Get controller status  
- MD =  read motion done status
'''
ts_stat = query("TS?", axe)    
ts_md   = query("MD?", axe)
time.sleep(4)
ts_stat2 = query("TS?", axe)    
ts_md2   = query("MD?", axe)
# Actuator.close()
exit()

# Move forth form +35 to +45 
move_done()
write(forth, axe)         # +10
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































