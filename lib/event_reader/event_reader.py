from datetime import datetime

class EventReader:
    def __init__(self):
        pass

    def validate_timestamp(self, event):
        try:
            datetime.strptime(event["timestamp"], '%Y-%m-%d %H:%M:%S.%f')
            return True
        except ValueError:
            return False
        except KeyError:
            return False
    
    def validate_duration(self, event):
        try:
            float(event["duration"])
            return True
        except ValueError:
            return False
        except KeyError:
            return False

    def validate(self, event):
        return self.validate_duration(event) and self.validate_timestamp(event)
        