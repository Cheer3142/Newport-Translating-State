"""
Real time reading
Example: DAQmx-Python Analog Input Acquisition and Plot With History (NI 2023)
Author: Davit Danielyan

DISCLAIMER: The attached Code is provided As Is. It has not been tested or validated as a product, for use in a
deployed application or system, or for use in hazardous environments. You assume all risks for use of the Code and
use of the Code is subject to the Sample Code License Terms which can be found at: http://ni.com/samplecodelicense
"""

import numpy as np
import matplotlib.pyplot as plt
import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration
from collections import deque
import time

# Initialize variables for data storage and plotting
wtime       = 5
clk_rate    = 50000
num_samples = int(clk_rate * wtime)  # 5 seconds at 5000 Hz
time_values = np.linspace(0, 5, num_samples)

# Configure NI DAQmx settings
task = nidaqmx.Task()
# task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")
# task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai1")
task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0:1")
task.timing.cfg_samp_clk_timing(rate=clk_rate
                                ,sample_mode=AcquisitionType.FINITE
                                ,samps_per_chan=num_samples)

# # Initialize variables for plotting
# history_length = 10  # seconds
# num_samples = int(task.timing.samp_clk_rate * history_length)
# time_values = np.linspace(-history_length, 0, num_samples)

# # Initialize The data storage
data_buffer = [deque(maxlen=num_samples), deque(maxlen=num_samples)]
time_buffer = deque(maxlen=num_samples)

# Create the plot
plt.ion()  # Enable interactive mode for dynamic updating
fig, ax = plt.subplots(1, 2, figsize=(15, 4))
line, = ax[0].plot(time_values, np.zeros(num_samples))
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Voltage (V)')
ax[0].set_title('Analog Input Port 0')

line = [line]
temp, = ax[1].plot(time_values, np.zeros(num_samples))
line.append(temp)
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Voltage (V)')
ax[1].set_title('Analog Input Port 1')
task.start()

# Main function
def read(data_buffer, time_buffer):
    new_data = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE, 
                         timeout=5.0)  # Read 50 samples
    timestamp = time.time()

    # Extend the new data
    data_buffer[0].extend(new_data[0])
    data_buffer[1].extend(new_data[1])
    time_buffer.extend([timestamp] * len(new_data[0]))

    # Time Mask Create
    time_diff = np.array(time_buffer) - time_buffer[-1]
    mask = time_diff > -5

    # Plot Axis#0
    line[0].set_xdata(-time_diff[mask])
    line[0].set_ydata(np.array(data_buffer[0])[mask])
    ax[0].relim()
    ax[0].autoscale_view()

    # Plot Axis#0
    line[1].set_xdata(-time_diff[mask])
    line[1].set_ydata(np.array(data_buffer[1])[mask])
    ax[1].relim()
    ax[1].autoscale_view()
    
    plt.ioff()  # Turn off interactive mode
    plt.show()                                         # Pause to allow the plot to update
    return (data_buffer, time_buffer)

if __name__ == '__main__':
    while True:
        try:
            data_buffer, time_buffer =  read(data_buffer, time_values)
        except (KeyboardInterrupt,SystemExit):
            task.stop()
            task.close()
            plt.ioff()  # Turn off interactive mode
            break
