import Labber
import unittest
from unittest.mock import MagicMock
from functools import partial
from labberwrapper.instruments.Keithley_6430 import Keithley6430


class TestKeithley6430(unittest.TestCase):

    def setUp(self):
        self.instrument = Keithley6430(Labber.connectToServer('localhost'))
        self.instrument.set_value = partial(self.instrument.set_value, validating=True)

    def test_init(self):
        self.assertIsInstance(self.instrument, Keithley6430)
        assert hasattr(self.instrument, 'instr')
        self.assertIsNotNone(self.instrument.instr)

    def test_set_voltage(self):
        self.instrument.set_value = MagicMock()
        self.instrument.instr.setValue = MagicMock()

        # check that bad values are filtered out
        self.device.set_voltage('f')
        self.device.set_voltage(-3)
        self.device.set_voltage(3)

        self.device.instr.setValue.assert_not_called()

        # check that good values are set properly
        for v in [-2, -1, 0, 1, 2]:
            self.device.set_voltage(v)

            self.device.set_value.assert_called_with(self.device._keithley_src_status_key(), 'On')
            self.device.set_value.assert_called_with(self.device._keithley_src_func_key(), 'Voltage')
            self.device.set_value.assert_called_with(self.device._keithley_src_volt_key(), v)
            self.device.instr.setValue.assert_called_with(self.device._keithley_src_volt_key(), v)
