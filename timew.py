#!/usr/bin/env python

import threading
from subprocess import check_output, CalledProcessError

import pytz


TIMEZONE = pytz.timezone("America/Toronto")
TASK_LINE_DELAY = 5
DAILY_TOTAL_DELAY = 31


class TimeWD(object):
    def __init__(self):
        self.task_line = "Updating task info..."
        self.daily_total = "00:00"
        self.update_lock = threading.Lock()

    def start(self):
        self._start_task_line_thread()
        self._start_daily_total_thread()

    def get_task_line(self):
        return self.task_line

    def _update_task_line(self):
        with self.update_lock:
            try:
                lines = check_output(["timew"]).split('\n')
                lines = [line.strip() for line in lines]

                task_name = lines[0][len('Tracking'):].strip()
                task_time = lines[3].split()[1]

                self.task_line = "{} ({task_t}) [{total}]".format(
                    task_name,
                    task_t=task_time,
                    total=self.daily_total)
            except CalledProcessError:
                self.task_line = "No task running. [{total}]".format(
                    total=self.daily_total)
            except:  # pylint: disable=bare-except
                self.task_line = "Current task query failed."

    def _update_daily_total(self):
        with self.update_lock:
            try:
                lines = check_output(["timew", "day"]).split('\n')
                lines = [line.strip() for line in lines]

                for line in lines:
                    if 'Tracked' in line:
                        self.daily_total = line.split()[1]

            except CalledProcessError:
                self.task_line = "'timew day' call failed."
            except:  # pylint: disable=bare-except
                self.task_line = "Daily total query failed."

    def _start_task_line_thread(self):
        self._update_task_line()
        self.task_line_thread = threading.Timer(
            TASK_LINE_DELAY,
            self._start_task_line_thread)
        self.task_line_thread.daemon = True
        self.task_line_thread.start()

    def _start_daily_total_thread(self):
        self._update_daily_total()
        self.daily_total_thread = threading.Timer(
            DAILY_TOTAL_DELAY,
            self._start_daily_total_thread)
        self.daily_total_thread.daemon = True
        self.daily_total_thread.start()


if __name__ == "__main__":
    timewd = TimeWD()
    timewd.start()
    import time
    while True:
        time.sleep(1)
        print timewd.get_task_line()
