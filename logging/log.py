import Labber
from pathlib import Path


class Log:

    def __init__(self, log_file_path, log_name, log_units, params, increment=True):
        # define log channels
        log = [dict(name=log_name, unit=log_units, vector=False)]

        # check for file and increment count if found
        if increment:
            path = Path(log_file_path)
            found = path.is_file()

            i = 1
            while found:
                log_file_path = f'{path.parent}/{path.name}{i}{path.suffix}'
                path = Path(log_file_path)
                found = path.is_file()
                i += 1

        # create log file
        self.file = Labber.createLogFile_ForData(log_file_path, log, params, use_database=False)
