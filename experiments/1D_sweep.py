import Labber
import numpy as np

from ..devices.NI_DAQ import NIDAQ
from ..devices.QDevil_QDAC import QDAC
from ..devices.SET import SET
from ..logging import Log

# connect to instrument server
client = Labber.connectToServer('localhost')

# connect to instruments
nidaq = NIDAQ(client)
qdac = QDAC(client)

# print QDAC overview
print(qdac.instr.getLocalInitValuesDict())

# preamp parameter
gain = 1e8

# NI_DAQ parameter
sample_rate_per_channel = 1e6  # Hz

I = dict(name='I', unit='A')
Vx = dict(name='Vx', unit='V')

# initialize logging
log = Log(
    "C:/Users/Measurement2/OneDrive/GroupShared/Data/QSim/20230530_measurement/TEST.hdf5",
    'Signal',
    'V',
    [I, Vx]
)

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

# voltage safety check
V_LIMIT = 2.5
if any(np.abs([SET1.bias_v, SET1.plunger_v, SET1.acc_v, SET1.vb1_v, SET1.vb2_v, SET1.fast_vend]) > V_LIMIT):
    raise Exception("Voltage too high")

# TODO: collect data and save to database