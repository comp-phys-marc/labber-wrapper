import Labber
import numpy as np
import time
import json

from ..devices.NI_DAQ import NIDAQ
from ..devices.QDevil_QDAC import QDAC
from ..devices.SET import SET
from ..logging import Log
from jsonschema import validate


V_LIMIT = 2.5


def one_dimensional_sweep(
        single_e_transistor,
        fast_ch,
        bias_v,
        plunger_v,
        acc_v,
        vb1_v,
        vb2_v,
        fast_vstart,
        fast_vend,
        fast_steps,
        fast_step_size,
        fast_ch_name,
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

    # print QDAC overview
    print(qdac.instr.getLocalInitValuesDict())

    # ramp to initial voltages in 1 sec
    qdac.ramp_voltages(
        v_startlist=[],
        v_endlist=[
            bias_v,
            plunger_v,
            acc_v,
            vb1_v,
            vb2_v
        ],
        ramp_time=1,
        repetitions=1,
        step_length=fast_step_size
    )
    time.sleep(2)

    # NI_DAQ parameters calculation
    num_samples_raw = int(fast_step_size * sample_rate_per_channel)

    # collect data and save to database
    start_time = time.time()

    vfast_list = np.linspace(fast_vstart, fast_vend, fast_steps)
    Vx = dict(name=fast_ch_name, unit='V', values=vfast_list)

    # initialize logging
    log = Log(
        "C:/Users/Measurement1/OneDrive/GroupShared/Data/QSim/20230530_measurement/TEST.hdf5",
        'I',
        'A',
        [Vx]
    )

    for vfast in vfast_list:
        qdac.ramp_voltages(
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
        data = {'I': result}
        log.file.addEntry(data)

    end_time = time.time()
    print(f'Time elapsed: {np.round(end_time - start_time, 2)} sec.')


if __name__ == '__main__':

    # define the SET to be measured

    dev_config = json.load(open('../device_configs/SET.json', 'r'))
    SET1 = SET(bias_ch_num,
               plunger_ch_num,
               acc_ch_num,
               vb1_ch_num,
               vb2_ch_num,
               ai_ch_num) 

    # load the experiment config
    config = json.load(open('../configs/1D_sweep.json', 'r'))
    jschema = json.load(open('../json_schemas/1d_&_2Dsweeps.json', 'r'))

    # voltage safety check
    validate(instance=config, schema=jschema)  
    
    # old code - validation not using jsonschemas. # TODO: delete once sure of schema validation
     #if any(np.abs([
     #           config['bias_v'],  # TODO: move out of config
     #           config['plunger_v'],
     #           config['acc_v'],
     #           config['vb1_v'],
     #           config['vb2_v'],
     #           config['fast_vend']
     #           ]) > V_LIMIT):
     #    raise Exception("Voltage too high")

    # perform the sweep
    one_dimensional_sweep(SET1,
                          config["fast_ch"],
                          config[bias_v],
                          config[plunger_v],
                          config[acc_v],
                          config[vb1_v],
                          config[vb2_v],
                          config[fast_vstart],
                          config[fast_vend],
                          config[fast_steps],
                          config[fast_step_size],
                          config[fast_ch_name],
                          {SET1.bias_ch_num: 1,
                          SET1.plunger_ch_num: 2,
                          SET1.acc_ch_num: 3,
                          SET1.vb1_ch_num: 4,
                          SET1.vb2_ch_num: 5})