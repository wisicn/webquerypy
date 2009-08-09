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
#global city url data and sms SubScriber data
cityURL = {'shanghai':'http://www.weather.com.cn/html/weather/101020100.shtml',
           'zibo':'http://www.weather.com.cn/html/weather/101120301.shtml'}

def getCityData(city):

    if cityURL.has_key(city):
        htmlDateList = handleHTTP.fetchHTTP(cityURL[city])
    else:
        return None

    usefulLines = []
    timeStr=time.strftime('[%m-%d_%H:%M]')
    if htmlDateList:

        if len(htmlDateList) > 100:
            newLines=htmlDateList

            matchStr,newLines=handleHTTP.getMatchHtmlLine(newLines,u'<h3><strong>')
            if matchStr and len(newLines) > 1:
                usefulLines.append(matchStr)

                matchStr,newLines=handleHTTP.getMatchHtmlLine(newLines,u'm_1_1')
                if matchStr and len(newLines) > 1:
                    usefulLines.append(matchStr)

                    matchStr,newLines=handleHTTP.getMatchHtmlLine(newLines,u'<em><strong>')
                    if matchStr and len(newLines) > 1:
                        usefulLines.append(matchStr)

                        matchStr,newLines=handleHTTP.getMatchHtmlLine(newLines,
                                                                      u'<em class=')
                        if matchStr and len(newLines) > 1:
                            usefulLines.append(matchStr)
                            usefulLines.append(newLines[0])

    # remove all the /t and /n /r, then remove html tag
    usefulLines=handleHTTP.removeHtmlTags(usefulLines)

    if usefulLines:
        usefulLines.append(timeStr)
        #return ','.join(usefulLines)
        return re.sub('[ \t]','',','.join(usefulLines))
    else:
        return None

def getCitys(citys):
    
    cityList = citys.split(',')
    resultList = []
    
    if cityList:
        for eachCity in cityList:
            oneResult = getCityData(eachCity)
            if oneResult:
                resultList.append(oneResult)
            time.sleep(globalWaitSeconds)
    if resultList:
        return resultList
    else:
        return None

def printCitys(citys):
    
    massResultList = getCitys(citys)
    
    if massResultList:
        for line in massResultList:
            print "%s" % line

    return 0

def listCitys():

    for city in cityURL.keys():
        print "%s" % city

def listCitysURL():

    for city in cityURL.keys():
        print "%s:%s" % (city,cityURL[city])

def main():

    usage = """usage: %prog [options] <city>"""
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-m", "--mass", dest="massFlag",action="store_true",
                      help="""Mass mode, you can specific more than one city
,separated by comma""")
    parser.add_option("-l", "--list", default=False,
                      dest="listCitysAction", action="store_true" ,
                      help="show the supported citys list")
    parser.add_option("-L", "--List", default=False,
                      dest="listCityURLAction", action="store_true" ,
                      help="show the supported citys list with URL")

    (options, args) = parser.parse_args()

    if options.listCitysAction:
        listCitys()
    elif options.listCityURLAction:
        listCitysURL()
    else:
        if len(args) != 1:
            #parser.print_help()
            parser.error("incorrect number of arguments")
        if options.massFlag:
            printCitys(args[0])
        else:
            print getCityData(args[0])

if __name__ == "__main__":
    main()
