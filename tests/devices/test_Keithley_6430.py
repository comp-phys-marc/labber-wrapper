import Labber
import unittest
from unittest.mock import MagicMock
from ...devices.Keithley_6430 import Keithley6430


class TestKeithley6430(unittest.TestCase):

    def test_init(self):
        device = Keithley6430(Labber.connectToServer('localhost'))
        self.assertIsInstance(device, Keithley6430)
        assert hasattr(device, 'instr')
        self.assertIsNotNone(device.instr)

    def test_set_voltage(self):
        device = Keithley6430(Labber.connectToServer('localhost'))
        device.set_value = MagicMock()
        device.instr.setValue = MagicMock()

        # check that bad values are filtered out
        device.set_voltage('f')
        device.set_voltage(-3)
        device.set_voltage(3)

        device.instr.setValue.assert_not_called()

        # check that good values are set properly
        for v in [-2, -1, 0, 1, 2]:
            device.set_voltage(v)

            device.set_value.assert_called_with(device._keithley_src_status_key(), 'On')
            device.set_value.assert_called_with(device._keithley_src_func_key(), 'Voltage')
            device.set_value.assert_called_with(device._keithley_src_volt_key(), v)
            device.instr.setValue.assert_called_with(device._keithley_src_volt_key(), v)
