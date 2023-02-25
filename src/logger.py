import logging
from colorama import Fore, Style


class Formatter(logging.Formatter):

    format = "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s "

    FORMATS = {
        logging.DEBUG: Fore.WHITE + format + Style.RESET_ALL,
        logging.INFO: Fore.GREEN + format + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + format + Style.RESET_ALL,
        logging.ERROR: Fore.RED + format + Style.RESET_ALL,
        logging.CRITICAL: Style.BRIGHT + Fore.RED + format + Style.RESET_ALL,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)

        return formatter.format(record)
    

logger = logging.getLogger()

logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(Formatter())

logger.addHandler(ch)