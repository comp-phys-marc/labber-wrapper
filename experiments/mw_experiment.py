import Labber
import numpy as np
import time
from dataclasses import dataclass
from typing import Optional
import matplotlib
import matplotlib.pyplot as plt
import json

from labberwrapper.devices.Keysight_PXI_AWG import KeysightPXIAWG
from labberwrapper.devices.Keysight_PXI_Digitizer import KeysightPXIDigitizer


@dataclass
class Piece(object):
    volts: float
    time_ns: float
    ramp_time_ns: Optional[float] = None


class Piecewise(object):

    def __init__(self, pieces, ramp_time_ns, resolution_ns=1):
        for piece in pieces:
            assert isinstance(piece, Piece)
            if piece.ramp_time_ns is None:
                piece.ramp_time_ns = ramp_time_ns

        self._pieces = pieces
        self._ramp_time = ramp_time_ns
        self._piece_index = 0
        self._resolution = resolution_ns

    def add(self, piece):
        assert isinstance(piece, Piece)
        if piece.ramp_time_ns is None:
            piece.ramp_time_ns = self._ramp_time
        self._pieces.append(piece)

    def insert(self, piece, index):
        assert isinstance(piece, Piece)
        before = self._pieces[0:index]
        after = self._pieces[index:]
        self._pieces = before + [piece] + after

    def remove(self, index):
        del self._pieces[index]

    def __iter__(self):
        return self

    def __next__(self):
        if self._piece_index < len(self._pieces):
            self._piece_index += 1
            return self._pieces[self._piece_index]
        raise StopIteration


def software_piecewise_microwave(
    piecewise,
    verbose=True
):

    # connect to server
    client = Labber.connectToServer('localhost')

    awg = KeysightPXIAWG(client)
    digitizer = KeysightPXIDigitizer(client)

    if verbose:
        # print AWG overview
        print(awg.instr.getLocalInitValuesDict())

        # print Digitizer overview
        print(digitizer.instr.getLocalInitValuesDict())

    millivolt = 10 ** -3

    reads = []

    for volt in np.cos(np.linspace(0, 10, 1000)) * 10 * millivolt:
        awg.setValue('Ch1 - Offset', volt)
        time.sleep(0.01)
        values = digitizer.getValue('Ch1 - Signal')
        reads.append(values['y'].max())

    digitizer.stopInstrument()
    awg.stopInstrument()

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(np.linspace(0, 1, 1000), reads)  # Plot some data on the axes.
    ax.set_xlabel('10 seconds')
    ax.set_ylabel('volts')

    # close connection
    client.close()


def hardware_piecewise_microwave():

    # connect to server
    client = Labber.connectToServer('localhost')

    awg = KeysightPXIAWG(client)
    digitizer = KeysightPXIDigitizer(client)

    millivolt = 10 ** -3

    awg.setValue('Ch1 - Waveform', np.linspace(0.0, 10 * millivolt, 10))
    awg.setValue('Ch1 - Waveform - Sweep rate', 0.2)
    reads = digitizer.getValue('Ch1 - Signal')['y']

    time.sleep(10)

    digitizer.stopInstrument()
    awg.stopInstrument()

    fig, ax = plt.subplots()  # Create a figure containing a single axes.
    ax.plot(np.linspace(0, 1, 10), reads)  # Plot some data on the axes.
    ax.set_xlabel('10 seconds')
    ax.set_ylabel('volts')

    # close connection
    client.close()


if __name__ == '__main__':
