import os
from pathlib import PurePath
from labberwrapper.instruments.BaseInstrument import BaseInstrument


class SRS830(BaseInstrument):

    @staticmethod
    def _SRS_lock_in_output_key():
        return 'Output amplitude'

    @staticmethod
    def _SRS_lock_in_reference_key():
        return 'Reference source'

    @staticmethod
    def _SRS_lock_in_frequency_key():
        return 'Frequency'
    
    @staticmethod
    def _SRS_lock_in_sensitivity_key():
        return 'Sensitivity'
    
    @staticmethod
    def _SRS_lock_in_time_constant_key():
        return 'Time constant'
    
    @staticmethod
    def _SRS_lock_in_slope_key():
        return 'Filter slope'
    
    def __init__(self, client):
        wd = PurePath(os.path.dirname(os.path.realpath(__file__))).parent
        file = open(PurePath(wd).joinpath("json_schemas/instrument_schemas/SRS_830.json"), "r")
        schema = ''.join(file.readlines())
        file.close()
        super().__init__(
            'Stanford Lock-in Amplifier SRS 830',
            dict(interface='GPIB', address='4'),
            client,
            schema
        )

    def set_output_and_readout(self, voltage, frequency, sensitivity, time_constant, slope, reference=1):
        self.instr.startInstrument()
        self.set_value(self._SRS_lock_in_output_key(), voltage)
        self.set_value(self._SRS_lock_in_reference_key(), reference) # 0 is external and 1 is internal
        self.set_value(self._SRS_lock_in_frequency_key(), frequency)
        self.set_value(self._SRS_lock_in_sensitivity_key(), sensitivity)
        self.set_value(self._SRS_lock_in_time_constant_key(), time_constant)
        self.set_value(self._SRS_lock_in_slope_key(), slope)

    def read(self, ch_id_1, ch_id_2):
        result_1 = self.instr.getValue(ch_id_1)
        result_2 = self.instr.getValue(ch_id_2)

        return result_1, result_2