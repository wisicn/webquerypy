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

import pySMS
import weatherQuery
import optparse

#global build-in preset sms SubScriber data

subscriberData = {'shanghai':'13800000000,13900000000',
                  'zibo':'13800000000,13700000000'}


def sendCitys(mobileNum,mobilePasswd):

    destPhoneMsgList=[]

    for city in subscriberData.keys():
        textStr = weatherQuery.getCityData(city)        
        if textStr:
            sendBody = (subscriberData[city],textStr)
            destPhoneMsgList.append(sendBody)
        else: 
            print "can not get weather for %s" % city
    if destPhoneMsgList:
        return pySMS.sendMultiMsgToPhones(mobileNum,mobilePasswd,destPhoneMsgList)
    else:
        return 1

def sendOneCity(mobileNum,mobilePasswd,city,destPhones):
    
    textStr = weatherQuery.getCityData(city)
    if textStr:
        return pySMS.sendMsgToPhones(mobileNum,mobilePasswd,destPhones,textStr)
    else:
        print "can not get weather for %s" % city
        return 1

def main():

    usage = """usage: %prog [options] <city>"""
    parser = optparse.OptionParser(usage=usage)

    parser.add_option("-f", "--from", default=None,
                      dest="fromPhone", action="store" ,type="string",
                      help="the mobile phone from which the SMS will be sent")
    parser.add_option("-p", "--passwd", "--password", default=None,
                      dest="phonePasswd",action="store" ,type="string",
                      help="the password of the mobile phone")
    parser.add_option("-t", "--to", default=None,
                      dest="destPhone",action="store" ,type="string",
                      help="the mobile phone to which the SMS will be sent")
    parser.add_option("-a", "--automatic", dest="fullAutomatic",action="store_true",
                      default=False,help="""full automatic mode, weather SMS will be
sent to the build-in preset mobile phones""")

    (options, args) = parser.parse_args()


    if options.fromPhone and options.phonePasswd: 

        if options.fullAutomatic:
            return sendCitys(options.fromPhone,options.phonePasswd)
        elif options.destPhone:

            if len(args) != 1:
                parser.error("""incorrect number of arguments,see --help/-h for
help""")
            else:
                city=args[0]

            return sendOneCity(options.fromPhone,
                               options.phonePasswd,
                               city,
                               options.destPhone)
        else:
            parser.error("""you must specific -t <DestPhone> or -a, see
--help/-h for help""")
    else:
        parser.error("options -f and -p are mutually exclusive")


    return 1

if __name__ == "__main__":
    main()
