import Labber
import numpy as np
import time
from dataclasses import dataclass
from typing import Optional
from math import floor
import json
from jsonschema import validate

from labberwrapper.devices.Keysight_PXI_AWG import KeysightPXIAWG
from labberwrapper.devices.Keysight_PXI_Digitizer import KeysightPXIDigitizer
from labberwrapper.logging.log import Log
from labberwrapper.devices.SET import SET


@dataclass
class Piece(object):
    volts: float
    time_ns: float
    ramp_time_ns: Optional[float] = None
    length: Optional[int] = None


class Piecewise(object):

    def __init__(self, pieces, ramp_time_ns, repeat=1, resolution_ns=1):
        for i, piece in enumerate(pieces):
            assert isinstance(piece, Piece)
            if piece.ramp_time_ns is None and i != len(pieces) - 1:
                piece.ramp_time_ns = ramp_time_ns
            elif piece.ramp_time_ns is None and i == len(pieces) - 1:
                piece.ramp_time_ns = 0
            if piece.length is None:
                piece.length = floor((piece.time_ns + piece.ramp_time_ns) / resolution_ns)

        self._pieces = pieces
        self._ramp_time = ramp_time_ns
        self._piece_index = 0
        self._raster_index = 0
        self._repeat_index = 0
        self._repeat = repeat
        self.resolution = resolution_ns

        waveform_length = 0
        for i, piece in enumerate(pieces):
            if i != len(pieces) - 1:
                waveform_length += floor((piece.time_ns + piece.ramp_time_ns) / resolution_ns)
            else:
                waveform_length += floor(piece.time_ns / resolution_ns)

        self.length = waveform_length

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

    def __len__(self):
        return self.length * self._repeat

    def __iter__(self):
        return self

    def __next__(self):

        # conditionally move to next piece
        if self._piece_index < len(self._pieces) - 1 and self._raster_index == self._pieces[self._piece_index].length:
            self._piece_index += 1
            self._raster_index = 0

        # conditionally repeat the waveform from the start
        elif self._repeat_index < self._repeat - 1 and self._raster_index == self._pieces[self._piece_index].length and self._piece_index == len(self._pieces) - 1:
            self._repeat_index += 1
            self._piece_index = 0
            self._raster_index = 0

        # end the iteration when we finish the last piece
        elif self._repeat_index == self._repeat - 1 and self._piece_index == len(self._pieces) - 1 \
            and self._raster_index == self._pieces[self._piece_index].length:
            self._piece_index = 0
            self._raster_index = 0
            self._repeat_index = 0
            raise StopIteration

        # get the current piece
        piece = self._pieces[self._piece_index]

        # raster the piece
        if self._raster_index < floor(piece.time_ns / self.resolution):
            self._raster_index += 1
            return piece.volts

        # raster the ramp between pieces
        elif self._raster_index < floor(piece.time_ns / self.resolution) + floor(piece.ramp_time_ns / self.resolution):
            curr_raster = self._raster_index
            self._raster_index += 1

            # calculate the slope
            target = self._pieces[self._piece_index + 1].volts
            slope = (target - piece.volts) / floor(piece.ramp_time_ns / self.resolution)
            x = curr_raster - floor(piece.time_ns / self.resolution)

            # get the voltage at this instant
            y = slope * x + piece.volts
            return y


def software_piecewise_microwave(
    single_electron_transistor,
    piecewise,
    samples,
    records,
    averages,
    buffer_size,
    log_file='MW_TEST.hdf5',
    verbose=True
):
    # check for feasibility assuming this loop speed is limiting
    start = time.time()
    for i in range(100):
        pass
    stop = time.time()
    per_step = (stop - start) / 100

    if piecewise.resolution * 10e-9 < per_step:
        raise Exception('Piecewise signal resolution is beyond this computer\'s iteration speed.')

    # connect to server
    client = Labber.connectToServer('localhost')

    awg = KeysightPXIAWG(client)
    digitizer = KeysightPXIDigitizer(client)

    if verbose:
        # print AWG overview
        print(awg.instr.getLocalInitValuesDict())

        # print Digitizer overview
        print(digitizer.instr.getLocalInitValuesDict())

    volts = []
    for volt in piecewise:
        volts.append(volt)
    Vg1 = dict(name='Vg1', unit='V', values=volts)

    # initialize logging
    log = Log(
        log_file,
        'ai',
        'V',
        [Vg1]
    )

    reads = np.array([])

    digitizer.configure_acquisition(samples, records, averages, buffer_size)

    for volt in piecewise:
        awg.set_voltage(single_electron_transistor.bias_ch_num, volt)
        time.sleep(piecewise.resolution * 10e-9)
        values = digitizer.get_voltage(single_electron_transistor.ai_ch_num)
        reads = np.append(reads, values['y'].max())

    data = {'ai': reads}
    log.file.addEntry(data)

    digitizer.instr.stopInstrument()
    awg.instr.stopInstrument()

    # close connection
    client.close()


def hardware_piecewise_microwave(
    single_electron_transistor,
    piecewise,
    samples,
    records,
    averages,
    buffer_size,
    log_file='MW_HW_TEST.hdf5',
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

    volts = []
    for volt in piecewise:
        volts.append(volt)

    Vg1 = dict(name='Vg1', unit='V', values=volts)

    # initialize logging
    log = Log(
        log_file,
        'ai',
        'V',
        [Vg1]
    )

    results =np.array([])

    digitizer.configure_acquisition(samples, records, averages, buffer_size)

    # TODO: what is the resolution on this?
    awg.set_waveform(single_electron_transistor.bias_ch_num, volts)
    read = digitizer.get_voltage(single_electron_transistor.ai_ch_num)['y']

    time.sleep(piecewise.length * piecewise.resolution * 10e-9)

    bins = len(piecewise)
    bin_size = int(samples / bins)

    for i in range(bins):
        results = np.append(results, np.average(read[i * bin_size:(i + 1) * bin_size]))

    data = {'ai': results}
    log.file.addEntry(data)

    digitizer.instr.stopInstrument()
    awg.instr.stopInstrument()

    # close connection
    client.close()


# if __name__ == '__main__':
    # # define the SET to be measured
    # SET1 = SET(1)

    # # load the experiment config
    # config = json.load(open('../experiment_configs/mw_experiment.json', 'r'))
    # jschema_mw = json.load(open('../json_schemas/mw_experiment.json', 'r'))

    # # TODO: range safety checks should include checks for the min, max resolutions
    # # Do we want separate schemas for software and hardware implementations?
    # validate(instance=config, schema=jschema_mw)

    # # generate the waveform
    # software_piecewise_microwave(
    #     single_electron_transistor=SET1,
    #     piecewise=Piecewise(
    #         pieces=[
    #             Piece(volts=1, time_ns=10),
    #             Piece(volts=2, time_ns=10),
    #             Piece(volts=1, time_ns=10)
    #         ],
    #         ramp_time_ns=config['ramp_time']
    #     ),
    #     samples=config['samples'],
    #     records=config['records'],
    #     averages=config['averages'],
    #     buffer_size=config['buffer_size']
    # )

    # hardware_piecewise_microwave(
    #     single_electron_transistor=SET1,
    #     piecewise=Piecewise(
    #         pieces=[
    #             Piece(volts=1, time_ns=10),
    #             Piece(volts=2, time_ns=10),
    #             Piece(volts=1, time_ns=10)
    #         ],
    #         ramp_time_ns=config['ramp_time']
    #     ),
    #     samples=config['samples'],
    #     records=config['records'],
    #     averages=config['averages'],
    #     buffer_size=config['buffer_size']
    # )
