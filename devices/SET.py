import time
from dataclasses import dataclass


@dataclass
class SET:
    bias_ch_num: int
    plunger_ch_num: int
    acc_ch_num: int
    vb1_ch_num: int
    vb2_ch_num: int
    ai_ch_num: str

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'SET(' \
               f'{self.bias_ch_num}, ' \
               f'{self.plunger_ch_num}, ' \
               f'{self.acc_ch_num}, ' \
               f'{self.vb1_ch_num}, ' \
               f'{self.vb2_ch_num}, ' \
               f'{self.ai_ch_num}' \
               f')'

    def sweep(self, qdac, config):
        time.sleep(0.01)  # it usually takes about 2 ms for setting up the NIDAQ tasks
        qdac.sync(1, config['fast_ch'][0])
        qdac.ramp_voltages(
            v_startlist=[config['fast_vstart'] for _ in range(len(config['fast_ch']))],
            v_endlist=[config['fast_vend'] for _ in range(len(config['fast_ch']))],
            ramp_time=config['fast_step_size'] * config['fast_steps'],
            step_length=config['fast_step_size'],
            repetitions=1
        )
