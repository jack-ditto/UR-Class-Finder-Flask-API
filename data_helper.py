import pandas as pd
from datetime import datetime
from pandas import ExcelFile

'''
Parse string from excel file into formatted string
'''
def formatTime(time_string):

    # Get rid of trailing decimal present when converting float to str
    time_string = str(time_string).replace(".0", "")

    # If time is actually a value
    if time_string != "nan":
        formatted_time = datetime.strptime(f"{time_string[:2]}{time_string[2:]}", "%H%M")
        return formatted_time.strftime("%-I:%M %p")

    # Return NA if time passed is "nan"
    return "NA"

'''
Take in a list of indexes and a value, and add to the list if the index within
the database contains the value
'''
def filter_name_by_contains(data_file, value, column_name, classes_index_list):

    # Number of classes in table
    num_classes = len(data_file[data_file.columns[0]])

    # Store classes that are in classes_index_list and contain value
    filtered_list = []

    # Value sent from website is null
    if str(value) == "nan":
        return False
    value = str(value)

    # There are no classes in the current session yet
    if not classes_index_list:

        # Iterate through all classes
        for class_index in range(num_classes):
            if value.lower() in str(data_file[column_name][class_index]).lower():
                filtered_list.append(class_index)

    # There are classes in current session
    else:

        # Iterate only through current classes in session
        for i in range(len(classes_index_list)):
            if value in str(data_file[column_name][classes_index_list[i]]).lower():
                filtered_list.append(classes_index_list[i])

    # Return the list, filtered
    return filtered_list

'''
Take in a list of indexes and a list of values, and add to the list if the index within
the database contains one of the values
'''
def filter_list_by_contains(data_file, value_list, column_name, classes_index_list):
    # Number of classes in table
    num_classes = len(data_file[data_file.columns[0]])

    # Store classes that are in classes_index_list and contain value
    filtered_list = []

    # Value sent from website is null
    if not value_list or not value_list.split():
        return classes_index_list
        
    value_list = value_list.split()

    # There are no classes in the current session yet
    if not classes_index_list:

        # Iterate through all classes
        for class_index in range(num_classes):
            for v in value_list:
                if v in data_file[column_name][class_index]:
                    filtered_list.append(class_index)

    # There are classes in current session
    else:

        # Iterate only through current classes in session
        for i in range(len(classes_index_list)):

            # Compare with each value in list
            for v in value_list:

                if v in data_file[column_name][classes_index_list[i]]:
                    filtered_list.append(classes_index_list[i])

    # Return the list, filtered
    return filtered_list
'''
Return the value as a string if it exists / != "nan". Return the missing_replacement
if not.
'''
def check_value(data_file, column_name, index, missing_replacement):

    converted_title = str(data_file[column_name][index])

    if(converted_title and converted_title != "nan"):
        return converted_title

    return missing_replacement
