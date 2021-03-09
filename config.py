# Imports
#import pymongo
import discord
import random
import os

## MongoDB
#myclient = pymongo.MongoClient(os.environ.get("TELESCOPE_MONGO"))

# Owner IDS (People who have access to restart the bot)
OWNERIDS = [684155404078415890,
            282565295351136256]

DEBUG_PRINTS = True

MESSAGES_PER_SECOND_AVG = []
CURRENT_MESSAGE_SECOND_COUNT = 0

# Main Color (Replace the part after 0x with a hex code)
MAINCOLOR = 0x011740

# Error Color (Replace the part after the 0x with a hex code)
ERRORCOLOR = 0xED4337

def log(*args):
    if DEBUG_PRINTS: print(str(" ".join([str(elem) for elem in args])))

def get_avg_messages():
    total = 0
    for c in MESSAGES_PER_SECOND_AVG:
        total += c
    if total == 0 or len(MESSAGES_PER_SECOND_AVG) == 0:
        return 0
    return total/len(MESSAGES_PER_SECOND_AVG)