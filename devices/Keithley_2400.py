from .BaseDevice import BaseDevice


class Keithley2400(BaseDevice):

    @staticmethod
    def _keithley_src_status_key():
        return 'Output on'

    @staticmethod
    def _keithley_src_func_key():
        return 'Source type'

    @staticmethod
    def _keithley_src_volt_key():
        return 'Source voltage'

    def __init__(self, client):
        schema = open("json_schemas/Keithley_2400_SourceMeter.json", "r").readlines()
        super().__init__('Keithley 2400 SourceMeter', dict(interface='GPIB', address='2'), client, schema)

    def set_voltage(self, voltage):
        self.instr.startInstrument()
        self.instr.setValue(self._keithley_src_status_key(), True)
        self.instr.setValue(self._keithley_src_func_key(), 'Voltage')
        self.instr.setValue(self._keithley_src_volt_key(), voltage)

