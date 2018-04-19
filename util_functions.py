#util_functions.py
pass
def remap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

def theta(line):
    return line.theta() if line.theta() < 90 else line.theta() - 180
