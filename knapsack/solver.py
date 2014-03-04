#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import ctypes
from ctypes import cdll
import logging

from numpy import array
from numpy import zeros
from numpy import int32


def solveTriv(values, weights, capacity):
    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    weight = 0
    taken = []

    for i in range(0, min(len(values), len(weights))):
        if weight + weights[i] <= capacity:
            taken.append(1)
            value += values[i]
            weight += weights[i]
        else:
            taken.append(0)

    isOpt = 0
    return (taken, value, isOpt)

    
def solveDynFwd(values, weights, capacity):
    values = array(values, dtype=int32)
    weights = array(weights, dtype=int32)

    numRows = capacity+1
    numCols = len(values)+1

    table = zeros((numRows, numCols), dtype=int32)
    rows = array(range(1, numRows), dtype=int32)
    cols = array(range(1, numCols), dtype=int32)

    print("Building Table...")
    for row in rows:
        for col in cols:
            #print("(row,col) = (%d, %s)"%(row, col))
            #logging.debug("(row,col) = (%d, %s)"%(row, col))
            if (weights[col-1] <= row):
                table[row][col] = max(table[row][col-1], values[col-1] + table[row - weights[col-1]][col-1])
            else:
                table[row][col] = table[row][col-1]
                
    print("Table:")
    print(table)

    print("Done building table.\n")
    print("Tracking backward...")
    #logging.debug("Table: " + str(table))
    
    (taken, value, isOpt) = ([0 for x in range(len(values))], table[row][col], 1)

    # Pull the items out one by one
    rem = capacity
    for item in range(len(values)-1, -1, -1):
        #logging.debug("Item=%d"%(item))
        #logging.debug("Remaining=%d"%(rem))
        if table[rem][item] != table[rem][item+1]:
            taken[item] = 1
            rem = rem - weights[item]
    
    print("Done tracking.\n")
        
    return (taken, value, isOpt)

    
def solveIt(inputData):
    lib = cdll.LoadLibrary('./solve_it.pyd')
    lib.solve_it.restype = ctypes.c_char_p
    lib.solve_it.argtypes = [ctypes.c_char_p]
    inputBytes = bytes(inputData, encoding='ascii')
    result = lib.solve_it(ctypes.create_string_buffer(inputBytes))
    return str(result, encoding='ascii')

def solveItSlow(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])

    values = [0 for x in range(items)]
    weights = [0 for x in range(items)]

    for i in range(1, items+1):
        line = lines[i]
        parts = line.split()

        values[i-1] = int(parts[0])
        weights[i-1] = int(parts[1])

    items = len(values)

    (taken, value, isOpt) = solveDynFwd(values, weights, capacity)
    
    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(isOpt) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        if "-slow" in sys.argv:
            print(solveItSlow(inputData))
        else:
            print(solveIt(inputData))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
