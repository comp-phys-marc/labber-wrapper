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
