# -*- coding: utf-8 -*-
"""
automate the boring stuff with python 
chapter 6
Practice Projects: Table Printer
https://automatetheboringstuff.com/2e/chapter6/


author: p1xckha
"""

def printTable(tableData):
    # determine the width of each column: colwidth
    colwidth = [0] * len(tableData) # initialize 
    for i in range(len(tableData)):
        width = max(list(map(len, tableData[i])))
        colwidth[i] = width+1
    
    # determine the shape of the new table
    m = max(list(map(len, tableData))) # number of rows
    n = len(tableData) # number of columns
    print(f"The new table is {m}x{n} table, which has {m} rows and {n} col:")
    
    # print the new table
    for i in range(m):
        for j in range(n):
            item = ""
            try:
                item = tableData[j][i].rjust(colwidth[j]," ")
            except:
                item = "".rjust(colwidth[j]," ")
            print(item, end="")
        print("")
    

if __name__ == "__main__":
    tableData = [['apples', 'oranges', 'cherries', 'banana'],
                 ['Alice', 'Bob', 'Carol', 'David'],
                 ['dogs', 'cats', 'moose', 'goose']]
    
    printTable(tableData)
    print("")
    
    tableData2 = [["soccer", "baseball", "hockey", "tennis"],
                  ["iphone", "android", "windows"],
                  ["icecream", "cake"],
                  ["violin"]]
    
    printTable(tableData2)
    
   
