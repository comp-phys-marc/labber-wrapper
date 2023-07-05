import Labber
import numpy as np
import time
import json

from labberwrapper.devices.NI_DAQ import NIDAQ
from devices.Keithley_6430 import Keithley6430
from labberwrapper.devices.QDevil_QDAC import QDAC
from labberwrapper.devices.SET import SET
from labberwrapper.logging.log import Log
from jsonschema import validate

def keithley_sweep(
        single_e_transistor,
        slow_vstart,
        slow_vend,
        slow_steps,
        step_length,
        gain=1e8,
        sample_rate_per_channel=1e6,
        v_min=-1,
        v_max=1,
        log_file='TEST.hdf5',
        verbose=True
):

    # connect to instrument server
    client = Labber.connectToServer('localhost')

    # connect to instruments
    nidaq = NIDAQ(client)
    keithley = Keithley6430(client)

    if verbose:
        # print NIDAQ overview
        print(nidaq.instr.getLocalInitValuesDict())

        # print Keithley overview
        print(keithley.instr.getLocalInitValuesDict())

    # NI_DAQ parameters calculation
    num_samples_raw = int(step_length * sample_rate_per_channel)

    vslow_list = np.linspace(slow_vstart, slow_vend, slow_steps)

    # initialize logging
    log = Log(
        log_file,
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

    config = json.load(open('../configs/keithley_sweep.json', 'r'))
    dev_config = json.load(open('../device_configs/SET.json', 'r'))

    # define the SET to be measured
   SET1 = SET(dev_config["bias_ch_num"],
              dev_config["plunger_ch_num"],
              dev_config["acc_ch_num"],
              dev_config["vb1_ch_num"],
              dev_config["vb2_ch_num"],
              dev_config["ai_ch_num"])
    # load the experiment config
    config = json.load(open('../configs/1D_sweep.json', 'r'))
    jschema_Sweep = json.load(open('../json_schemas/keithley_sweep.json', 'r'))
    jschema_dev = json.load(open('../json_schemas/SET.json', 'r'))

    # voltage safety check
    validate(instance=config, schema=jschema_sweep)
    validate(instance = dev_config, schema = jschema_dev) 

    # perform the sweep
    keithley_sweep(
        SET1,
        config[bias_volt],
        config[bias_ch_num],
        config[slow_vstart],
        config[slow_vend],
        config[slow_steps],
        config[step_length],
        v_min=-10,
        v_max=10,
        sample_rate_per_channel=1e3
    )