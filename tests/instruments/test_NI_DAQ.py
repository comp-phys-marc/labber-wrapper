import Labber
import unittest
import numpy as np
from functools import partial
from unittest.mock import MagicMock
from instruments.NI_DAQ import NIDAQ


class TestNIDAQ(unittest.TestCase):

    def setUp(self):
        self.instrument = NIDAQ(Labber.connectToServer('localhost'))
        self.instrument.set_value = partial(self.instrument.set_value, validating=True)

    def test_init(self):
        self.assertIsInstance(self.instrument, NIDAQ)
        assert hasattr(self.instrument, 'instr')
        self.assertIsNotNone(self.instrument.instr)

    def test_configure_read(self):
        self.instrument.instr.setValue = MagicMock()

        cases = [
            dict(
                ch_id=0,
                num_samples=1,
                sample_rate=10e3,
                v_min=-10,
                v_max=10,
                trigger='Immediate'
            ),
            dict(
                ch_id=1,
                num_samples=10,
                sample_rate=10e6,
                v_min=-5,
                v_max=5,
                trigger='Channel 1'
            ),
            dict(
                ch_id=2,
                num_samples=100,
                sample_rate=10e5,
                v_min=-2,
                v_max=2,
                trigger=None
            )
        ]

        for data in cases:
            self.instrument.configure_read(**data)

            self.instrument.instr.setValue.assert_called_with(self.instrument._ni_num_sames_key, data['num_samples'])
            self.instrument.instr.setValue.assert_called_with(self.instrument._ni_sample_rate_key, data['sample_rate'])
            self.instrument.instr.setValue.assert_called_with(self.instrument._ni_enable_key(data['ch_id']), True)
            self.instrument.instr.setValue.assert_called_with(self.instrument._ni_high_range_key(data['ch_id']), data['v_max'])
            self.instrument.instr.setValue.assert_called_with(self.instrument._ni_low_range_key(data['ch_id']), data['v_min'])

            if data['trigger'] is not None:
                self.instrument.instr.setValue.assert_called_with(self.instrument._ni_trig_key, data['trigger'])

    def test_read(self):

        for (ch_id, gain) in [(0, 1e8), (1, 2e6), (8, -3e5)]:
            self.instrument.instr.getValue = MagicMock(return_value={'y': np.array([i for i in range(ch_id)])})

            res = self.instrument.read(ch_id, gain)

            self.device.instr.getValue.assert_called_with(self.device._ni_data_key(ch_id))
            np.testing.assert_array_equal(res, self.device.instr.getValue(self.device._ni_data_key(ch_id))['y'] / gain)