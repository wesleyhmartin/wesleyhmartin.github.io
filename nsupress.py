import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 500  # adjust: smaller = more sensitive
HPF_CUTOFF = 100  # high-pass cutoff in Hz

p = pyaudio.PyAudio()

# Input (mic)
input_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                      input=True, frames_per_buffer=CHUNK)

# Output (headphones)
output_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                       output=True)

print("Live monitoring with noise suppression... Press Ctrl+C to stop.")

try:
    while True:
        data = input_stream.read(CHUNK, exception_on_overflow=False)
        samples = np.frombuffer(data, dtype=np.int16)

        # High-pass filter (remove low-frequency hum)
        fft = np.fft.rfft(samples)
        freqs = np.fft.rfftfreq(len(samples), 1.0 / RATE)
        fft[freqs < HPF_CUTOFF] = 0
        filtered = np.fft.irfft(fft)

        # Noise gate: mute samples under threshold
        filtered = np.where(np.abs(filtered) > THRESHOLD, filtered, 0)

        # Back to bytes
        output_stream.write(filtered.astype(np.int16).tobytes())
except KeyboardInterrupt:
    pass

input_stream.stop_stream()
input_stream.close()
output_stream.stop_stream()
output_stream.close()
p.terminate()
