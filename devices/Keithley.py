

class Keithley:

    @staticmethod
    def _keithley_src_status_key():
        return 'Source status'

    @staticmethod
    def _keithley_src_func_key():
        return 'Source function'

    @staticmethod
    def _keithley_src_volt_key():
        return 'Source voltage'

    @staticmethod
    def _keithley_measured_curr_key():
        return 'Measured current'

    def __init__(self, client):
        self.instr = client.connectToInstrument('Keithley', dict(interface='GPIB', address='GPIB0::02::INSTR'))

    def set_voltage(self, voltage):
        self.instr.setValue(self._keithley_src_status_key(), 'On')
        self.instr.setValue(self._keithley_src_func_key(), 'Voltage')
        self.instr.setValue(self._keithley_src_volt_key(), voltage)

    def get_current(self):
        return self.instr.getValue(self._keithley_measured_curr_key())
