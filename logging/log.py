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
            while found and i < 10:
                if i > 1:
                    log_file_path = f'{path.parent}/{path.name.split(".")[0][:-1]}{i}{path.suffix}'
                else:
                    log_file_path = f'{path.parent}/{path.name.split(".")[0]}{i}{path.suffix}'
                path = Path(log_file_path)
                found = path.is_file()
                i += 1

            if found and i == 10:
                raise Exception(f'Too many log files: {i}')

        # create log file
        self.file = Labber.createLogFile_ForData(log_file_path, log, params, use_database=False)
