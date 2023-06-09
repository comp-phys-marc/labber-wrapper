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


# TODO: debug on lab computer
def keithley_sweep(
        single_e_transistor,
        config,
        channel_generator_map,
        gain=1,
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
        step_length=config['step_length']
    )
    time.sleep(duration + 0.2)

    # NI_DAQ parameters calculation
    num_samples_raw = int(config['step_length'] * sample_rate_per_channel)

    vslow_list = np.linspace(config['slow_vstart'], config['slow_vend'], config['slow_steps'])

    # initialize logging
    log = Log(
        "TEST3.hdf5",
        'NIai',
        'V',
        []
    )

    keithley.set_voltage(vslow_list[0])
    keithley.instr.startInstrument()

    for vslow in vslow_list[1:]:
        keithley.set_voltage(vslow)
        time.sleep(config['step_length'])
        keith_cur = keithley.get_current()

        result = nidaq.read(
            ch_id=single_e_transistor.ai_ch_num,
            v_min=v_min,
            v_max=v_max,
            gain=gain,
            num_samples=num_samples_raw,
            sample_rate=sample_rate_per_channel
        )
        data = {'NIai': np.average(result), 'Vg1': vslow, 'Ig': keith_cur}
        log.file.addEntry(data)

    keithley.instr.stopInstrument()


if __name__ == '__main__':

    # define the SET to be measured
    dev_config = json.load(open('../device_configs/SET.json', 'r'))
    SET1 = SET(dev_config["bias_ch_num"])

    # load the experiment config
    config = json.load(open('../configs/keithley_sweep.json', 'r'))

    # voltage safety check
    if  config['bias_volt'] > V_LIMIT:
        raise Exception("Voltage too high")

    # perform the sweep
    keithley_sweep(SET1, config, {
            SET1.bias_ch_num: 1
        },
        v_min=-10,
        v_max=10,
        sample_rate_per_channel=1e3
    )
