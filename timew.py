#!/usr/bin/env python

import threading
import pytz

from subprocess import check_output, CalledProcessError

TIMEZONE = pytz.timezone("America/Toronto")


class TimeWD:
    def __init__(self):
        self.current_task_line = "Updating task info..."
        self.daily_total_line = "00:00"
        self.current_task_update_status = "IDLE"

    def start(self):
        self._cts_update_current_task_line()
        self._cts_update_daily_total_line()

    def get_current_task_line(self):
        return self.current_task_line

    def _update_current_task_line(self):
        if self.current_task_update_status == "IDLE":
            self.current_task_update_status = "BUSY"
        else:
            return

        try:
            lines = check_output(["timew"]).split('\n')
            lines = [_.strip() for _ in lines]

            task_name = lines[0][len('Tracking'):].strip()
            task_time = lines[3].split()[1]

            self.current_task_line = "{} ({task_t}) [{total}]".format(
                task_name,
                task_t=task_time,
                total=self.daily_total_line)
        except CalledProcessError:
            self.current_task_line = "No task running. [{total}]".format(total=self.daily_total_line)
        except: # Catch-all, don't crash i3bar
            self.current_task_line = "Current task query failed."

        self.current_task_update_status = "IDLE"

    def _update_daily_total_line(self):
        if self.current_task_update_status != "IDLE": # HACK
            return

        try:
            lines = check_output(["timew", "day"]).split('\n')
            lines = [line.strip() for line in lines]

            for line in lines:
                if 'Tracked' in line:
                    self.daily_total_line = line.split()[1]

        except CalledProcessError:
            self.current_task_line = "'timew day' call failed."
        except:
            self.current_task_line = "Daily total query failed."

    def _cts_update_current_task_line(self):
        self._update_current_task_line()
        t = threading.Timer(5, self._cts_update_current_task_line)
        t.start()

    def _cts_update_daily_total_line(self):
        self._update_daily_total_line()
        t = threading.Timer(31, self._cts_update_daily_total_line)
        t.start()

if __name__ == "__main__":
    timewd = TimeWD()
    timewd.start()
    import time
    while True:
        time.sleep(1)
        print timewd.get_current_task_line()
