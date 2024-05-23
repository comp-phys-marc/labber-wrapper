import Labber
import unittest
from unittest.mock import MagicMock
from functools import partial
from labberwrapper.instruments.SRS_830 import SRS830


class TestSRS830(unittest.TestCase):

    def setUp(self):
        self.instrument = SRS830(Labber.connectToServer('localhost'))
        self.instrument.set_value = partial(self.instrument.set_value, validating=True)

    def test_init(self):
        self.assertIsInstance(self.instrument, SRS830)
        assert hasattr(self.instrument, 'instr')
        self.assertIsNotNone(self.instrument.instr)

    def test_set_voltage(self):
        self.instrument.set_value = MagicMock()
        self.instrument.instr.setValue = MagicMock()

        # check that bad values are filtered out
        self.instrument.set_output_and_readout(
            voltage=0.002, #minimum should be 0.004
            frequency=1000, 
            sensitivity=2, 
            time_constant=2, 
            slope=2
            )
        
        self.instrument.set_output_and_readout(
            voltage=0.004, 
            frequency=-1000, #should not put negative values 
            sensitivity=2, 
            time_constant=2, 
            slope=2
            )

        self.instrument.set_output_and_readout(
            voltage=0.004, 
            frequency=1000,  
            sensitivity='a', # should not accept a string
            time_constant=2, 
            slope=2
            )
        
        self.instrument.set_output_and_readout(
            voltage=0.004, 
            frequency=1000, 
            sensitivity=2, 
            time_constant=20, #maximum is 19
            slope=2
            )
        
        self.instrument.set_output_and_readout(
            voltage=0.004, 
            frequency=1000, 
            sensitivity=2, 
            time_constant=2,
            slope=4, #maximum should be 3
            )
        self.instrument.instr.setValue.assert_not_called()

        # check that good values are set properly
        for v in [0.004, 0.05]:
            for f in [0, 1000]:
                for s in [0, 26]:
                    for t in [0, 19]:
                        for slope in [0, 3]:
                            self.instrument.set_output_and_readout(v, f, s, t, slope)

                            self.instrument.set_value.assert_called_with(self._SRS_lock_in_output_key(), v)
                            self.instrument.set_value.assert_called_with(self._SRS_lock_in_frequency_key(), f)
                            self.instrument.set_value.assert_called_with(self._SRS_lock_in_sensitivity_key(), s)
                            self.instrument.set_value.assert_called_with(self._SRS_lock_in_time_constant_key(), t)
                            self.instrument.set_value.assert_called_with(self._SRS_lock_in_slope_key(), slope)
                            self.instrument.instr.setValue.assert_called_with(self.instrument._SRS_lock_in_output_key(), v)
                            self.instrument.instr.setValue.assert_called_with(self.instrument._SRS_lock_in_frequency_key(), f)
                            self.instrument.instr.setValue.assert_called_with(self.instrument._SRS_lock_in_sensitivity_key(), s)
                            self.instrument.instr.setValue.assert_called_with(self.instrument._SRS_lock_in_time_constant_key(), t)
                            self.instrument.instr.setValue.assert_called_with(self.instrument._SRS_lock_in_slope_key(), slope)