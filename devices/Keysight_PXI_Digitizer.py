

class KeysightPXIDigitizer:

    @staticmethod
    def _keysight_signal_key(channel):
        return f'Ch{channel} - Signal'

    def __init__(self, client):
        self.instr = client.connectToInstrument('Keysight PXI Digitizer', dict(interface='PXI', address='3'))

    def get_voltage(self, channel):
        self.instr.startInstrument()
        self.instr.setValue(self._keysight_signal_key(channel))
