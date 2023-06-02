import Labber


class Log:

    def __init__(self, log_file_path, log_name, log_units, params):
        # define log channels
        log = [dict(name=log_name, unit=log_units, vector=False)]

        # create log file
        self.file = Labber.createLogFile_ForData(log_file_path, log, params, use_database=False)
