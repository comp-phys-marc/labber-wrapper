import Labber
import numpy as np
import time
import json

from labberwrapper.devices.NI_DAQ import NIDAQ
from labberwrapper.devices.Keithley import Keithley
from labberwrapper.devices.QDevil_QDAC import QDAC
from labberwrapper.devices.SET import SET
from labberwrapper.logging.log import Log

V_LIMIT = 2.5


def one_dimensional_sweep(
        single_e_transistor,
        config,
        channel_generator_map,
        gain=1e8,
        sample_rate_per_channel=1e6,
        v_min=-1,
        v_max=1
):

    # connect to instrument server
    client = Labber.connectToServer('localhost')

    # connect to instruments
    nidaq = NIDAQ(client)
    qdac = QDAC(client, channel_generator_map)
    keithley = Keithley(client)

    # print QDAC overview
    print(qdac.instr.getLocalInitValuesDict())

    # print Keithley overview
    print(keithley.instr.getLocalInitValuesDict())

    # ramp to initial voltages in 1 sec
    duration = qdac.ramp_voltages(
        v_startlist=[],
        v_endlist=[
            config['bias_volt']
        ],
        ramp_time=1,
        repetitions=1,
        step_length=config['fast_step_size']
    )
    time.sleep(duration + 0.2)

    # NI_DAQ parameters calculation
    num_samples_raw = int(config['fast_step_size'] * sample_rate_per_channel)

    vslow_list = np.linspace(config['slow_vstart'], config['slow_vend'], config['slow_steps'])

    # initialize logging
    log = Log(
        "C:/Users/Measurement2/OneDrive/GroupShared/Data/QSim/20230605_measurement/TEST3.hdf5",
        'NIai',
        'V',
        []
    )

    keithley.set_voltage(vslow_list[0])
    keithley.instr.startInstrument()

    for vslow in vslow_list[1:]:
        keithley.set_voltage(vslow)
        time.sleep(0.01)
        keith_cur = keithley.get_current()

        result = nidaq.read(
            ch_id=single_e_transistor.ai_ch_num,
            v_min=v_min,
            v_max=v_max,
            gain=gain,
            num_samples=num_samples_raw,
            sample_rate=sample_rate_per_channel
        )
        data = {'NIai': result, 'Vg1': vslow, 'Ig': keith_cur}
        log.file.addEntry(data)

    keithley.instr.stopInstrument()


if __name__ == '__main__':

    # define the SET to be measured
    SET1 = SET(9, 10, 11, 12, 13, "Dev2/ai0")  # TODO: get from config

    # load the experiment config
    config = json.load(open('../configs/1D_sweep.json', 'r'))

    # voltage safety check
    if any(np.abs([
                config['bias_v'],  # TODO: move out of config
                config['plunger_v'],
                config['acc_v'],
                config['vb1_v'],
                config['vb2_v'],
                config['fast_vend']
            ]) > V_LIMIT):
        raise Exception("Voltage too high")

    # perform the sweep
    one_dimensional_sweep(SET1, config, {
            SET1.bias_ch_num: 1,
            SET1.plunger_ch_num: 2,
            SET1.acc_ch_num: 3,
            SET1.vb1_ch_num: 4,
            SET1.vb2_ch_num: 5
        },
        v_min=-10,
        v_max=10
    )
