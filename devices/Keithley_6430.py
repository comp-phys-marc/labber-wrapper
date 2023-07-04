from .BaseDevice import BaseDevice


class Keithley6430(BaseDevice):

    @staticmethod
    def _keithley_src_status_key():
        return 'Source on_off'

    @staticmethod
    def _keithley_src_func_key():
        return 'Source function'

    @staticmethod
    def _keithley_src_volt_key():
        return 'Voltage Amplitude'

    @staticmethod
    def _keithley_measured_curr_key():
        return 'Measured current'

    def __init__(self, client):
        schema = open("json_schemas/Keithley_6430_SourceMeter.json", "r").readlines()
        super().__init__('Keithley 6430 Source Measurement Unit', dict(interface='GPIB', address='2'), client, schema)

    def set_voltage(self, voltage):
        self.instr.startInstrument()
        self.set_value(self._keithley_src_status_key(), 'On')
        self.set_value(self._keithley_src_func_key(), 'Voltage')
        self.set_value(self._keithley_src_volt_key(), voltage)

