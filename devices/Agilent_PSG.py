

class AgilentPSG:

    @staticmethod
    def _agilent_freq_key():
        return 'Frequency'

    @staticmethod
    def _agilent_freq_sweep_key():
        return 'Frequency - Sweep rate'

    @staticmethod
    def _agilent_output_unit_key():
        return 'Output unit'

    @staticmethod
    def _agilent_output_unit_sweep_key():
        return 'Output unit - Sweep rate'

    @staticmethod
    def _agilent_power_key():
        return 'Power'

    @staticmethod
    def _agilent_power_sweep_key():
        return 'Power - Sweep rate'

    @staticmethod
    def _agilent_levelling_key():
        return 'Automatic levelling control (ALC)'

    @staticmethod
    def _agilent_levelling_sweep_key():
        return 'Automatic levelling control (ALC) - Sweep rate'

    @staticmethod
    def _agilent_phase_sweep_key():
        return 'Phase - Sweep rate'

    @staticmethod
    def _agilent_phase_key():
        return 'Phase'

    @staticmethod
    def _agilent_output_sweep_key():
        return 'Output - Sweep rate'

    @staticmethod
    def _agilent_output_key():
        return 'Output'

    def __init__(self, client):
        self.instr = client.connectToInstrument('Agilent PSG Signal Generator', dict(interface='GPIB', address='19'))
