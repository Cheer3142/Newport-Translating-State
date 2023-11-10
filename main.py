'''
import time
import datetime
import json
import os
from PIL import Image, ImageTk
import cv2
import serial
from collections import deque
'''


import time
import PortModule
import numpy as np
import matplotlib.pyplot as plt
import nidaqmx
from nidaqmx.constants import AcquisitionType


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
    a = PortModule.serial_ports()
    return a

def select_port(label):
    global Actuator
    Actuator = PortModule.ConnectPort(label)         

    for i in range(20):
        return_word =  query("ID?", str(i))
        if return_word:
            print(return_word) # b'SNB169273'
            print("------ Done ------")
            return str(i)
    
    return False
    
def write(com, option):
    Actuator.write("{}{}\n\r".format(option, com).encode())
    print("{}{}\n\r".format(option, com).encode())
    time.sleep(0.1)
        
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

### Port Search ###
print("Port Search.....")
port_available = port_search()
print(port_available)
if len(port_available) == 0:
    print("No Port and exit")
    exit()

### Axe Finder ###
selected_port = int(input("Your Port's index (zero start): "))
axe = select_port(port_available[selected_port])
if not axe: 
    print("No actuator available and exit")
    exit()

### Declare the dynamic range and velocity ###
obs_velocity    = 0.1
distance        = 10

### Initialize variables for data storage and plotting ###
wtime       = distance/obs_velocity
clk_rate    = 50000
num_samples = clk_rate * wtime                      # wtime seconds at clk_rate Hz
time_values = np.linspace(0, wtime, num_samples)
data_buffer = []
# data_buffer = np.zeros(num_samples)

### Configure NI DAQmx settings ###
task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai2:3")
task.timing.cfg_samp_clk_timing(rate=clk_rate,
                                sample_mode=AcquisitionType.FINITE,
                                samps_per_chan=num_samples)

### Create the plot ###
plt.ion()                                       # Enable interactive mode for dynamic updating
fig, ax = plt.subplots(1, 2, figsize=(15, 4))
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Voltage (V)')
ax[0].set_title('Analog Input Channel 2')
line0, = ax[0].plot([], [])

ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Voltage (V)')
ax[1].set_title('Analog Input Channel 3')
line1, = ax[1].plot([], [])

exit()    #######################################################################################################################
### Start Command List (Start at +45) ###
stcom_lst   = ["MO", "OR", "WS", "VA10", "PA+35", "WS", "VA{}".format(obs_velocity)]   
stcom_con   = ';'.join(stcom_lst) 

### Back and Forth Command ###
back        = "PR-{};WS".format(distance)
forth       = "PR+{};WS".format(distance)

### Running ###
print("Running Task.....")
write(stcom_con, axe)                       

'''
Status Check
- TS = Get controller status  
- MD =  read motion done status
'''
ts_stat = query("TS?", axe)    
ts_md   = query("MD?", axe)
time.sleep(10)
ts_stat2 = query("TS?", axe)    
ts_md2   = query("MD?", axe)

exit()    #######################################################################################################################
### Move forth form +35 to +45 ###
move_done()
write(forth, axe)         # +10
try:
    task.start()
    data_buffer.append(task.read(number_of_samples_per_channel=
                                    nidaqmx.constants.READ_ALL_AVAILABLE, 
                                    timeout=wtime)) #task.wait_until_done()
    
    ### Set the data ###
    line0.set_data(time_values, data_buffer[-1][0])
    ax[0].relim()
    ax[0].relim()
    line1.set_data(time_values, data_buffer[-1][1])
    ax[1].relim()
    ax[1].autoscale_view()

    ### Fix ###
    fig.canvas.draw()
    fig.canvas.flush_events()
    task.stop()
finally:
    print('Closing The Task')
    task.close()

''' 
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
'''

# Close connection #######################################################################################################################
print('---------- CLose Port ----------')
Actuator.close()































