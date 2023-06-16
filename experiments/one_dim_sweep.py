import Labber
import numpy as np
import time
import json

from labberwrapper.devices.NI_DAQ import NIDAQ
from labberwrapper.devices.QDevil_QDAC import QDAC
from labberwrapper.devices.SET import SET
from labberwrapper.logging.log import Log


# TODO: add one_dimensional_sweep_hardware
def one_dimensional_sweep(
        single_e_transistor,
        fast_ch,
        fast_vstart,
        fast_vend,
        fast_steps,
        fast_step_size,
        fast_ch_name,
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

    # print QDAC overview
    print(qdac.instr.getLocalInitValuesDict())

    # NI_DAQ parameters calculation
    num_samples_raw = int(fast_step_size * sample_rate_per_channel)

    # collect data and save to database
    start_time = time.time()

    vfast_list = np.linspace(fast_vstart, fast_vend, fast_steps)
    Vx = dict(name=fast_ch_name, unit='V', values=vfast_list)

    # initialize logging
    log = Log(
        "TEST.hdf5",
        'I',
        'A',
        [Vx]
    )

    fast_ramp_mapping = {}
    results = np.array([])

    for i in range(len(fast_ch)):
        fast_ramp_mapping[fast_ch[i]] = channel_generator_map[fast_ch[i]]

    # TODO: call ramp_voltages_software once and remove this outer loop
    for vfast in vfast_list:
        fast_qdac = QDAC(client, fast_ramp_mapping)
        fast_qdac.ramp_voltages_software(
            v_startlist=[],
            v_endlist=[vfast for _ in range(len(fast_ch))],
            ramp_time=0.005,
            repetitions=1,
            step_length=fast_step_size
        )
        time.sleep(0.005)
        result = nidaq.read(
            ch_id=single_e_transistor.ai_ch_num,
            v_min=v_min,
            v_max=v_max,
            gain=gain,
            num_samples=num_samples_raw,
            sample_rate=sample_rate_per_channel
        )
        results = np.append(results, np.average(result))
    data = {'I': results}
    log.file.addEntry(data)

    qdac.instr.stopInstrument()
    fast_qdac.instr.stopInstrument()

    end_time = time.time()
    print(f'Time elapsed: {np.round(end_time - start_time, 2)} sec.')


if __name__ == '__main__':

    # define the SET to be measured
    config = json.load(open('../configs/1D_sweep.json', 'r'))
    dev_config = json.load(open('../device_configs/SET.json', 'r'))
    SET1 = SET(dev_config["bias_ch_num"],
               dev_config["plunger_ch_num"],
               dev_config["acc_ch_num"],
               dev_config["vb1_ch_num"],
               dev_config["vb2_ch_num"],
               dev_config["ai_ch_num"]) 

    # perform the sweep
    one_dimensional_sweep(SET1,
                          config["fast_ch"],
                          config["fast_vstart"],
                          config["fast_vend"],
                          config["fast_steps"],
                          config["fast_step_size"],
                          config["fast_ch_name"],
                          {SET1.bias_ch_num: 1,
                          SET1.plunger_ch_num: 2,
                          SET1.acc_ch_num: 3,
                          SET1.vb1_ch_num: 4,
                          SET1.vb2_ch_num: 5})