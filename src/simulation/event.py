from datetime import datetime

class Event:
    def __init__(self, date: datetime, oil_left: int, oil_added: int):
        self.date = date
        self.oil_left = oil_left
        self.oil_added = oil_added

