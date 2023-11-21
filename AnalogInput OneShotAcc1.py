'''
One shot reading
'''

import numpy as np
import matplotlib.pyplot as plt
import nidaqmx
from nidaqmx.constants import AcquisitionType
import pandas as pd
# import time

# Initialize variables for data storage and plotting
wtime       = 5
clk_rate    = 50000
num_samples = clk_rate * wtime  # 5 seconds at 5000 Hz
time_values = np.linspace(0, wtime, num_samples)
#data_buffer = []
df = pd.DataFrame(index=time_values)
#data_buffer = np.zeros(num_samples)


# Configure NI DAQmx settings
task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai2:3")
task.timing.cfg_samp_clk_timing(rate=clk_rate,
                                sample_mode=AcquisitionType.FINITE,
                                samps_per_chan=num_samples)


# Create the plot
plt.ion()                       # Enable interactive mode for dynamic updating
fig, ax = plt.subplots(1, 2, figsize=(15, 4))
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Voltage (V)')
ax[0].set_title('Analog Input Channel 2')

ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Voltage (V)')
ax[1].set_title('Analog Input Channel 3')


line0, = ax[0].plot([], [], 'r')
line1, = ax[1].plot([], [], 'g')

# Initialize variable for timing
# b = time.time()

try:
    for i in range(5):
        # print(time.time() - b)
        # a = time.time()
        
        task.start()
        df['head{}'.format(i)], df['low{}'.format(i)] = task.read(number_of_samples_per_channel = nidaqmx.constants.READ_ALL_AVAILABLE
                                            , timeout=wtime)
        #data_buffer.append(task.read(number_of_samples_per_channel=
        #                             nidaqmx.constants.READ_ALL_AVAILABLE, timeout=wtime)) #task.wait_until_done()
        # b = time.time()
        # print(b-a, end=' ')
        
        ### Plot Axis#0 ###
        # ax[0].plot(time_values, data_buffer[-1][0], label='attempt {}'.format(i+1))
        line0.set_data(time_values, df['head{}'.format(i)])
        ax[0].relim()
        ax[0].autoscale_view()
        # ax[0].legend()

        ### Plot Axis#1 ###
        # ax[1].plot(time_values, data_buffer[-1][1], label='attempt {}'.format(i+1))
        line1.set_data(time_values, df['low{}'.format(i)])
        ax[1].relim()
        ax[1].autoscale_view()
        # ax[1].legend()

        fig.canvas.draw()
        fig.canvas.flush_events()
        task.stop()
finally:
    print('Closing The Task')
    task.stop()
    task.close()














