# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from bson.objectid import ObjectId
from flask import Flask
from flask import jsonify
from flask import request

from app.config import config
from app.extensions import db
from app.models import Criminals, Users, Users_reports

app = Flask(__name__)
app.config.from_object(config['production'])
config['production'].init_app(app)
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
        print(str(e))
        result = {'error': 'An error was occurred: ' + str(e)}
        return result, 400


@app.route('/person', methods=['POST', 'PUT'])
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
        print(user_exists)

        if user_exists:
            user_exists.update(**person_data)
            results = {"status": "User was updated",
                       "user_details": person_data}
        else:
            user = Users.from_json(person_data)
            print(user.to_json())
            user.save()
            results = {"status": "New user was inserted",
                       "user_details": person_data}

        return jsonify(results), 201

    except Exception as e:
        print(str(e))
        result = {'error': 'An error was occurred: ' + str(e)}
        return result, 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
