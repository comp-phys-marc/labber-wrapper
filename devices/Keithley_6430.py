

class Keithley6430:

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
        self.instr = client.connectToInstrument('Keithley 6430 Source Measurement Unit', dict(interface='GPIB', address='2'))

    def set_voltage(self, voltage):
        self.instr.startInstrument()
        self.instr.setValue(self._keithley_src_status_key(), 'On')
        self.instr.setValue(self._keithley_src_func_key(), 'Voltage')
        self.instr.setValue(self._keithley_src_volt_key(), voltage)

