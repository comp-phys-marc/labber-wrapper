import Labber
import numpy as np
import time
import json
from jsonschema import validate

from labberwrapper.devices.Keithley_2400 import Keithley2400
from labberwrapper.devices.SRS_830 import SRS830
from labberwrapper.logging.log import Log

import matplotlib
import matplotlib.pyplot as plt

def gate_sweep(
    gate_start,
    gate_end,
    gate_steps,
    voltage, 
    frequency, 
    sensitivity, 
    time_constant, 
    slope,
    ch_id_1, 
    ch_id_2,
    step_length,  # need to calculate (5 times the time constant we set)
    log_file='TEST.hdf5',
    verbose=True
):

    # connect to instrument server
    client = Labber.connectToServer('localhost')

    # connect to instruments
    lock_in = SRS830(client)
    keithley = Keithley2400(client)

    if verbose:
        # print Lock_in overview
        print(lock_in.instr.getLocalInitValuesDict())

        # print Keithley overview
        print(keithley.instr.getLocalInitValuesDict())

    lock_in.set_output_and_readout(
        voltage=voltage, 
        frequency=frequency, 
        sensitivity=sensitivity, 
        time_constant=time_constant, 
        slope=slope,
    )

    gate_voltage_list = np.linspace(gate_start, gate_end, gate_steps)
    Vg1 = dict(name='Vg1', unit='V', values=gate_voltage_list)

    # initialize logging
    log = Log(
        log_file,
        [
            dict(name='R', units='A'),
            dict(name='theta', units='rad'),
        ],
        [Vg1]
    )

    r_results = []
    theta_results = []
    for gate_volt in gate_voltage_list:
        keithley.set_voltage(gate_volt)
        time.sleep(step_length)  

        result = lock_in.read(ch_id_1=ch_id_1, ch_id_2=ch_id_2)
        r_results.append(result[0])
        theta_results.append(result[1])

    data = {
        'R': np.array(r_results),
        'theta': np.array(theta_results)
    }
    log.file.addEntry(data)


if __name__ == '__main__':
    # load the experiment config

    # voltage safety check
    config = json.load(open('../experiment_configs/lock_in_keithley_gating_oussama.json', 'r'))
    schem = json.load(open('../json_schemas/experiment_schemas/lock_in_keithley_gating_oussama.json', 'r'))

    validate(instance=config, schema=schem)

    # perform the sweep
    gate_sweep(
        config['gate_start'],
        config['gate_end'],
        config['gate_steps'],
        config['voltage'], 
        config['frequency'],
        config['sensitivity'], 
        config['time_constant'], 
        config['slope'],
        config['ch_id_1'], 
        config['ch_id_2'],
        config['step_length'],
        log_file='TEST.hdf5'
    )