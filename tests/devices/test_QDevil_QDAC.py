import Labber
import unittest
from ...devices.QDevil_QDAC import QDAC


class TestQDAC(unittest.TestCase):

    def test_init(self):
        device = QDAC(Labber.connectToServer('localhost'))
        self.assertIsInstance(device, QDAC)
        assert hasattr(device, 'instr')
        self.assertIsNotNone(device.instr)

    # TODO: mock device.set_value and assert that it is called with the correct key and value pairs
