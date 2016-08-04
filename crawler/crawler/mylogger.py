import logging
import logging.handlers


class MyLogger:
    @classmethod
    def from_name(cls, name):
        handler = logging.handlers.TimedRotatingFileHandler(
            name + ".log",
            when='D',
            backupCount=7)
        fmt = '%(asctime)s|%(filename)s:%(funcName)s:%(lineno)s:[%(name)s]:%(message)s'
        formatter = logging.Formatter(fmt)
        handler.setFormatter(formatter)
        flog = logging.getLogger(name)
        flog.addHandler(handler)
        flog.setLevel(logging.DEBUG)
        return flog
