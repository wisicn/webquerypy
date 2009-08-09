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

import PyFetion
import time
import optparse

#global time interval between each SMS
smsWaitSeconds=5

def sendMsgToList(fromPhone,phonePasswd,
                  destPhoneList,msgStr='test fromPython',verbose=False):
#example for destPhoneList: ['13919801980','13819801980','15819801980']

    phoneObj = PyFetion.PyFetion(fromPhone,phonePasswd,"TCP",debug_type=verbose)
    try:
        phoneObj.login()
    except PyFetion.PyFetionSupportError,e:
        return 1
    except PyFetion.PyFetionAuthError,e:
        return 2

    if phoneObj.login_ok:
        for phone in destPhoneList:
            if phone:
                phoneObj.send_sms(msgStr,phone,True)
                time.sleep(smsWaitSeconds)
    else:
        return 1

    return 0

def sendMsgToPhones(fromPhone,phonePasswd,
                    destPhones,msgStr='test fromPython',verbose=False):
#example for destPhones: '13919801980,13819801980,15819801980'
    
    destList=destPhones.split(',')

    if destList:
        return sendMsgToList(fromPhone,phonePasswd,destList,msgStr,verbose)
    else:
        return 1

def sendMultiMsgToPhones(fromPhone,phonePasswd,destPhoneMsgList,verbose=False):    
# example for destPhoneMsgList:
# [('13819801980,13819811981,13919801980','message to be send'),
#  ('12319801980,12219811981','2nd message'),
#  ('12319801980','3rd message')]    
    phoneObj = PyFetion.PyFetion(fromPhone,phonePasswd,"TCP",debug_type=verbose)
    try:
        phoneObj.login()
    except PyFetion.PyFetionSupportError,e:
        return 1
    except PyFetion.PyFetionAuthError,e:
        return 2

    if phoneObj.login_ok:
        for eachPare in destPhoneMsgList:
            phoneList=eachPare[0].split(',')
            msgStr=eachPare[1]
            if phoneList:
                for phone in phoneList:
                    phoneObj.send_sms(msgStr,phone,True)
                    time.sleep(smsWaitSeconds)
    else:
        return 1

    return 0

def main():

    usage = "usage: %prog [options] <Your Message>"
    parser = optparse.OptionParser(usage)

    parser.add_option("-f", "--from", default=None,
                      dest="fromPhone", action="store" ,type="string",
                      help="the mobile phone from which the SMS will be sent")
    parser.add_option("-p", "--passwd", "--password", default=None,
                      dest="phonePasswd",action="store" ,type="string",
                      help="the password of the mobile phone")
    parser.add_option("-t", "--to", default=None,
                      dest="destPhone",action="store" ,type="string",
                      help="the mobile phone to which the SMS will be sent")
    parser.add_option("-v", "--verbose", dest="debugMode",action="store_true",
                      default=False,
                      help="verbose mode, show debug infomation")

    (options, args) = parser.parse_args()

    argc = len(args)
    smsStr = "hello world from sms"


    if not (options.fromPhone and options.phonePasswd and options.destPhone):
        parser.error("options -f and -p and -t are mutually exclusive")
    else:
        if argc == 0:
            inputLines=[]
            while 1:
                try:
                    inputStr = raw_input()
                except EOFError:
                    break
                else:
                    inputLines.append(inputStr)
            smsStr = '\n'.join(inputLines)
        elif argc > 1:
            parser.print_help()
            parser.error("incorrect number of arguments")
        else:
            smsStr = args[0]

        return sendMsgToPhones(fromPhone=options.fromPhone,
                               phonePasswd=options.phonePasswd,
                               destPhones=options.destPhone,
                               msgStr=smsStr,verbose=options.debugMode)


if __name__ == "__main__":
    main()
