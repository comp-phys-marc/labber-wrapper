import Labber
import unittest
from ...devices.QDevil_QDAC import QDAC
from unittest.mock import MagicMock


class TestQDAC(unittest.TestCase):

    def setUp(self):
        self.device = QDAC(
            Labber.connectToServer('localhost'),
            {
                1: 2,
                2: 3,
                3: 4,
                4: 5
            }
        )

    def test_init(self):
        self.assertIsInstance(self.device, QDAC)
        assert hasattr(self.device, 'instr')
        self.assertIsNotNone(self.device.instr)

    def test_sync(self):
        self.device.instr.setValue = MagicMock()

        cases = [(1, 1), (2, 2), (3, 3), (0, 4), (1, 25), (0, 0)]

        for case in cases:
            self.device.sync(*case)

            if case[0] not in (1, 2) or case[1] > 24 or case[1] < 1:
                self.assertRaises(Exception, self.device.sync, case)

            generator = case[1] + 1
            self.device.instr.setValue.assert_called_with(self.device._qdac_sync_key(case[0]), f'Generator {generator}')