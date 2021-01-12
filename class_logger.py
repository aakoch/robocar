#class_logger.py

__filename__ = "class_logger.py"

# might take up too much memory
TRACE_LOG_LEVEL=const(10)
DEBUG_LOG_LEVEL=const(20)
INFO_LOG_LEVEL=const(30)
WARN_LOG_LEVEL=const(40)
ERROR_LOG_LEVEL=const(50)

class Logger():
    """Logger"""

    def __init__(self):
        self.format_ = "%l:"
        self.log_level = ERROR_LOG_LEVEL

    def set_level(self, level):
        self.log_level = level

    def log(self, level, *msg):
        print(self.format_.replace("%l", level), *msg)

    def trace(self, *msg):
        if self.log_level <= TRACE_LOG_LEVEL:
            self.log("TRACE", *msg)

    def debug(self, *msg):
        if self.log_level <= DEBUG_LOG_LEVEL:
            self.log("DEBUG", *msg)

    def info(self, *msg):
        if self.log_level <= INFO_LOG_LEVEL:
            self.log("INFO", *msg)

    def warn(self, *msg):
        if self.log_level <= WARN_LOG_LEVEL:
            self.log("WARN", *msg)

    def error(self, *msg):
        if self.log_level <= ERROR_LOG_LEVEL:
            self.log("ERROR", *msg)
