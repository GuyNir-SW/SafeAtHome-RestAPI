from flask import Flask
from flask import jsonify
from flask import request

from app.config import config
from app.extensions import db
from app.models import Criminals, Users, Users_reports

app = Flask(__name__)
app.config.from_object(config['production'])
config['production'].init_app(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db.init_app(app)


def jsonify_results(results):
    results = jsonify(results)
    results.headers.add('Access-Control-Allow-Origin', '*')
    results.headers.add('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS')
    results.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return results


def verify_person(firstName, lastName, token):
    results = {
        'token': token,
        'firstName': firstName,
        'LastName': lastName
    }
    full_name = firstName + ' ' + lastName

    print("verifying {} token: {}".format(full_name, token))
    criminal_found = Criminal_data.objects(name=full_name).first()
    print(criminal_found)

    if criminal_found:
        report = criminal_found.to_json()
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
    return results


@app.route('/users/list', methods=['GET'])
def get_users_list():
    try:
        users_list = [user.to_json() for user in Users.objects]
        result = jsonify_results({
            "users": users_list
        })
        return result, 200
    except Exception as e:
        result = jsonify_results({'error': 'An error was occurred: ' + str(e)})
        return result, 400


@app.route('/criminals/list', methods=['GET'])
def get_criminals_list():
    try:
        criminals_list = [criminal.to_json() for criminal in Criminal_data.objects]
        result = jsonify_results({
            "criminals": criminals_list
        })
        return result, 200
    except Exception as e:
        result = jsonify_results({'error': 'An error was occurred: ' + str(e)})
        return result, 400


@app.route('/person', methods=['GET'])
def get_persons_report():
    person_data = request.form.to_dict(flat=False) or request.args.to_dict(
        flat=False)
    person_data = {k: v[0] if len(v) == 1 else v for k, v in
                   person_data.items()}

    token = person_data.get('token')
    firstName = person_data.get("firstName", '')
    lastName = person_data.get("lastName", '')
    if not token and not (firstName and lastName):
        return jsonify_results({'error': 'Must get token or firstName with lastName'}), 400

    try:
        user_found = Users.objects(token=token) or \
                     Users.objects(firstName=person_data.get("firstName"),
                                   LastName=person_data.get("lastName"))
        report_found = Users_reports.objects(token=token) or \
                       Users_reports.objects(firstName=person_data.get("firstName"),
                                             LastName=person_data.get("lastName"))
        if not user_found:
            return jsonify_results({'error': 'User didnt sign up'}), 400

        user_details = user_found.first().to_json()
        if report_found:
            reports = [report_.to_json() for report_ in report_found]
            result = jsonify_results({
                "user_details": user_details,
                "status": "Found report",
                "resultsCount": len(reports),
                "items": reports
            })
        else:
            result = jsonify_results({
                "user_details": user_details,
                "status": "No report was found",
                "resultsCount": 0,
                "items": []
            })

        return result, 200
    except Exception as e:
        result = jsonify_results({'error': 'An error was occurred: ' + str(e)})
        return result, 400


@app.route('/report', methods=['POST', 'PUT'])
def create_report():
    if request.headers.get('content-type') == 'application/json':
        person_data = request.get_json(force=True)
    else:
        person_data = request.form.to_dict(flat=False) or request.args.to_dict(
            flat=False)
        person_data = {k: v[0] if len(v) == 1 else v for k, v in
                       person_data.items()}
    logging.info("params received: " + str(person_data))

    token = person_data.get('token')

    if not person_data.get('token'):
        return jsonify_results({'error': 'token is missing'}), 400
    if not person_data.get("firstName"):
        return jsonify_results({'error': 'firstName is missing'}), 400
    if not person_data.get("lastName"):
        return jsonify_results({'error': 'lastName is missing'}), 400

    firstName = person_data.get("firstName")
    lastName = person_data.get("lastName")
    try:
        results = verify_person(firstName, lastName, token)
        results = jsonify_results(results)
        return results, 200

    except Exception as e:
        result = jsonify_results({'error': 'An error was occurred: ' + str(e)})
        return result, 400


@app.route('/newPerson', methods=['POST', 'PUT'])
def insert_person():
    if request.headers.get('content-type') == 'application/json':
        print(request.json)
        person_data = request.json or request.get_json(force=True)
    else:
        person_data = request.form.to_dict(flat=False) or request.args.to_dict(flat=False)
        person_data = {k: v[0] if len(v) == 1 else v for k, v in person_data.items()}
    logging.info("params received: " + str(person_data))

    if not person_data.get("id_num"):
        return jsonify_results({'error': "id_num is missing"}), 400
    if not person_data.get("firstName"):
        return jsonify_results({'error': 'firstName is missing'}), 400
    if not person_data.get("lastName"):
        return jsonify_results({'error': 'lastName is missing'}), 400
    if not person_data.get("token"):
        return jsonify_results({'error': 'token is missing'}), 400

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

        logging.info("results: " + str(results))
        results.update({
            "verification_results": verify_person(person_data.get("firstName"),
                                                  person_data.get("lastName"),
                                                  person_data.get("token"))})
        results = jsonify_results(results)
        return results, 201

    except Exception as e:
        result = jsonify_results({'error': 'An error was occurred: ' + str(e)})
        return result, 400


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)