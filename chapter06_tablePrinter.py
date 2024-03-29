# -*- coding: utf-8 -*-
"""
automate the boring stuff with python 
chapter 6
Practice Projects: Table Printer
https://automatetheboringstuff.com/2e/chapter6/


author: p1xckha
"""


def print_transposed_table(table_data):
    '''
    table_data: list of list of string
    print transposed table as fllows.
    
    for example:
    table_data = [[11,12,13],
                  [21,22,23]]
    print_transposed_table(table_data)
    
    result:
        11 21 
        12 22
        13 23

    '''
    # determine the width of each column: colwidth
    colwidth = [0] * len(table_data) # initialize 
    for i in range(len(table_data)):
        width = max(list(map(len, table_data[i])))
        colwidth[i] = width+1
    
    # determine the shape of the new table
    m = max(list(map(len, table_data))) # number of rows
    n = len(table_data) # number of columns
    print(f"The new table is {m}x{n} table, which has {m} rows and {n} col:")
    
    # print the new table
    for i in range(m):
        for j in range(n):
            item = ""
            try:
                item = table_data[j][i].rjust(colwidth[j]," ")
            except:
                item = "".rjust(colwidth[j]," ")
            print(item, end="")
        print("")
    

if __name__ == "__main__":
    table_data = [['apples', 'oranges', 'cherries', 'banana'],
                 ['Alice', 'Bob', 'Carol', 'David'],
                 ['dogs', 'cats', 'moose', 'goose']]
    
    print_transposed_table(table_data)
    print("")
    
    table_data2 = [["soccer", "baseball", "hockey", "tennis"],
                  ["iphone", "android", "windows"],
                  ["icecream", "cake"],
                  ["violin"]]
    
    print_transposed_table(table_data2)
    
   
