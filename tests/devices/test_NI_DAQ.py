import Labber
import unittest
import numpy as np
from unittest.mock import MagicMock
from ...devices.NI_DAQ import NIDAQ


class TestNIDAQ(unittest.TestCase):

    def test_init(self):
        device = NIDAQ(Labber.connectToServer('localhost'))
        self.assertIsInstance(device, NIDAQ)
        assert hasattr(device, 'instr')
        self.assertIsNotNone(device.instr)

    def test_configure_read(self):
        device = NIDAQ(Labber.connectToServer('localhost'))
        device.instr.setValue = MagicMock()

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
            device.configure_read(**data)

            device.instr.setValue.assert_called_with(device._ni_num_sames_key, data['num_samples'])
            device.instr.setValue.assert_called_with(device._ni_sample_rate_key, data['sample_rate'])
            device.instr.setValue.assert_called_with(device._ni_enable_key(data['ch_id']), True)
            device.instr.setValue.assert_called_with(device._ni_high_range_key(data['ch_id']), data['v_max'])
            device.instr.setValue.assert_called_with(device._ni_low_range_key(data['ch_id']), data['v_min'])

            if data['trigger'] is not None:
                device.instr.setValue.assert_called_with(device._ni_trig_key, data['trigger'])

    def test_read(self):
        device = NIDAQ(Labber.connectToServer('localhost'))

        for (ch_id, gain) in [(0, 1e8), (1, 2e6), (8, -3e5)]:
            device.instr.getValue = MagicMock(return_value={'y': np.array([i for i in range(ch_id)])})

            res = device.read(ch_id, gain)

            device.instr.getValue.assert_called_with(device._ni_data_key(ch_id))
            self.assertEqual(res, device.instr.getValue(device._ni_data_key(ch_id))['y'] / gain)