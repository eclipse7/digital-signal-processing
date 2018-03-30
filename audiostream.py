"""PyAudio Example: ASIO (callback version)."""

import numpy as np
import pyaudio

WINDOW_SIZE = 256

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

print(p.get_device_info_by_index(14))   # Focusrite ASIO
print(p.get_device_info_by_index(18))   # Focusrite input
print(p.get_device_info_by_index(15))   # Focusrite output


def process_data(in_data):
    n = len(in_data)

    # int16 to float32
    f_data_array = np.zeros(n, dtype=np.float32)
    for i in range(0, n):
        f_data_array[i] = in_data[i] / 32768.0

    # processing data
    for i in range(0, n):
        f_data_array[i] = f_data_array[i] * 1

    # float32 to int16
    out_data = np.zeros(n, dtype=np.int16)
    for i in range(0, n):
        out_data[i] = int(f_data_array[i] * 32768.0)
    return out_data



# define callback (2)
def process_frame(in_data, frame_count, time_info, status):
    data_array = np.fromstring(in_data, dtype=np.int16)
    out_data = process_data(data_array)
    return (out_data, pyaudio.paContinue)


# open stream using callback (3)
stream = p.open(format=pyaudio.paInt16, channels=1, rate=48000,
                input=True,
                output=True,
                input_device_index=14,
                output_device_index=14,
                frames_per_buffer=WINDOW_SIZE,
                stream_callback=process_frame)


# start the stream (4)
stream.start_stream()
print('Latency in: {} ms'.format(int(pyaudio.Stream.get_input_latency(stream) * 1000)))
print('Latency out: {} ms'.format(int(pyaudio.Stream.get_output_latency(stream) * 1000)))

i = input("Press to stop")

# stop stream (6)
stream.stop_stream()
stream.close()

# close PyAudio (7)
p.terminate()
