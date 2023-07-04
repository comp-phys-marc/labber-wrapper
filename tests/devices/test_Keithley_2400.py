import Labber
import unittest
from ...devices.Keithley_2400 import Keithley2400


class TestKeithley2400(unittest.TestCase):

    def test_init(self):
        device = Keithley2400(Labber.connectToServer('localhost'))
        self.assertIsInstance(device, Keithley2400)
        assert hasattr(device, 'instr')
        self.assertIsNotNone(device.instr)

    # TODO: mock device.set_value and assert that it is called with the correct key and value pairs
