from api import db, Class

classes = [
    {
        "class_name": "Computer Science",
        "crn": "1421",
        "professor": "Greg Rogers",
        "start_time": "9:00am",
        "end_time": "10:15am",
        "location": "JPSN 103",
        "department": "CMSC"
    },
    {
        "class_name": "Calculus",
        "crn": "5264",
        "professor": "Paul Smith",
        "start_time": "11:00am",
        "end_time": "12:15pm",
        "location": "JPSN 132",
        "department": "MATH"
    },
    {
        "class_name": "Spanish in the Media",
        "crn": "8562",
        "professor": "Leslie Kissling",
        "start_time": "3:00pm",
        "end_time": "5:00pm",
        "location": "INTC 210",
        "department": "LAIS"
    },
    {
        "class_name": "Intro to Microeconomics",
        "crn": "2142",
        "professor": "Grace Vanderwergen",
        "start_time": "2:00pm",
        "end_time": "3:15pm",
        "location": "BUS 312",
        "department": "ECON"
    },
    {
        "class_name": "Who Do You Trust?",
        "crn": "6342",
        "professor": "Carol Wittig",
        "start_time": "8:00am",
        "end_time": "9:15am",
        "location": "LIB 204",
        "department": "FYS"
    }
]

for c in classes:
    obj = Class(
        class_name = c["class_name"],
        crn = c["crn"],
        professor = c["professor"],
        start_time = c["start_time"],
        end_time = c["end_time"],
        location = c["location"],
        department = c["department"]
    )
    db.session.add(obj)

db.session.commit()
