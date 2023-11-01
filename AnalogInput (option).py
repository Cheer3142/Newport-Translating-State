import numpy as np
import matplotlib.pyplot as plt
import nidaqmx
from nidaqmx.constants import AcquisitionType, TerminalConfiguration

# Initialize variables for data storage and plotting
wtime       = 5
clk_rate    = 50000
num_samples = int(clk_rate * wtime)  # 5 seconds at 5000 Hz
time_values = np.linspace(0, 5, num_samples)
#data_buffer = np.zeros(num_samples)


# Configure NI DAQmx settings
task = nidaqmx.Task()
task.ai_channels.add_ai_voltage_chan("cDAQ1Mod1/ai0")
task.timing.cfg_samp_clk_timing(rate=clk_rate,
                                sample_mode=AcquisitionType.FINITE,
                                samps_per_chan=num_samples)


# Create the plot
plt.ion()  # Enable interactive mode for dynamic updating
fig, ax = plt.subplots()
ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage (V)')
ax.set_title('Analog Input from Dev1/ai0')
task.start()


try:
    data_buffer = task.read(number_of_samples_per_channel=nidaqmx.constants.READ_ALL_AVAILABLE, timeout=5.0)

    task.wait_until_done()

    ax.plot(time_values, data_buffer)
    plt.ioff()  # Turn off interactive mode
    plt.show()
    print(1)
finally:
    task.stop()
    task.close()
