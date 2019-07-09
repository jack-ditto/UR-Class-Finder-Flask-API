import pandas as pd
from datetime import datetime
from pandas import ExcelFile

'''
Parse string from excel file into formatted string

returns time as a string if it exists, otherwise returns empty string
'''
def formatTime(time_string):

    # Get rid of trailing decimal present when converting float to str
    time_string = str(time_string).replace(".0", "")

    # If time is actually a value
    if time_string:
        formatted_time = datetime.strptime(f"{time_string[:2]}{time_string[2:]}", "%H%M")
        return formatted_time.strftime("%-I:%M %p")

    # Return NA if time passed is "nan"
    return ''
