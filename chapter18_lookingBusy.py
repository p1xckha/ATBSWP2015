# -*- coding: utf-8 -*-
"""
Looking Busy
"""

import pyautogui
import time
from math import sqrt

class MouseCursor():
    SHORT_DISTANCE = 1000
    def __init__(self):
        self.interval = 1 # 
        self.DURATION = 60 # 
        self.recent_distance = 0
        self.positions = None # list of (x, y) as circular buffer
        self.latest_positon_index = -1
        self.initialize_positions()
    
    def initialize_positions(self):
        buffersize = int (self.DURATION / self.interval)
        self.positions = [None] * buffersize
        
    def add_position(self):
        position = pyautogui.position()
        self.move_latest_position_index()
        i = self.latest_positon_index
        self.positions[i] = position
    
    def move_latest_position_index(self):
        self.latest_positon_index = (self.latest_positon_index + 1) % self.DURATION
        
    def distance(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return distance
    
    def set_recent_distance(self):
        # calculate the total distance mouse move in recent 10 mins
        recent = 0
        i = self.latest_positon_index
        while self.positions[i] != None and self.positions[i-1] != None:
            pos1 = self.positions[i-1]
            pos2 = self.positions[i]
            distance = self.distance(pos1, pos2)
            recent += distance
            i = (i-1) % int(self.DURATION / self.interval)
            if i == self.latest_positon_index:
                break
        self.recent_distance = recent
    
    def get_recent_distance(self):
        return self.recent_distance
        
    def show_positions(self):
        print(self.positions)
    
    def is_many_positons(self):
        i = self.latest_positon_index
        amount = 0
        while self.positions[i] != None:
            amount += 1
            i = (i-1) % int (self.DURATION / self.interval)
            if i == self.latest_positon_index:
                break
        
        return amount == int (self.DURATION / self.interval)
    
    def is_long_recent_distance(self):
        return self.get_recent_distance() > self.SHORT_DISTANCE
    
    def handle_positions(self):
        self.add_position()
        self.set_recent_distance()
        
    def isused(self):
        if self.is_many_positons() and not self.is_long_recent_distance():
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
    
    
    
    