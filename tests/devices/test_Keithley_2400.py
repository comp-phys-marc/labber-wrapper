import Labber
import unittest
from unittest.mock import MagicMock

from jsonschema import ValidationError

from ...devices.Keithley_2400 import Keithley2400


class TestKeithley2400(unittest.TestCase):

    def test_init(self):
        device = Keithley2400(Labber.connectToServer('localhost'))
        self.assertIsInstance(device, Keithley2400)
        assert hasattr(device, 'instr')
        self.assertIsNotNone(device.instr)

    def test_set_voltage(self):
        device = Keithley2400(Labber.connectToServer('localhost'))
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

            device.set_value.assert_called_with(device._keithley_src_status_key(), True)
            device.set_value.assert_called_with(device._keithley_src_func_key(), 'Voltage')
            device.set_value.assert_called_with(device._keithley_src_volt_key(), v)

