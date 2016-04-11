#!/usr/bin/env python
import sys

def findsum(array, s):
    print "find {} in {}".format(s, array)
    rlt = []
    idx = 0
    while idx < len(array):
        if array[idx] == s:
            rlt += [[s]]
        elif array[idx] < s:
            found = findsum(array[idx+1:], s - array[idx])
            for f in found:
                rlt += [f + [array[idx]]]
        idx += 1
    return rlt

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "usage ./find_subarray.py sum array, eg ./find_subarray 15 5 10 10 2 3"
        exit(1)
    array = [int(i) for i in sys.argv[2:]]
    s = int(sys.argv[1])
    print findsum(array, s)

