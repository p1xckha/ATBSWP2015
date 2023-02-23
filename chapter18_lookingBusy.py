# -*- coding: utf-8 -*-
"""
Looking Busy

find out whether PC is used or not in the following way:
    mouse cursor was moved -> PC is used
    mouse cursor was not moved -> PC is not used
"""

import pyautogui
import time
from math import sqrt
import numpy as np


class MouseCursor():
    SHORT_DISTANCE = 10
    def __init__(self):
        self.interval = 1 # seconds
        self.DURATION = 60 # seconds
        self.recent_distance = 0 # distance which mouse moved in recent DURATION
        self.positions = None # list of (x, y) as circular buffer
        self.buffersize = None
        self.initialize_positions()
        self.total_time = 0
    
    def initialize_positions(self):
        buffersize = int (self.DURATION / self.interval)
        self.positions = np.zeros((buffersize, 2))
        self.buffersize = buffersize
        
    def add_position(self):
        position = pyautogui.position()
        self.positions = np.roll(self.positions, 1, axis=0) # shift one element
        self.positions[0] = position # override oldest element with position
    
    def distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return distance
    
    def set_recent_distance(self):
        # calculate the distance mouse moved in resent DURATION
        recent_distance = 0
        for i in range(1, self.buffersize):
            pos1 = self.positions[i-1]
            pos2 = self.positions[i]
            distance = self.distance(pos1, pos2)
            recent_distance += distance
        self.recent_distance = recent_distance
    
    def get_recent_distance(self):
        return self.recent_distance
        
    def show_positions(self):
        print(self.positions)
    
    def is_many_positons(self):
        # if self.positions are full, we get enough positions  
        return self.total_time >= self.buffersize
    
    def is_long_recent_distance(self):
        # if mouse moves, I assume PC is being used now
        return self.get_recent_distance() > self.SHORT_DISTANCE
    
    def handle_positions(self):
        self.add_position()
        self.total_time += self.interval
        self.set_recent_distance()
        
    def is_used(self):
        if self.is_many_positons() and not self.is_long_recent_distance():
            return False # mouse is not used
        else:
            return True # mouse is used
    
    def run(self):
        print("*" * 20)
        print("press ctrl-C to exit")
        print("*" * 20)
        try:
            while True:
                self.handle_positions()
                if self.is_used():
                    print("You are using PC now. ", end="")
                else:
                    print("You are not using PC now. ", end="")
                print("mouse recently moved  %d" % (self.recent_distance) )
                time.sleep(self.interval)
        except KeyboardInterrupt as e:
            print(e)

if __name__ == '__main__':
    mouse = MouseCursor()
    mouse.run()
    
    
    
    