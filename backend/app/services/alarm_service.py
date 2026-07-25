class AlarmService:
    def __init__(self):
        self.alarms = []

    def add_alarm(self, alarm):
        self.alarms.append(alarm)
        return alarm

    def get_all_alarms(self):
        return self.alarms

    def clear_alarms(self):
        self.alarms.clear()
