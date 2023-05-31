import numpy as np
import time

class SET:
    def __init__(
            self,
            bias_ch_num: int,
            plunger_ch_num: int,
            acc_ch_num: int,
            vb1_ch_num: int,
            vb2_ch_num: int,
            ai_ch_num: str
    ):
        self.bias_ch_num = bias_ch_num
        self.plunger_ch_num = plunger_ch_num
        self.acc_ch_num = acc_ch_num
        self.vb1_ch_num = vb1_ch_num
        self.vb2_ch_num = vb2_ch_num
        self.bias_v = np.array([])
        self.plunger_v = np.array([])
        self.acc_v = np.array([])
        self.vb1_v = np.array([])
        self.vb2_v = np.array([])
        self.slow_ch = np.array([])
        self.fast_ch = np.array([])
        self.slow_vstart = np.array([])
        self.slow_vend = np.array([])
        self.slow_steps = np.array([])
        self.fast_vstart = np.array([])
        self.fast_vend = np.array([])
        self.fast_steps = np.array([])
        self.fast_step_size = np.array([])
        self.ai_ch_num = ai_ch_num

    def __repr__(self):
        return "SET()"

    def __str__(self):
        return f'SET(' \
               f'{self.bias_ch_num}, ' \
               f'{self.plunger_ch_num}, ' \
               f'{self.acc_ch_num}, ' \
               f'{self.vb1_ch_num}, ' \
               f'{self.vb2_ch_num}, ' \
               f'{self.ai_ch_num}' \
               f')'

    def sweep(self, qdac):
        time.sleep(0.01)  # it usually takes about 2 ms for setting up the NIDAQ tasks
        # qdac.channels[self.fast_ch[0]-1].sync(1)  TODO: use QDAC sync channels' labber config
        qdac.ramp_voltages(
            self.fast_ch,
            [self.fast_vstart for _ in range(len(self.fast_ch))],
            [self.fast_vend for _ in range(len(self.fast_ch))],
            self.fast_step_size * self.fast_steps
        )