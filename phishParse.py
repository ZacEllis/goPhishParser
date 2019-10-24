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
        at_matches = re.match(r'.*"address":"(\d+\.\d+\.\d+\.\d+)".*', raw_details)
        details = "IP_Address: " + at_matches.group(1)
    elif (action_type == "Clicked Link"):
        at_matches = re.match(r'.*"address":"(\d+\.\d+\.\d+\.\d+)".*', raw_details)
        details = "IP_Address: " + at_matches.group(1)

    elif (action_type == "Submitted Data"):
        un_match = re.match(r'.*"email.*?":\["(.*?)"\].*', raw_details, re.IGNORECASE)
        try:
            username = "Email: " + un_match.group(1)
        except Exception as e:
            username = "-"
            sys.stderr.write(f"Processing email: {e} - {raw_details}\n")
        pw_match = re.match(r'.*"pas.*?":\["(.*?)"\].*', raw_details, re.IGNORECASE)
        try:
            raw_pw = pw_match.group(1)
            pwd = f"Password: {raw_pw[:2]}" + "*" * (len(raw_pw) - 4) + f"{raw_pw[-2]}{raw_pw[-1]}"
        except Exception as e:
            pwd = "No Password Received"
            sys.stderr.write(f"Processing pwd: {e} - {raw_details}\n")
        details = username + "; " + pwd

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
except Exception as _:
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
