from flask import Flask
from flask_restful import Resource, Api, reqparse
import os
from flask_cors import CORS
import pandas as pd
from pandas import ExcelFile
from data_helper import *

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
api = Api(app)
CORS(app)

# Excel file to read from
df = pd.read_excel("courses_3.31.xlsx", sheet_name="Sheet1")

# Endpoint for query-ing database
class RequestDatabase(Resource):

    def post(self):

        # Uncomment this statement to keep running on error
        try:

            # Set up argument parser
            parser = reqparse.RequestParser()
            parser.add_argument('class_name', type=str)
            parser.add_argument('crn', type=str)
            parser.add_argument('professor', type=str)
            parser.add_argument('start_time', type=str)
            parser.add_argument('end_time', type=str)
            parser.add_argument('building', type=str)
            parser.add_argument('department', type=str)
            parser.add_argument('campus', type=str)
            parser.add_argument('course_number', type=str)
            parser.add_argument('days', type=str)

            args = parser.parse_args()

            # Assign variables from arguments
            _class_name = args['class_name']
            _crn = args['crn']
            _professor = args['professor']
            _start_time = args['start_time']
            _end_time = args['end_time']
            _building = args['building']
            _department = args['department']
            _campus = args['campus']
            _course_number = args['course_number']
            _days = args['days']

            # List of indexes of classes for filtering
            classes = []

            classes = filter_name_by_contains(df, _class_name, "TITLE", classes)
            classes = filter_name_by_contains(df, _crn, "CRN", classes)
            classes = filter_name_by_contains(df, _professor, "LASTNAME", classes)
            classes = filter_list_by_contains(df, _department, "SUBJ", classes)

            # Build the response
            return_data = []
            for class_index in classes:

                # Set professor to blank string if not specified
                professor = ""
                if str(df['LASTNAME'][class_index]) != "nan":
                    professor = str(df['LASTNAME'][class_index]),

                # Set building to blank string if not specified
                building = ""
                if str(df['BLDG'][class_index]) != "nan":
                    building = str(df['BLDG'][class_index])

                return_data.append(
                    {
                        'class_name': str(df['TITLE'][class_index]).title(),
                                             'crn': str(df['CRN'][class_index]),
                        'professor': professor,
                        'start_time': formatTime(df['BEGIN'][class_index]),
                        'end_time': formatTime(df['END'][class_index]),
                        'building': building,
                        'department': str(df['SUBJ'][class_index])
                    }
                )

            return return_data

        # Uncomment this statement to keep running on error
        except Exception as e:
            print(str(e))
            return {'error': str(e)}


# Add endpoint to app
api.add_resource(RequestDatabase, '/RequestDatabase')

if __name__ == "__main__":
    app.run(debug=True)
