import os
import logging
from dataclasses import dataclass
from utils.date_time import now
from typing import Any

@dataclass(kw_only=True)
class CustomFormatter(logging.Formatter):

    grey        : str = "\x1b[38;20m"
    yellow      : str = "\x1b[33;20m"
    green       : str = "\x1b[32m"
    red         : str = "\x1b[31;20m"
    bold_red    : str = "\x1b[31;1m"
    reset       : str = "\x1b[0m"
    
    def __init__(self, name):
        self.name = name
        self.formatmsg   : str = f"[%(asctime)s] [{name}] [%(levelname)s]: %(message)s"

        self.FORMATS = {
            logging.DEBUG:      f"{self.green}{self.formatmsg}{self.reset}",
            logging.INFO:       f"{self.grey}{self.formatmsg}{self.reset}",
            logging.WARNING:    f"{self.yellow}{self.formatmsg}{self.reset}",
            logging.ERROR:      f"{self.red}{self.formatmsg}{self.reset}",
            logging.CRITICAL:   f"{self.bold_red}{self.formatmsg}{self.reset}"
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

@dataclass(kw_only=True)
class Log:

    name: str
    file_logger: bool = False
    log_file_name: str = "log"
    day = now(format="%Y_%m_%d")
    now = now(format="at_%H_%M_%S")


    def __post_init__(self):
        logging.getLogger('asyncio').setLevel(logging.WARNING)
        self.__init_streeam_handler()
        if self.file_logger:
            self.__init_log_folder()
            self.__init_file_handler("log", name=self.log_file_name)
            self.__init_file_handler("csv", name=self.log_file_name, input=False)


    def __init_log_folder(self):
        self.log_folder = f"{os.getcwd()}/log/{self.day}/"
        if not os.path.exists(self.log_folder): os.makedirs(self.log_folder)


    def __init_streeam_handler(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(level=logging.DEBUG)

        self.stream_channel = logging.StreamHandler()

        self.stream_channel.setFormatter(CustomFormatter(name=self.name))
        self.logger.addHandler(self.stream_channel)


    def __init_file_handler(self, file_type: str, name: str, input: bool = True):
        log_file = f"{self.log_folder}{name}_{self.now}.{file_type}"

        with open(f"{log_file}", 'w'): ... # Create log file

        if input:
            self.file_channel = logging.FileHandler(filename=log_file)
            self.file_channel.setFormatter(CustomFormatter(name=self.name))
            self.logger.addHandler(self.file_channel)
            
    
    def info(self,  msg: Any):  return self.logger.info(msg)

    def debug(self, msg: Any):  return self.logger.debug(msg)

    def warn(self,  msg: Any):  return self.logger.warning(msg)

    def error(self, msg: Any):  return self.logger.error(msg)


