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

import urllib2
import re

def buildOpener(urlStr,proxyStr=None,proxyUser=None,proxyPasswd=None,
              authRealm=None,authUser=None,authPasswd=None):
    
    retOpener = urllib2.build_opener()

    if proxyStr:
        proxyHandle=urllib2.ProxyHandler(proxyStr)
    else:
        proxyHandle=urllib2.ProxyHandler({})

    retOpener.add_handler( proxyHandle )
        
    if proxyUser:
        passwdMgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passwdMgr.add_password(None,"",proxyUser,proxyPasswd)
        proxyAuthHandle=urllib2.ProxyBasicAuthHandler(passwdMgr)
        retOpener.add_handler( proxyAuthHandle )
    
    if authUser:
        passwdMgr2 = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passwdMgr2.add_password(authRealm,urlStr,authUser,authPasswd)
        urlAuthHandle=urllib2.ProxyBasicAuthHandler(passwdMgr2)
        retOpener.add_handler( urlAuthHandle )
    
    return retOpener

def fetchHTTP(urlStr,proxyStr=None,proxyUser=None,proxyPasswd=None,
              authRealm=None,authUser=None,authPasswd=None):
    
    opener = buildOpener(urlStr,proxyStr,proxyUser,proxyPasswd,authRealm,authUser,authPasswd)
    try:
        httpData = opener.open(urlStr)
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        return None
    else:
        return httpData.readlines()

def getMatchHtmlLine(rawLines,pattern,offsetNum=0):

    mypatt=re.compile(pattern,re.UNICODE)

    if rawLines:
        counter=0
        for oneLine in rawLines:
            if mypatt.search(oneLine):
                #restLine=rawLines[counter:]
                retLine=rawLines[counter+offsetNum]
                return (retLine,rawLines[counter+1+offsetNum:])
            counter=counter+1
    else:
        return (None,rawLines)

    return (None,rawLines)

def removeHtmlTags(rawLines):

    retLines=[]

    for i in range(len(rawLines)):
        tmpLine=rawLines[i]
        if tmpLine:
            tmpLine=re.sub('[\t\n\r\f\v]','',tmpLine)
            tmpLine=re.sub('&nbsp;','',tmpLine)
            tmpLine=re.sub('<.*?>','',tmpLine)
        retLines.append(tmpLine)

    return retLines


if __name__ == "__main__":
    lines=fetchHTTP("http://www.weather.com.cn/html/weather/101020100.shtml")
    if lines:        
        for line in lines:
            print line


