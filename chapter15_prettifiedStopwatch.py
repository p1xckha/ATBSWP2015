# -*- coding: utf-8 -*-
"""

chapter 15
Prettified Stopwatch
"""

import time

class Stopwatch():
    def __init__(self):
        self.recorded_times = [] # list of unix time
    
    def add_time(self):
        self.recorded_times.append(time.time())
    
    def print_lastlap(self):
        lap_num = len(self.recorded_times) - 1
        total_time = self.recorded_times[lap_num] - self.recorded_times[0]
        total_time = "%.2f" % total_time
        total_time = total_time.rjust(7)
        lap_time = self.recorded_times[lap_num] - self.recorded_times[lap_num - 1]
        lap_time = "%.2f" % lap_time
        lap_time = lap_time.rjust(7)
        print('Lap #%02d: %s (%s)' % (lap_num, total_time , lap_time), end='')
        
    def run(self):
        print("press enter to add a lap.")
        print("Ctrl-C to exit")
        self.add_time() # start
        try:
            while True:
                input()
                self.add_time()
                self.print_lastlap()
        except KeyboardInterrupt as e:
            print("\nDone.")
    
    def reset(self):
        self.recorded_times.clear()
    

if __name__ == "__main__":
    sw = Stopwatch()
    sw.run()
    
