import sys
from enum import Enum


class Logger:
    class Level(Enum):
        DEBUG = 1
        WARNING = 2
        FATAL = 3

    _colors = {
        Level.DEBUG.value: '\033[92m',
        Level.WARNING.value: '\033[93m',
        Level.FATAL.value: '\033[91m',
        'END': '\033[0m'
    }

    @staticmethod
    def log(message: str, level=Level.WARNING) -> None:
        color = Logger._colors[level.value]
        formatted_message = '{}{}{}\n'.format(color, message, Logger._colors['END'])
        if level == Logger.Level.DEBUG:
            print(formatted_message, end='')
        else:
            sys.stderr.write(formatted_message)


if __name__ == '__main__':
    Logger.log('DEBUG', Logger.Level.DEBUG)
    Logger.log('WARNING', Logger.Level.WARNING)
    Logger.log('FATAL', Logger.Level.FATAL)
