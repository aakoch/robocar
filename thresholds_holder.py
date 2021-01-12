__filename__ = "thresholds_holder.py"

class ThresholdsHolder():
    """Holds array of thresholds for use for finding lines when line is lost"""

    def __init__(self):
        self.i = 0

    def set_thresholds(self, thresholds):
        self.thresholds = thresholds

    def next_threshold(self):
        self.i += 1
        if (self.i >= len(self.thresholds)):
            self.i = 0
        return self.thresholds[self.i]

    def get_threshold(self):
        return self.thresholds[self.i]

#thresholdsHolder = ThresholdsHolder()
#thresholdsHolder.set_thresholds( \
    #[[(55, 60, -33, 0, -63, -21)], \
    #[(6, 55, -33, -10, -60, -23)], \
    #[(48, 68, -16, 6, -61, -18)], \
    #[(61, 71, -16, -1, -57, -8)]])

#for i in range(1, 50):
    #print(thresholdsHolder.next_threshold())
