from mongoengine import *

class Criminal_data(db.Document):
    name = StringField(required=True)
    ID_number = LongField(required=True)
    felony = StringField(required=True)
    verdict = LongField(required=True)
    verdict_date = LongField(required=True)
    # db_last_update_date = DateTimeField(default=datetime.now())
    # db_last_update_date = LongField(default=int(time.time()))

    def to_json(self):
        json_person = {
            'name': self.name,
            'ID_number': self.ID_number,
            'felony': self.felony,
            'verdict': self.verdict,
            'verdict_date': self.verdict_date,
            # 'db_last_update_date': self.db_last_update_date,
            # 'current_timestamp': datetime.now().strftime('%Y-%m-%d')
        }
        return json_person

    @staticmethod
    def from_json(json_person):
        return Criminal_data(name=json_person.get('name'),
                        ID_number=json_person.get('ID_number'),
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