#!/usr/bin/python

"""
Output lines selected randomly from a file

Copyright 2005, 2007 Paul Eggert.
Copyright 2010 Darrell Benjamin Carbajal.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Please see <http://www.gnu.org/licenses/> for a copy of the license.

$Id: randline.py,v 1.4 2010/04/05 20:04:43 eggert Exp $
"""

import random, sys, string, argparse
from optparse import OptionParser

class shuf:
    def __init__(self, inputlines, headcount, repeat):
        self.inputlines = inputlines
        self.headcount = headcount
        self.repeat = repeat

    def chooseline(self):
        if len(self.inputlines) == 0:
            return
        if self.repeat:
            while self.headcount > 0:
                sys.stdout.write(random.choice(self.inputlines))
                self.headcount-=1
        else:
            for index in range(0,self.headcount):
                toPop = random.choice(self.inputlines)
                sys.stdout.write(toPop)
                popIndex = self.inputlines.index(toPop)
                self.inputlines.pop(popIndex)
                self.headcount-=1

def main():
    version_msg = "%prog 2.0"
    usage_msg = """%prog [OPTION]... FILE or  %prog -i LO-HI [OPTION]...
    Output randomly selected lines from FILE."""

    parser = OptionParser(version=version_msg,
                          usage=usage_msg)
    parser.add_option("-n", "--head-count=COUNT",
                      action="store", dest="headcount", default=sys.maxsize,
                      help="output at most COUNT lines")
    parser.add_option("-i", "--input-range=LO-HI",
                      action="store", dest="inputrange", default="",
                      help="treat each number LO through HI as an input line")
    parser.add_option("-r", "--repeat",
                      action="store_const", dest="repeat", default=False,
                      const=True, help="output lines can be repeated")

    options, args = parser.parse_args(sys.argv[1:]) # options --> holds num range ; args --> holds file
    try:
        headcount = int(options.headcount) # headcount holds file after -n
    except:
        parser.error("invalid line count: '{0}'".
                     format(options.headcount))
    if headcount==0:
        parser.error("invalid line count: '{0}'".
                     format(options.headcount))
    if headcount<0:
        parser.error("negative count: '{0}'".
                      format(options.headcount))

        # -i option
        # need to check for errors
    inputrange = options.inputrange
    
    if len(inputrange) > 0: # inputrange should hold numbers after -i
        if len(args) != 0: # args should hold file names (which should be 0 in this case)
            parser.error("invalid input range '{0}'".
                         format(args[0]))
        
        nums = inputrange.split("-") #puts the nums before and after "-" into array nums        
        if len(nums) != 2:
            parser.error("invalid input range '{0}'".
                         format(options.inputrange))
        else:
            lo = nums[0]
            hi = nums[1]
        try:
            lo = int(lo)
        except ValueError as e:
            parser.error("invalid input range '{0}'".
                         format(options.inputrange))
        try:
            hi = int(hi)
        except ValueError as e:
            parser.error("invalid input range '{0}'".
                         format(options.inputrange))
        
        if lo > hi:
            parser.error("invalid input range '{0}'".
                         format(options.inputrange))

        inputlines = list(range(lo,hi+1))
        
        i = 0
        while i<len(inputlines):
            inputlines[i] = str(inputlines[i]) + "\n"
            i+=1

    else:
        if len(args) == 0:
            inputlines = sys.stdin.readlines()
        elif (args[0] == "-" and len(args == 1)):
            inputlines = sys.stdin.readlines()
        elif len(args) == 1:
            try:
                f = open(args[0], 'r')
                inputlines = f.readlines()
                f.close()
            except IOError as e:
                errno, strerror = e.args
                parser.error("I/O error({0}): {1}".
                     format(errno, strerror))
        else:
            parser.error("extra operand '{0}'".
                         format(args[1]))
                
    repeat = options.repeat

    if repeat==False:
        if headcount > len(inputlines):
            headcount = len(inputlines)

    generator = shuf(inputlines, headcount, repeat)
    generator.chooseline()

if __name__ == "__main__":
    main()
