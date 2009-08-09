#!/usr/bin/env python
# -*- coding: utf-8 -*-
# $Id$
# Author: Wisilence Seol (wisicn AT gmail DOT com)
# 
# Copyright (C) 2009 by Wisilence Seol(wisicn AT gmail DOT com).
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 2 as published by the Free Software Foundation.
#
# You may obtain a copy of the License at:
# http://www.gnu.org/licenses/gpl-2.0.html
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software 
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
# MA 02110-1301, USA.

import handleHTTP
import re
import time
import optparse

globalWaitSeconds=1

baseQueryURL='http://www.google.com/finance?q='

def getOneQuery(tickerSymbol):
    
    queryURL=baseQueryURL+tickerSymbol
    htmlDateList = handleHTTP.fetchHTTP(queryURL)

    usefulLines = []
    if htmlDateList:

        #build the first two fields, Market,Symbol
        queryLines = tickerSymbol.split(':')
        for eachLine in queryLines:
            usefulLines.append(eachLine)

        if len(htmlDateList) > 100:
            newLines = htmlDateList
            
            dropStr,newLines=handleHTTP.getMatchHtmlLine(newLines,'class="pr"')
            if dropStr and len(newLines) > 1:
                usefulLines.append(newLines[0])

                dropStr,newLines=handleHTTP.getMatchHtmlLine(newLines,'id=price-change')
                if dropStr and len(newLines) > 1:
                    usefulLines.append(newLines[0])
                    usefulLines.append(newLines[1])
        
                    dropStr,newLines=handleHTTP.getMatchHtmlLine(newLines,'mdata-dis',-4)
                    if dropStr and len(newLines) > 1:
                        tmpLines=newLines[:3]
                        combinStr='\t'.join(tmpLines)
                        usefulLines.append(combinStr)

                        dropStr,newLines=handleHTTP.getMatchHtmlLine(newLines,'>Open</span>')
                        if dropStr and len(newLines) > 1:
                            usefulLines.append(newLines[0])

        # remove all the /t and /n /r, then remove html tag
        usefulLines=handleHTTP.removeHtmlTags(usefulLines)

    if usefulLines:
        return ','.join(usefulLines)
    else:
        return None

def getQuerys(tickerSymbols):

    queryList=tickerSymbols.split(',')
    resulList = []

    if queryList:
        for eachQuery in queryList:
            oneResult = getOneQuery(eachQuery)
            if oneResult:
                resulList.append(oneResult)
            time.sleep(globalWaitSeconds)

    if resulList:
        return resulList
    else:
        return None

def main():

    usage = """usage: %prog [options] <StockSymbol> 
       StockSymbol should be like Market:Number,for example HKG:2600"""
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-m", "--mass", dest="massFlag",action="store_true",
                      help="""Mass mode, you can specific more than one stock
symbol, separated by comma""")

    (options, args) = parser.parse_args()

    if len(args) != 1:
        #parser.print_help()
        parser.error("incorrect number of arguments")
    if options.massFlag:
        #print "mass reading %s..." % args[0]
        massResultList = getQuerys(args[0])
        if massResultList:
            for line in massResultList:
                print "%s" % line
    else:
        #print "single reading %s..." % args[0]
        print getOneQuery(args[0])

if __name__ == "__main__":
    main()
    #aa=getOneQuery('HKG:0606')
    #print "%s" % aa

#    aLots = getQuerys('HKG:0606,HKG:2600,SHA:600600')
#    aLots = getQuerys('HKG:2600')
#    if aLots:
#        for line in aLots:
#            print "%s" % line
