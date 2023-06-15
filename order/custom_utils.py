from order.models import Store

import datetime
from zoneinfo import ZoneInfo

class StoreWrapper:
    """Wrapper for Store model with helper functions"""

    def __init__(self, store:Store):
        self.store = store

        schedule = store.schedule.__dict__
        del schedule['_state']
        del schedule['id']
        self.schedule = list(schedule.values())

    def schedule_to_dict(self):
        processed_schedule = {}
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, weekday in enumerate(weekdays):
            start_time = self.schedule[i]
            end_time = self.schedule[i+1]
            if start_time is None or end_time is None:
                processed_schedule[weekday] = "Closed"
            else:
                processed_schedule[weekday] = \
                f" {start_time.strftime('%I:%M %p')} -  {end_time.strftime('%I:%M %p')}".replace(" 0", "")

        return processed_schedule
    
    def store_to_dict(self):
        processed_store = self.store.__dict__.copy()
        del processed_store['_state']
        del processed_store['timezone']

        return processed_store
    
    def check_is_open(self):
        is_open = True

        if self.store.out_of_schedule_close:
            is_open = False

        else:
            timezone = ZoneInfo(self.store.timezone)
            
            localized_datetime = datetime.datetime.now(tz=timezone)
            current_day = localized_datetime.weekday()
            localized_time = localized_datetime.time()

            today_open = self.schedule[current_day*2]
            today_close = self.schedule[current_day*2 + 1]

            if today_open is None or today_close is None:
                is_open = False
            elif localized_time < today_open or localized_time > today_close:
                is_open = False

        return is_open
