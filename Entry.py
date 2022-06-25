from datetime import datetime

class Entry:
    def __init__(self, minute, duration):
        self.minute = minute
        self.duration = duration
    def __repr__(self):
        return '{"' + str(self.minute) + '" : ' + str(self.duration) + '}'