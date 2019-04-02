from api import db, Class
import pandas as pd
from pandas import ExcelFile

# Excel file to read from
df = pd.read_excel("201820_ABJ 2.xlsx", sheet_name="Sheet1")

# Number of columns
num_classes = len(df[df.columns[0]])

# Days of the week for building week code
days = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]

# JSON of class days and time
times = {}


def updateTimesJson(i, times_json, df):
    for d in days:
        if not str(df[d][i]) == "nan":
            if not d in times_json:
                times_json[d] = [
                    [
                        df["S TM"][i].strftime("%H:%M"),
                        df["E TM"][i].strftime("%H:%M")
                    ]
                ]
            else:
                times_json[d].append(
                    [
                        df["S TM"][i].strftime("%H:%M"),
                        df["E TM"][i].strftime("%H:%M")
                    ]
                )
    return times_json


# Iterate through columns
for i in range(num_classes):


    times = updateTimesJson(i, times, df)

    while i < num_classes and str(df["CRN"][i]) == str(df["CRN"][i+1]):
        

    # Build class object from data in file
    obj = Class(
        campus = df["CAMPUS"][i],
        crn = str(df["CRN"][i]),
        department = df["SUBJ"][i],
        course_number = str(df["CRSE"][i]),
        section = str(df["SEC"][i]),
        class_name = df["TITLE"][i],
        attr = str(df["ATTR"][i]),
        num_credits = str(df["CR"][i]),
        times = times,
        building = df["BLDG"][i],
        room = str(df["RM"][i]),
        code = str(df["CODE"][i]),
        professor = df["INSTRUCTOR"][i],
        notes = df["COMMENTS"][i]
    )



    classes_list.append(obj)

# db.session.add(obj)

db.session.commit()
