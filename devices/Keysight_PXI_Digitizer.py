

class KeysightPXIDigitizer:

    @staticmethod
    def _keysight_signal_key(channel):
        return f'Ch{channel} - Signal'

    @staticmethod
    def _keysight_number_of_samples_key():
        return 'Number of samples'

    @staticmethod
    def _keysight_number_of_records_key():
        return 'Number of records'

    @staticmethod
    def _keysight_number_of_averages_key():
        return 'Number of averages'

    @staticmethod
    def _keysight_records_per_buffer_key():
        return 'Records per Buffer'

    def __init__(self, client):
        self.instr = client.connectToInstrument('Keysight PXI Digitizer', dict(interface='PXI', address='3'))

    def configure_acquisition(self, samples, records, averages, buffer_size):
        self.instr.startInstrument()
        self.instr.setValue(self._keysight_number_of_samples_key(), samples)
        self.instr.setValue(self._keysight_number_of_records_key(), records)
        self.instr.setValue(self._keysight_number_of_averages_key(), averages)
        self.instr.setValue(self._keysight_records_per_buffer_key(), buffer_size)

    def get_voltage(self, channel):
        self.instr.startInstrument()
        self.instr.setValue(self._keysight_signal_key(channel))
