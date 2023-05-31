import Labber
import numpy as np

from ..devices.NI_DAQ import NIDAQ
from ..devices.QDevil_QDAC import QDAC
from ..devices.SET import SET
from ..logging import Log

V_LIMIT = 2.5


def one_dimensional_sweep(single_e_transistor, gain=1e8, sample_rate_per_channel=1e6):

    # connect to instrument server
    client = Labber.connectToServer('localhost')

    # connect to instruments
    nidaq = NIDAQ(client)
    qdac = QDAC(client)

    # print QDAC overview
    print(qdac.instr.getLocalInitValuesDict())

    I = dict(name='I', unit='A')
    Vx = dict(name='Vx', unit='V')

    # initialize logging
    log = Log(
        "C:/Users/Measurement2/OneDrive/GroupShared/Data/QSim/20230530_measurement/TEST.hdf5",
        'Signal',
        'V',
        [I, Vx]
    )

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

    # TODO: collect data and save to database


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

    one_dimensional_sweep(SET1)
