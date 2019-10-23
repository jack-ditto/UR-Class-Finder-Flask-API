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
#df = pd.read_excel("courses_3.31.xlsx", sheet_name="Sheet1")
df = pd.read_excel("Spring 2020.xlsx", sheet_name="Sheet1")

# Fill blank spots with empty string
df.fillna('',inplace=True)
# Make title and professor lowercase
df['TITLE'] = df['TITLE'].apply(lambda t: t.lower())
df['LASTNAME'] = df['LASTNAME'].apply(lambda t: t.lower())

# Endpoint for query-ing database
class SearchClasses(Resource):

    def post(self):

            # Set up argument parser
            parser = reqparse.RequestParser()
            parser.add_argument('class_name', type=str)
            parser.add_argument('crn', type=str)
            parser.add_argument('professor', type=str)
            parser.add_argument('start_time', type=str)
            parser.add_argument('end_time', type=str)
            parser.add_argument('building', type=str)
            parser.add_argument('department', action='append')
            parser.add_argument('campus', type=str)
            parser.add_argument('course_number', type=str)
            parser.add_argument('days', type=str)

            args = parser.parse_args()

            # Assign variables from arguments
            _class_name = args['class_name'].lower() if args['class_name'] else ""
            _crn = args['crn']
            _professor = args['professor'].lower() if args['professor'] else ""
            _start_time = args['start_time']
            _end_time = args['end_time']
            _building = args['building']
            _department = args['department'] if args['department'] else []
            _campus = args['campus']
            _course_number = args['course_number']
            _days = args['days']

            # List of indexes of classes for filtering

            classes = df
            classes = classes[(classes['TITLE'].str.contains(_class_name)) | (not _class_name)]
            classes = classes[(classes['CRN'] == (int(_crn) if _crn else _crn)) | (not _crn)]
            classes = classes[(classes['LASTNAME'].str.contains(_professor)) | (not _professor)]
            classes = classes[(classes['SUBJ'].isin(_department)) | (len(_department) == 0)]
            
            

            # Build the response
            return_data = []
            for index, row in classes.iterrows():
                start_t, end_t = formatTimes(str(row['BEGIN']), str(row['END']))
                return_data.append(
                    {
                        'class_name': row['TITLE'].title(),
                        'crn': row['CRN'],
                        'professor': row['LASTNAME'].title(),
                        'start_time': start_t,
                        'end_time': end_t,
                        'building': row['BLDG'],
                        'department': row['SUBJ'],
                        'week_code': row['M'] + row['T'] + row['W'] + row['R'] + row['F'],
                        'level': row['CRSE']
                    }
                )

            return return_data

class SameClassSearch(Resource):

    def post(self):

        # Set up argument parser
        parser = reqparse.RequestParser()
        parser.add_argument('classes_names', action='append')
        args = parser.parse_args()
        _classes_names = list(set(args['classes_names'])) if args['classes_names'] else []

        classes = pd.DataFrame()
        for class_name in _classes_names:
            classes = pd.concat([classes, df[df['TITLE'] == class_name.lower()]])
        
        
        
        # Build the response
        return_data = []
        for index, row in classes.iterrows():
            start_t, end_t = formatTimes(str(row['BEGIN']), str(row['END']))
            return_data.append(
                {
                    'class_name': row['TITLE'].title(),
                    'crn': row['CRN'],
                    'professor': row['LASTNAME'].title(),
                    'start_time': start_t,
                    'end_time': end_t,
                    'building': row['BLDG'],
                    'department': row['SUBJ'],
                    'week_code': row['M'] + row['T'] + row['W'] + row['R'] + row['F'],
                    'level': row['CRSE']
                }
            )
        return return_data

class DateLastUpdated(Resource):

    def post(self):

        return "10/22/19"

# Add endpoint to app
api.add_resource(SearchClasses, '/SearchClasses')
api.add_resource(SameClassSearch, '/SameClassSearch')
api.add_resource(DateLastUpdated, '/dateLastUpdated')

if __name__ == "__main__":
    app.run(debug=False)
