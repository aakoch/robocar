#log.py
# log - By: aakoch - Sat Apr 28 2018

# might take up too much memory
TRACE_LOG_LEVEL=const(10)
DEBUG_LOG_LEVEL=const(20)
INFO_LOG_LEVEL=const(30)
WARN_LOG_LEVEL=const(40)
ERROR_LOG_LEVEL=const(50)

log_level = TRACE_LOG_LEVEL

try:
    trace("trace")
except NameError:
    def trace(*msg):
        if log_level >= TRACE_LOG_LEVEL:
            print("TRACE:", *msg)

try:
    debug("debug")
except NameError:
    def debug(*msg):
        if log_level >= DEBUG_LOG_LEVEL:
            print("DEBUG:", *msg)

try:
    info("info")
except NameError:
    def info(*msg):
        if log_level >= INFO_LOG_LEVEL:
            print("INFO:", *msg)

try:
    warn("warn")
except NameError:
    def warn(*msg):
        if log_level >= WARN_LOG_LEVEL:
            print("WARN:", *msg)

try:
    error("error")
except NameError:
    def error(*msg):
        if log_level >= ERROR_LOG_LEVEL:
            print("ERROR:", *msg)

#def trace(*msg):
    #if log_level >= TRACE_LOG_LEVEL:
        #print("TRACE:", *msg)
        ##pyb.delay(10)

#def debug(*msg):
    #if log_level >= DEBUG_LOG_LEVEL:
        #print("DEBUG:", *msg)

#def info(*msg):
    #if log_level >= INFO_LOG_LEVEL:
        #print("INFO:", *msg)

#def warn(*msg):
    #if log_level >= WARN_LOG_LEVEL:
        #print("WARN:", *msg)

#def error(*msg):
    #if log_level >= ERROR_LOG_LEVEL:
        #print("ERROR:", *msg)
