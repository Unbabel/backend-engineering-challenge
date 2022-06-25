from datetime import datetime

class Entry:
    def __init__(self, date, duration):
        self.date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        self.duration = duration
    def __repr__(self):
        return '{' + str(self.date) + ' : ' + str(self.duration) + '}'