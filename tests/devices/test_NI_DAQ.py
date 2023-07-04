import Labber
import unittest
from ...devices.NI_DAQ import NIDAQ


class TestNIDAQ(unittest.TestCase):

    def test_init(self):
        device = NIDAQ(Labber.connectToServer('localhost'))
        self.assertIsInstance(device, NIDAQ)
        assert hasattr(device, 'instr')
        self.assertIsNotNone(device.instr)

    # TODO: mock device.set_value and assert that it is called with the correct key and value pairs
