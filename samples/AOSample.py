from d2kdask import D200X, Buffer
from d2kdask import BufferType, OutputChannel, Definite, SyncMode, StopMode
import d2kdask
import numpy as np
import matplotlib.pyplot as plt
from time import sleep


def cos_wave(freq, time):
    return np.sin(2*np.pi * freq * time)


def generate_wave(freq, seconds, sample_rate=44100, amplitude=1):
    wave = [
        amplitude * cos_wave(freq, t)
        for t in np.linspace(0, seconds, sample_rate * seconds)]
    wave = np.array(wave)
    wave *= 32767
    wave += 32766
    return wave.astype(np.uint16)


def main():
    BASETIME = 40000000
    SCAN_INTERVAL = 160

    sample_rate = BASETIME / SCAN_INTERVAL

    wave = generate_wave(freq=440, seconds=1, sample_rate=4000, amplitude=1)

    card = D200X(d2kdask.Card.DAQ_2005, 0)
    buffer = Buffer(card.id_, n_samples=4000,
                    buffer_type=BufferType.AnalogOutput)

    buffer.set_data(wave)

    card.ao_cont_write_channel(
        OutputChannel.Zero, buffer, 30, SCAN_INTERVAL, SCAN_INTERVAL,
        SyncMode.Asynchronous)

    while True:
        stopped, writeCount = card.ao_async_check()
        print("Write count: ", writeCount)
        sleep(0.1)
        if stopped:
            break

    card.ao_async_clear(StopMode.NextCounterUpdate)


if __name__ == "__main__":
    main()
