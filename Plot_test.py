import matplotlib.pyplot as plt
import random
from collections import deque
import numpy as np

# Create the plot
plt.ion()  # Enable interactive mode for dynamic updating
fig, ax = plt.subplots(1, 2, figsize=(15, 4))
time_values = np.linspace(0, 5, 5000)
line, = ax[0].plot(time_values, np.zeros(5000))
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Voltage (V)')
ax[0].set_title('Analog Input Port 0')

line = [line]
temp, = ax[1].plot(time_values, np.zeros(5000))
line.append(temp)
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Voltage (V)')
ax[1].set_title('Analog Input Port 1')


# Initialize The data storage
data_buffer = [deque(maxlen=50000), deque(maxlen=50000)]
time_buffer = deque(maxlen=50000)
i = 0

print(i)
while True:
    try:
        print(i)
        # Extend the new data
        data_buffer[0].extend([random.randint(0, 10)])
        data_buffer[1].extend([random.randint(0, 10)])
        time_buffer.extend([i])
        i = i + 1

        # Plot Axis#0
        line[0].set_xdata(time_buffer)
        line[0].set_ydata(data_buffer[0])
        ax[0].relim()
        ax[0].autoscale_view()

        # Plot Axis#0
        line[1].set_xdata(time_buffer)
        line[1].set_ydata(data_buffer[1])
        ax[1].relim()
        ax[1].autoscale_view()

        plt.pause(0.01)
    except (KeyboardInterrupt,SystemExit,Exception):
        plt.ioff()  # Turn off interactive mode
        break

''' 
import logging
import threading
import time

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=thread_function, args=(1,))
    logging.info("Main    : before running thread")
    x.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()
    logging.info("Main    : all done")
'''
