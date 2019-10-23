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
        #formatted_time = datetime.strptime(f"{time_string[:2]}{time_string[2:]}", "%H%M") 
        formatted_time = datetime.strptime(f"{time_string[:2]}{time_string[3:5]}", "%H%M")  
    
        return formatted_time.strftime("%-I:%M %p")

    # Return NA if time passed is "nan"
    return ''

def formatTimes(start_time_string, end_time_string):
    
    if start_time_string and end_time_string:

        start_t = datetime.strptime(start_time_string, "%I:%M:%S")
        end_t = datetime.strptime(end_time_string, "%I:%M:%S")
        
        if start_t.hour < 8:
            return start_t.strftime("%-I:%M") + " PM",  end_t.strftime("%-I:%M") + " PM"
        
        if start_t.hour < 12 and end_t.hour < 8:
            return start_t.strftime("%-I:%M") + " AM",  end_t.strftime("%-I:%M") + " PM"

        return start_t.strftime("%-I:%M") + " AM", end_t.strftime("%-I:%M") + " AM"
    
    return '', ''







