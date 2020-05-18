from flask import Flask
from flask import jsonify
from flask import request

import os

# configs
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    MONGODB_HOST = os.environ.get('DATABASE_URL') or "mongodb+srv://tsilahadad:Noam3012@michal-sela-dspmm.gcp.mongodb.net/michal-sela?retryWrites=true&w=majority"
       #  "mongodb+srv://Michal_sela:hackathon@cluster0-4bsi2.gcp.mongodb.net/Bad_guys?retryWrites=true&w=majority"


    MONGODB_DB = os.environ.get('DB_NAME') or "Bad_guys"


config = {
    'production': ProductionConfig,
    'default': ProductionConfig
}

# extensions
from flask_mongoengine import MongoEngine

db = MongoEngine()

# models

import time
from datetime import datetime

from mongoengine import *

class Criminals(db.Document):
    name = StringField(required=True)
    birth_year = LongField(required=True)
    city_of_residence = StringField(required=True)
    felony = StringField(required=True)
    verdict = LongField(required=True)
    verdict_date = LongField(required=True)
    # db_last_update_date = DateTimeField(default=datetime.now())
    # db_last_update_date = LongField(default=int(time.time()))

    def to_json(self):
        json_person = {
            'name': self.name,
            'birth_year': self.birth_year,
            'city_of_residence': self.city_of_residence,
            'felony': self.felony,
            'verdict': self.verdict,
            'verdict_date': self.verdict_date,
            # 'db_last_update_date': self.db_last_update_date,
            # 'current_timestamp': datetime.now().strftime('%Y-%m-%d')
        }
        return json_person

    @staticmethod
    def from_json(json_person):
        return Criminals(name=json_person.get('name'),
                        birth_year=json_person.get('birth_year'),
                        city_of_residence=json_person.get('city_of_residence'),
                        felony=json_person.get('felony'),
                        verdict=json_person.get('verdict'),
                        verdict_date=json_person.get('verdict_date'))


class Users(db.Document):
    id_num = StringField(required=True)
    firstName = StringField(required=True)
    lastName = StringField(required=True)
    token = StringField(required=True)
    location = StringField(required=False)
    twitter = StringField(required=False)
    gender = StringField(required=False)
    job = StringField(required=False)
    pic = ListField(StringField(), default=list, required=False)
    birthday = DateTimeField(required=False)
    # db_last_update_date = DateTimeField(default=datetime.now())

    def to_json(self):
        json_user = {
            'id_num': self.id_num,
            'firstName': self.firstName,
            'lastName': self.lastName,
            'token': self.token,
            'location': self.location,
            'twitter': self.twitter,
            'gender': self.gender,
            'job': self.job,
            'pic': self.pic,
            'birthday': self.birthday,
            # 'db_last_update_date': self.db_last_update_date,
            # 'current_timestamp': datetime.now().strftime('%Y-%m-%d')
        }
        return json_user

    @staticmethod
    def from_json(json_user):
        return Users(
            id_num=json_user.get('id_num'),
            firstName=json_user.get('firstName'),
            lastName=json_user.get('lastName'),
            token=json_user.get('token'),
            location=json_user.get('location'),
            twitter=json_user.get('twitter'),
            gender=json_user.get('gender'),
            job=json_user.get('job'),
            pic=json_user.get('pic'),
            birthday=json_user.get('birthday'))


class Users_reports(db.Document):
    token = StringField(required=True)
    suspected = BooleanField(required=True)
    firstName = StringField(required=True)
    LastName = StringField(required=True)
    report = DictField(required=False)
    resultsCount = IntField(required=False)
    # db_last_update_date = DateTimeField(default=datetime.now())

    def to_json(self):
        json_report = {
            'token': self.token,
            'suspected': self.suspected,
            'firstName': self.firstName,
            'LastName': self.LastName,
            'report': self.report,
            'resultsCount': self.resultsCount
            # 'db_last_update_date': self.db_last_update_date,
            # 'current_timestamp': datetime.now().strftime('%Y-%m-%d')
        }
        return json_report

    @staticmethod
    def from_json(json_report):
        return Users_reports(
            token=json_report.get('token'),
            suspected=json_report.get('suspected'),
            firstName=json_report.get('firstName'),
            LastName=json_report.get('LastName'),
            report=json_report.get('report'),
            resultsCount=json_report.get('resultsCount'))


app = Flask(__name__)
app.config.from_object(config['production'])
config['production'].init_app(app)
#app.config['MONGO_HOST'] = "mongodb+srv://tsilahadad:Noam3012@michal-sela-dspmm.gcp.mongodb.net/michal-sela?retryWrites=true&w=majority"
#app.config["MONGODB_DATABASE"] = 'michal-sela'
db.init_app(app)


@app.route('/searchPerson', methods=['GET'])
def searchPerson():
    """Search for person info.."""
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    if firstName is None:
      return 'No first Name provided.', 400
    if lastName is None:
      return 'No last Name provided.', 400
    result = jsonify({
            "name": firstName + ' ' + lastName,
            "birth_year": 1972,
            "city_of_residence": "נשר",
            "felony": "החזקת חומרי פדופיליה",
            "verdict": "24 חודשי מאסר",
            "verdict_date": "ספט-07"
        })
    return result, 200


@app.route('/person', methods=['GET'])
def get_persons_report():
    person_data = request.form.to_dict(flat=False) or request.args.to_dict(
        flat=False)
    person_data = {k: v[0] if len(v) == 1 else v for k, v in
                   person_data.items()}

    if not person_data.get('token'):
        return jsonify({'error': 'token is missing'}), 400
    if not person_data.get("firstName"):
        return jsonify({'error': 'firstName is missing'}), 400
    if not person_data.get("lastName"):
        return jsonify({'error': 'lastName is missing'}), 400

    token = person_data.get('token')
    try:
        report_found = Users_reports.objects(token=token) or \
                       Users_reports.objects(firstName=person_data.get("firstName"), LastName=person_data.get("lastName"))
        if report_found:
            reports = [report_.to_json() for report_ in report_found]
            result = jsonify({
                "status": "Found report",
                "resultsCount": len(reports),
                "items": reports
            })
        else:
            result = jsonify({
                "status": "No report was found",
                "resultsCount": 0,
                "items": []
            })
        return result, 200
    except Exception as e:
        result = {'error': 'An error was occurred: ' + str(e)}
        return result, 400


@app.route('/report', methods=['POST', 'PUT'])
def create_report():
    person_data = request.form.to_dict(flat=False) or request.args.to_dict(
        flat=False)
    person_data = {k: v[0] if len(v) == 1 else v for k, v in
                   person_data.items()}

    token = person_data.get('token')
    if not token:
        return jsonify({'error': 'token is missing'}), 400
    if not person_data.get("firstName"):
        return jsonify({'error': 'firstName is missing'}), 400
    if not person_data.get("lastName"):
        return jsonify({'error': 'lastName is missing'}), 400

    full_name = person_data.get("firstName") + ' ' + person_data.get("lastName")
    results = {
        'token': token,
        'firstName': person_data.get("firstName"),
        'LastName': person_data.get("lastName")
    }

    try:
        print([criminal.to_json() for criminal in Criminals.objects])
        criminal_found = Criminals.objects(name=full_name)
        if criminal_found:
            report = [criminal.to_json() for criminal in criminal_found]
            results.update({
                'suspected': True,
                "resultsCount": len(report),
                'report': report
            })

        else:
            results.update({
                'suspected': False,
                "resultsCount": 0,
                'report': {}
            })

        report_exists = Users_reports.objects(token=token).first()
        if report_exists:
            report_exists.update(**results)
        else:
            user_report = Users_reports.from_json(results)
            user_report.save()

        return results, 200

    except Exception as e:
        result = {'error': 'An error was occurred: ' + str(e)}
        return result, 400


@app.route('/newPerson', methods=['POST', 'PUT'])
def insert_person():
    person_data = request.form.to_dict(flat=False) or request.args.to_dict(flat=False)
    person_data = {k: v[0] if len(v) == 1 else v for k, v in person_data.items()}

    if not person_data.get("id_num"):
        return {'error': "id_num is missing"}, 400
    if not person_data.get("firstName"):
        return jsonify({'error': 'firstName is missing'}), 400
    if not person_data.get("lastName"):
        return jsonify({'error': 'lastName is missing'}), 400

    try:
        user_exists = Users.objects(id_num=person_data.get("id_num"))

        if user_exists:
            user_exists.update(**person_data)
            results = {"status": "User was updated",
                       "user_details": person_data}
        else:
            user = Users.from_json(person_data)
            user.save()
            results = {"status": "New user was inserted",
                       "user_details": person_data}

        return jsonify(results), 201

    except Exception as e:
        result = {'error': 'An error was occurred: ' + str(e)}
        return result, 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
