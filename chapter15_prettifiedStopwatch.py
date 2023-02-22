# -*- coding: utf-8 -*-
"""
Automate Boring Stuff With Python
chapter 15
Prettified Stopwatch

if this script run, it print the Laps in the following format.

**************************
press enter to add a lap.
Ctrl-C to exit
**************************

Lap #01:    3.34 (   3.34)
Lap #02:    6.14 (   2.80)
Lap #03:    8.07 (   1.93)
Lap #04:    8.90 (   0.82)
Lap #05:    9.80 (   0.91)
Lap #06:   10.04 (   0.23)
Lap #07:   10.26 (   0.23)
.....

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
        print("**************************")
        print("press enter to add a lap.")
        print("Ctrl-C to exit")
        print("**************************")
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
    
