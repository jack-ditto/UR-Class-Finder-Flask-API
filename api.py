from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
api = Api(app)

# Set up the initial database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
db = SQLAlchemy(app)

# Used to update database structure if / when needed
migrate = Migrate(app, db)

# Model for classes in database
class Class(db.Model):

    # Fields to be stored for each class
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(80), unique=False, nullable=False)
    crn = db.Column(db.String(10), unique=True, nullable=False)
    professor = db.Column(db.String(80), unique=False, nullable=True)
    start_time = db.Column(db.String(80), unique=False, nullable=True)
    end_time = db.Column(db.String(80), unique=False, nullable=True)
    location = db.Column(db.String(80), unique=False, nullable=True)
    department = db.Column(db.String(80), unique=False, nullable=True)

    # String representation for testing
    def __repr__(self):
        return f'''<Name {self.class_name}, CRN {self.crn}, Prof. {self.professor}
        Time {self.start_time} - {self.end_time}, Location {self.location},
        Dept. {self.department}'''

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
            parser.add_argument('location', type=str)
            parser.add_argument('department', type=str)
            args = parser.parse_args()

            # Assign variables from arguments
            _class_name = args['class_name']
            _crn = args['crn']
            _professor = args['professor']
            _start_time = args['start_time']
            _end_time = args['end_time']
            _location = args['location']
            _department = args['department']

            if not all(x is None for x in args.values()):

                print(args.values() != [None] * len(args.values()))
                # Build query based on all parameters
                res = Class.query
                if _class_name is not None:
                    res = res.filter(Class.class_name.contains(_class_name))
                if _crn is not None:
                    res = res.filter(Class.crn.contains(_crn))
                if _professor is not None:
                    res = res.filter(Class.professor.contains(_professor))
                if _start_time is not None:
                    res = res.filter(Class.start_time.contains(_start_time))
                if _end_time is not None:
                    res = res.filter(Class.end_time.contains(_end_time))
                if _location is not None:
                    res = res.filter(Class.location.contains(_location))
                if _department is not None:
                    res = res.filter(Class.department.contains(_department))

                # Return classes that meet query
                return [
                    {
                        'class_name': c.class_name,
                        'crn': c.crn,
                        'professor': c.professor,
                        'start_time': c.start_time,
                        'end_time': c.end_time,
                        'location': c.location,
                        'department': c.department
                    }

                    for c in res.all()
                ]

            else:
                return []

        except Exception as e:
            return {'error': str(e)}

# Add endpoint to app
api.add_resource(RequestDatabase, '/RequestDatabase')

if __name__ == "__main__":
    app.run(debug=True)
