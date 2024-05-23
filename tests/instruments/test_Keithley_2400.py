import Labber
import unittest
from unittest.mock import MagicMock
from functools import partial
from instruments.Keithley_2400 import Keithley2400


class TestKeithley2400(unittest.TestCase):

    def setUp(self):
        self.instrument = Keithley2400(Labber.connectToServer('localhost'))
        self.instrument.set_value = partial(self.instrument.set_value, validating=True)

    def test_init(self):
        self.assertIsInstance(self.instrument, Keithley2400)
        assert hasattr(self.instrument, 'instr')
        self.assertIsNotNone(self.instrument.instr)

    def test_set_voltage(self):
        self.instrument.set_value = MagicMock()
        self.instrument.instr.setValue = MagicMock()

        # check that bad values are filtered out
        self.instrument.set_voltage('f')
        self.instrument.set_voltage(-3)
        self.instrument.set_voltage(3)

        self.instrument.instr.setValue.assert_not_called()

        # check that good values are set properly
        for v in [-2, -1, 0, 1, 2]:
            self.instrument.set_voltage(v)

            self.instrument.set_value.assert_called_with(self.instrument._keithley_src_status_key(), True)
            self.instrument.set_value.assert_called_with(self.instrument._keithley_src_func_key(), 'Voltage')
            self.instrument.set_value.assert_called_with(self.instrument._keithley_src_volt_key(), v)
            self.instrument.instr.setValue.assert_called_with(self.instrument._keithley_src_volt_key(), v)


