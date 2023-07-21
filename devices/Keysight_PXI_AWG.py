

class KeysightPXIAWG:

    @staticmethod
    def _keysight_offset_key(channel):
        return f'Ch{channel} - Offset'

    def __init__(self, client):
        self.instr = client.connectToInstrument('Keysight PXI AWG', dict(interface='PXI', address='4'))

    def set_voltage(self, channel, voltage):
        self.instr.startInstrument()
        self.instr.setValue(self._keysight_offset_key(channel), voltage)
