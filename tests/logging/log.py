import Labber
import unittest
from logging.log import Log
from unittest.mock import MagicMock

class TestLog(unittest.TestCase):

    def test_init(self):
        Labber.createLogFile_ForData = MagicMock()

        # Test without incrementing

        cases = [
            dict(
                log_file_path='test_file.log',
                log_channels=[dict(name='Voltage', units='V')],
                params=dict(name='param', unit='V', values=[1., 2., 3.]),
                increment=False
            ),
            dict(
                log_file_path='test_log.log',
                log_channels=[dict(name='Current', units='A')],
                params=dict(name='param', unit='A', values=[5., 6., 7.]),
                increment=False
            ),
            dict(
                log_file_path='test_dump.log',
                log_channels=[dict(name='Resistance', units='Ohms')],
                params=dict(name='param', unit='A', values=[10., 11., 12.]),
                increment=False
            )
        ]

        for case in cases:
            Log(**case)

            Labber.createLogFile_ForData.assert_called_with(
                case['log_file_path'],
                case['log_channels'],
                case['params'],
                use_database=False
            )

        # Test with incrementing

        cases = [
            dict(
                log_file_path='test_file.log',
                log_channels=[dict(name='Voltage', units='V')],
                params=dict(name='param', unit='V', values=[1., 2., 3.]),
                increment=False
            ),
            dict(
                log_file_path='test_file.log',
                log_channels=[dict(name='Current', units='A')],
                params=dict(name='param', unit='A', values=[5., 6., 7.]),
                increment=False
            ),
            dict(
                log_file_path='test_file.log',
                log_channels=[dict(name='Resistance', units='Ohms')],
                params=dict(name='param', unit='A', values=[10., 11., 12.]),
                increment=False
            )
        ]

        for i, case in enumerate(cases):
            Log(**case)

            Labber.createLogFile_ForData.assert_called_with(
                case['log_file_path'] if i == 0 else case['log_file_path'] + f'_{i}',
                case['log_channels'],
                case['params'],
                use_database=False
            )
