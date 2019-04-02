from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
api = Api(app)
CORS(app)

# Set up the initial database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)

# Used to update database structure if / when needed
migrate = Migrate(app, db)

# Model for classes in database
class Class(db.Model):

    # Primary key
    id = db.Column(db.Integer, primary_key=True)
    # Campus / school
    campus = db.Column(db.String(4), unique=False, nullable=True)
    # CRN
    crn = db.Column(db.String(5), unique=False, nullable=True)
    # Subject, such as ECON
    department = db.Column(db.String(80), unique=False, nullable=True)
    # Coutse number, like 101
    course_number = db.Column(db.Integer, unique=False, nullable=True)
    # Section number
    section = db.Column(db.String(4), unique=False, nullable=True)
    # Title of class
    class_name = db.Column(db.String(80), unique=False, nullable=False)
    # Attribue, like SSIR
    attr = db.Column(db.String(80), unique=False, nullable=True)
    # Number of credits
    num_credits = db.Column(db.Float(20), unique=False, nullable=True)
    # Days of the week
    days = db.Column(db.String(7), unique=False, nullable=True)
    # Start time
    start_time = db.Column(db.String(80), unique=False, nullable=True)
    # End time
    end_time = db.Column(db.String(80), unique=False, nullable=True)
    # Building
    building = db.Column(db.String(10), unique=False, nullable=True)
    # Room number
    room = db.Column(db.String(10), unique=False, nullable=True)
    # Code (no idea what this is)
    code = db.Column(db.String(10), unique=False, nullable=True)
    # Professor name
    professor = db.Column(db.String(80), unique=False, nullable=True)
    # Additional notes about classes
    notes = db.Column(db.String(500), unique=False, nullable=True)
    # Time for lab, null if no lab
    lab_start = db.Column(db.String(80), unique=False, nullable=True)
    lab_end = db.Column(db.String(80), unique=False, nullable=True)
    lab_days = db.Column(db.String(7), unique=False, nullable=True)
    
    # String representation for testing
    def __repr__(self):
        return f'''<Name {self.class_name}>'''

# Endpoint for query-ing database
class RequestDatabase(Resource):

    def post(self):

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

            # These are the attributes to check for contains
            class_attributes = [_campus, _crn, _course_number,
            _class_name, _days, _start_time, _end_time, _professor]

            # Check if all params are either none or empty
            if not all(x is None or not x for x in args.values()):
                # Build query based on all parameters
                res = Class.query
                for a in class_attributes:
                    if a is not None:
                        res = res.filter(Class.class_name.contains(a))
                # Department is dropdown, so args are sent comma separated
                if _department:
                    _department = _department.split(",")
                    res = res.filter(Class.department.in_(_department))

                # Return classes that meet query
                print([x.crn for x in res.all()[:2]])
                return [
                    {
                        'class_name': c.class_name,
                        'crn': c.crn,
                        'professor': c.professor,
                        'start_time': c.start_time,
                        'end_time': c.end_time,
                        'building': c.building,
                        'department': c.department
                    }

                    for c in res.all()
                ]

            else:
                return []

        except Exception as e:
            print(str(e))
            return {'error': str(e)}

# Add endpoint to app
api.add_resource(RequestDatabase, '/RequestDatabase')

if __name__ == "__main__":
    app.run(debug=True)
