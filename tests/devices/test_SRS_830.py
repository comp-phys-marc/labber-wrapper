import Labber
import unittest
from unittest.mock import MagicMock
from functools import partial
from devices.SRS_830 import SRS830


class TestSRS830(unittest.TestCase):

    def setUp(self):
        self.device = SRS830(Labber.connectToServer('localhost'))
        self.device.set_value = partial(self.device.set_value, validating=True)

    def test_init(self):
        self.assertIsInstance(self.device, SRS830)
        assert hasattr(self.device, 'instr')
        self.assertIsNotNone(self.device.instr)

    def test_set_voltage(self):
        self.device.set_value = MagicMock()
        self.device.instr.setValue = MagicMock()

        # check that bad values are filtered out
        self.device.set_output_and_readout(
            voltage=0.002, #minimum should be 0.004
            frequency=1000, 
            sensitivity=2, 
            time_constant=2, 
            slope=2
            )
        
        self.device.set_output_and_readout(
            voltage=0.004, 
            frequency=-1000, #should not put negative values 
            sensitivity=2, 
            time_constant=2, 
            slope=2
            )

        self.device.set_output_and_readout(
            voltage=0.004, 
            frequency=1000,  
            sensitivity='a', # should not accept a string
            time_constant=2, 
            slope=2
            )
        
        self.device.set_output_and_readout(
            voltage=0.004, 
            frequency=1000, 
            sensitivity=2, 
            time_constant=20, #maximum is 19
            slope=2
            )
        
        self.device.set_output_and_readout(
            voltage=0.004, 
            frequency=1000, 
            sensitivity=2, 
            time_constant=2,
            slope=4, #maximum should be 3
            )
        self.device.instr.setValue.assert_not_called()

        # check that good values are set properly
        for v in [0.004, 0.05]:
            for f in [0, 1000]:
                for s in [0, 26]:
                    for t in [0, 19]:
                        for slope in [0, 3]:
                            self.device.set_output_and_readout(v, f, s, t, slope)

                            self.device.set_value.assert_called_with(self._SRS_lock_in_output_key(), v)
                            self.device.set_value.assert_called_with(self._SRS_lock_in_frequency_key(), f)
                            self.device.set_value.assert_called_with(self._SRS_lock_in_sensitivity_key(), s)
                            self.device.set_value.assert_called_with(self._SRS_lock_in_time_constant_key(), t)
                            self.device.set_value.assert_called_with(self._SRS_lock_in_slope_key(), slope)
                            self.device.instr.setValue.assert_called_with(self.device._SRS_lock_in_output_key(), v)
                            self.device.instr.setValue.assert_called_with(self.device._SRS_lock_in_frequency_key(), f)
                            self.device.instr.setValue.assert_called_with(self.device._SRS_lock_in_sensitivity_key(), s)
                            self.device.instr.setValue.assert_called_with(self.device._SRS_lock_in_time_constant_key(), t)
                            self.device.instr.setValue.assert_called_with(self.device._SRS_lock_in_slope_key(), slope)