import numpy as np
from time import sleep
from influx_client import initiate_client


time = np.arange(-100*np.pi, 100*np.pi, 0.01)
amplitude = np.sin(time).tolist()

influx = initiate_client()

for i in amplitude:
    influx.send_data(
        bucket="chris-bucket",
        measurement="sine-wave",
        location="earth",
        temperature=i
    )
    print(i)
    sleep(0.01)

influx.client.close()
