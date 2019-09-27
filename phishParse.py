#!/usr/bin/env python3
# Parse goPhish csv for pretty tables
# zac@hacklabs.com - 25 Jan 2019

import csv
import re
import sys
from datetime import datetime, timedelta


def row_handle(row):
    (email, date_time, action_type, raw_details) = row

    dt_obj = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=11)
    new_date_time = dt_obj.strftime("%a %d %b - %H:%M")

    if (action_type == "Email Opened"):
        at_matches = re.match('.*"address":"(\d+\.\d+\.\d+\.\d+)".*', raw_details)
        details = "IP_Address: " + at_matches.group(1)
    elif (action_type == "Clicked Link"):
        at_matches = re.match('.*"address":"(\d+\.\d+\.\d+\.\d+)".*', raw_details)
        details = "IP_Address: " + at_matches.group(1)

    elif (action_type == "Submitted Data"):
        un_match = re.match('.*"Username.*?":\["(.*?)"\].*', raw_details, re.IGNORECASE)
        try:
            username = "Email: " + un_match.group(1)
        except:
            username = "USERNAME PARSE ERROR"
            print("Uhhh, he's dead jim - " + raw_details, sys.stderr)
        pw_match = re.match('.*"pas.*?":\["(.*?)"\].*', raw_details, re.IGNORECASE)
        raw_password = pw_match.group(1)
        password = f"Password: {raw_password[:2]}" + "*" * (len(raw_password) - 4) + f"{raw_password[-2]}{raw_password[-1]}"
        details = username + "; " + password

    elif (action_type == "Email Reported"):
        details = "-"

    else:
        raise ValueError("Action type did not match known types. Unexpected action: " + action_type)

    new_row = f"{email},{new_date_time},{action_type},{details}"

    return new_row


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <goPhish-Events-file.csv>")
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
    elif lineNum >= 2 and row[2] != "Email Sent":  # Ignore second line that's 'campaign created'
        print(row_handle(row))
    lineNum += 1
