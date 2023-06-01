import Labber
import numpy as np
import time

from ..devices.NI_DAQ import NIDAQ
from ..devices.QDevil_QDAC import QDAC
from ..devices.SET import SET
from ..logging import Log

V_LIMIT = 2.5


def one_dimensional_sweep(single_e_transistor, channel_generator_map, gain=1e8, sample_rate_per_channel=1e6):

    # connect to instrument server
    client = Labber.connectToServer('localhost')

    # connect to instruments
    nidaq = NIDAQ(client)
    qdac = QDAC(client, channel_generator_map)

    # print QDAC overview
    print(qdac.instr.getLocalInitValuesDict())

    # voltage safety check
    if any(np.abs([
                single_e_transistor.bias_v,
                single_e_transistor.plunger_v,
                single_e_transistor.acc_v,
                single_e_transistor.vb1_v,
                single_e_transistor.vb2_v,
                single_e_transistor.fast_vend
            ]) > V_LIMIT):
        raise Exception("Voltage too high")

    # ramp to initial voltages in 1 sec
    qdac.ramp_voltages(
        v_startlist=[],
        v_endlist=[
            single_e_transistor.bias_v,
            single_e_transistor.plunger_v,
            single_e_transistor.acc_v,
            single_e_transistor.vb1_v,
            single_e_transistor.vb2_v
        ],
        ramp_time=1,
        repetitions=1,
        step_length=single_e_transistor.fast_step_size
    )
    time.sleep(2)

    # NI_DAQ parameters calculation
    num_samples_raw = int(single_e_transistor.fast_step_size * sample_rate_per_channel)

    # collect data and save to database
    start_time = time.time()

    vfast_list = np.linspace(SET1.fast_vstart, SET1.fast_vend, SET1.fast_steps)
    Vx = dict(name='Vx', unit='V', values=vfast_list)

    # initialize logging
    log = Log(
        "C:/Users/Measurement2/OneDrive/GroupShared/Data/QSim/20230530_measurement/TEST.hdf5",
        'I',
        'A',
        [Vx]
    )

    for vfast in np.linspace(SET1.fast_vstart, SET1.fast_vend, SET1.fast_steps):
        qdac.ramp_voltages(
            v_startlist=[],
            v_endlist=[vfast for _ in range(len(SET1.fast_ch))],
            ramp_time=0.005,
            repetitions=1,
            step_length=single_e_transistor.fast_step_size
        )
        time.sleep(0.005)
        result = nidaq.read(
            ch_id=SET1.ai_ch_num,
            v_min=-1,
            v_max=1,
            gain=gain,
            num_samples=num_samples_raw,
            sample_rate=sample_rate_per_channel
        )
        data = {'I': result}
        log.file.addEntry(data)

    end_time = time.time()
    print(f'Time elapsed: {np.round(end_time - start_time, 2)} sec.')


if __name__ == '__main__':

    # define the SET to be measured
    SET1 = SET(9, 10, 11, 12, 13, "Dev2/ai0")

    # setup sweep parameters
    SET1.fast_ch = [SET1.acc_ch_num]
    SET1.fast_vstart = -1.7  # V
    SET1.fast_vend = -2.4
    SET1.fast_steps = 100
    SET1.fast_step_size = 0.050  # sec

    # initial voltages in volts before sweep starts
    SET1.bias_v = -10e-6
    SET1.plunger_v = 0
    SET1.acc_v = SET1.fast_vstart
    SET1.vb1_v = 0
    SET1.vb2_v = 0

    one_dimensional_sweep(SET1, {
        SET1.bias_ch_num: 1,
        SET1.plunger_ch_num: 2,
        SET1.acc_ch_num: 3,
        SET1.vb1_ch_num: 4,
        SET1.vb2_ch_num: 5
    })
