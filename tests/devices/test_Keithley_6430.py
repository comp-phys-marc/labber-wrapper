import Labber
import unittest
from ...devices.Keithley_6430 import Keithley6430


class TestKeithley6430(unittest.TestCase):

    def test_init(self):
        device = Keithley6430(Labber.connectToServer('localhost'))
        self.assertIsInstance(device, Keithley6430)
        assert hasattr(device, 'instr')
        self.assertIsNotNone(device.instr)

    # TODO: mock device.set_value and assert that it is called with the correct key and value pairs
