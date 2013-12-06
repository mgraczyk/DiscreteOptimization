#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import ctypes
from ctypes import cdll
import logging


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
    rows = capacity+1
    cols = len(values)+1

    zeros = [0]*cols
    table = [zeros[:] for i in range(rows)]
    
    print("Building Table...")
    
    for row in range(1, rows):
        for col in range(1, cols):
            logging.debug("(row,col) = (%d, %s)"%(row, col))
            if (weights[col-1] <= row):
                table[row][col] = max(table[row][col-1], values[col-1] + table[row - weights[col-1]][col-1])
            else:
                table[row][col] = table[row][col-1]
                
    print("Table:")
    print(table)

    print("Done building table.\n")
    print("Tracking backward...")
    #logging.debug("Table: " + str(table))
    
    (taken, value, isOpt) = ([0 for x in xrange(len(values))], table[row][col], 1)

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
    #lib = cdll.LoadLibrary('D:\School\Coursera\DiscreteOptimization\knapsack\CSpeedUp.pyd');
    lib = cdll.LoadLibrary('./CSpeedUp.pyd')
    lib.solve_it.restype = ctypes.c_char_p
    lib.solve_it.argtypes = [ctypes.c_char_p]
    return lib.solve_it(ctypes.create_string_buffer(inputData))

def solveItSlow(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])

    values = [0 for x in xrange(items)]
    weights = [0 for x in xrange(items)]

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
        print(sys.argv)
        if len(sys.argv) > 2 and (sys.argv[2] == '-slow'):
            print(solveItSlow(inputData))
        else:
            print(solveIt(inputData))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')
