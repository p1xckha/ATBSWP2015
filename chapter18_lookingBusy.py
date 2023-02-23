# -*- coding: utf-8 -*-
"""
Looking Busy
"""

import pyautogui
import time
from math import sqrt

class MouseCursor():
    SHORT_DISTANCE = 50
    def __init__(self):
        self.positions = [] # list of (x, y)
        self.interval = 1 # 
        self.DURATION = 60 # 
        self.recent_distance = 0
    
    def add_position(self):
        position = pyautogui.position()
        self.positions.append(position)
    
    def distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return distance
    
    def set_recent_distance(self):
        # discard old positions and remain recent positions in 10mins
        n = int(self.DURATION / self.interval)
        if len(self.positions) > n:
            self.positions = self.positions[-n:]
        
        # calculate the total distance mouse move in recent 10mins
        recent = 0
        for i in range(len(self.positions) - 1):
            pos1 = self.positions[i]
            pos2 = self.positions[i+1]
            distance = self.distance(pos1, pos2)
            recent += distance
        self.recent_distance = recent
    
    def get_recent_distance(self):
        return self.recent_distance
        
    def show_positions(self):
        print(self.positions)
    
    def is_many_positons(self):
        return len(self.positions) >= self.DURATION
    
    def is_long_totaldistance(self):
        return self.get_recent_distance() > self.SHORT_DISTANCE
    
    def handle_positions(self):
        self.add_position()
        self.set_recent_distance()
        
    def isused(self):
        if self.is_many_positons() and not self.is_long_totaldistance():
            return False
        else:
            return True
    
    def run(self):
        print("*" * 20)
        print("press ctrl-C to exit")
        print("*" * 20)
        try:
            while True:
                self.handle_positions()
                if self.isused():
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
    
    
    
    