import Labber
import time

from labberwrapper.instruments.QDevil_QDAC import QDAC


def initialize(
    config,
    channel_generator_map,
):
    """
    Brings voltages up to configured values prior to another experiment.
    """

    # connect to instrument server
    client = Labber.connectToServer('localhost')

    # connect to instruments
    qdac = QDAC(client, channel_generator_map)

    # print QDAC overview
    print(qdac.instr.getLocalInitValuesDict())

    # ramp to initial voltages in 1 sec
    qdac.ramp_voltages(
        v_startlist=[],
        v_endlist=[
            config['bias_v'],
            config['plunger_v'],
            config['acc_v'],
            config['vb1_v'],
            config['vb2_v']
        ],
        ramp_time=1,
        repetitions=1,
        step_length=config['fast_step_size']
    )
    time.sleep(2)