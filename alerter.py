import os
duration = 4  # seconds
freq = 440  # Hz

def alertit():
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))