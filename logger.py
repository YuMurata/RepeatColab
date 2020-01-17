from logging\
    import (Formatter, handlers, StreamHandler,
            getLogger, DEBUG, Handler, INFO)
import typing
from pathlib import Path


class Logger:
    def __init__(self, module_name: str,
                 *, handler_list: typing.List[Handler] = None,
                 log_file_path: str = None):
        self.logger = getLogger(module_name)
        self.logger.setLevel(DEBUG)

        asctime = '[%(asctime)s]'
        name = '[%(name)s]'
        levelname = '[%(levelname)s]'
        process = '[%(process)d]'
        message = '%(message)s'

        if handler_list is None:
            format_item_list = [asctime, name, levelname, process, message]

            formatter = Formatter(' '.join(format_item_list))

            # stdout
            handler = StreamHandler()
            handler.setLevel(INFO)
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

            if log_file_path is not None:
                Path(log_file_path).parent.mkdir(exist_ok=True, parents=True)

                # file
                handler = handlers.RotatingFileHandler(filename=log_file_path,
                                                       maxBytes=1048576,
                                                       backupCount=3)
                handler.setLevel(DEBUG)
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)

        else:
            for handler in handler_list:
                self.logger.addHandler(handler)

    def debug(self, msg: typing.Any):
        self.logger.debug(msg)

    def info(self, msg: typing.Any):
        self.logger.info(msg)

    def warn(self, msg: typing.Any):
        self.logger.warning(msg)

    def error(self, msg: typing.Any):
        self.logger.error(msg)

    def critical(self, msg: typing.Any):
        self.logger.critical(msg)
