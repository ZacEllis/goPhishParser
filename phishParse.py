#!/usr/bin/env python3
# Parse goPhish csv for pretty tables
# zac@hacklabs.com - 25 Jan 2019

import csv, sys, re

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def row_handle(row):
    (email, date_time, action_type, raw_details) = row
    
    #Parse datetime
    dt_matches = re.match('\d{4}-(\d\d)-(\d\d)T(\d\d:\d\d):\d\dZ', date_time)
    month = months[int(dt_matches.group(1))]
    day = dt_matches.group(2)
    time = dt_matches.group(3)
    new_date_time = day + " " + month + " - " + str(time)

    if (action_type == "Email Opened"):
        at_matches = re.match('.*"address":"(\d+\.\d+\.\d+\.\d+)".*', raw_details)
        details = "IP_Address: " + at_matches.group(1)
    elif (action_type == "Clicked Link"):
        at_matches = re.match('.*"address":"(\d+\.\d+\.\d+\.\d+)".*', raw_details)
        details = "IP_Address: " + at_matches.group(1)

    elif (action_type == "Submitted Data"):
        un_match = re.match('.*"user.*?":\["(.*?)"\].*', raw_details, re.IGNORECASE)
        username = "Username: " + un_match.group(1)
        pw_match = re.match('.*"pass.*?":\["(.*?)"\].*', raw_details, re.IGNORECASE)
        raw_password = pw_match.group(1)
        password = "Password: " + (raw_password[:2] + "*"*(len(raw_password)-4) + raw_password[-2] + raw_password[-1])
        details = username + "; " + password

    else: 
        ValueError ("Action type did not match known types. Unexpected action: " + action_type)

    new_row = email+"," +new_date_time+"," + action_type+"," +details

    return new_row



if len(sys.argv) != 2: 
    print("Usage:", sys.argv[0],"<goPhish-Events-file.csv>")
    exit()

try:
    eventsFile = open(sys.argv[1])
except:
    print(f"Error opening file \"{sys.argv[1]}\"")
    exit()

fileIter = csv.reader(eventsFile, delimiter=',')
lineNum = 0
for row in fileIter:
    if lineNum == 0:
        print(row)
    elif lineNum >= 2 and row[2] != "Email Sent": # Ignore lineNum=1 because that's 'campaign created'
        print (row_handle(row))
    lineNum += 1



