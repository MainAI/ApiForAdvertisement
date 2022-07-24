from typing import Union
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify, request
from flask.views import MethodView

app = Flask('app')
Base = declarative_base()

PG_DSN = 'postgresql://admin:1234@127.0.0.1:5432/flask_test_use'
engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)


class Advertisement(Base):
    __tablename__ = 'advertisements'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True, unique=True)
    description = Column(String, nullable=False)
    time = Column(DateTime, server_default=func.now())
    owner = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


Base.metadata.create_all(engine)


class HTTPError(Exception):
    def __init__(self, status_code: int, message: Union[str, list, dict]):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HTTPError)
def handle_invalid_usage(error):
    response = jsonify({
        "status_code": error.status_code,
        "message": error.message})
    response.status_code = error.status_code
    return response


class AdvertisementView(MethodView):

    def get(self, id_adv=None):
        with Session() as session:
            response = []
            if id_adv is None:
                advertisements = session.query(Advertisement). \
                    filter(Advertisement.is_active == True).all()
            else:
                advertisements = session.query(Advertisement). \
                    filter(Advertisement.id == id_adv, Advertisement.is_active == True)
                if not len(list(advertisements)):
                    raise HTTPError(404, "id not exist")
            for adv in advertisements:
                temp = {'id': adv.id,
                        'title': adv.title,
                        'description': adv.description,
                        'time': adv.time,
                        'owner': adv.owner}
                response.append(temp)
            return jsonify(response)

    def post(self):
        json_data = request.json
        with Session() as session:
            advertisement = Advertisement(**json_data)
            session.add(advertisement)
            try:
                session.commit()
                return jsonify({
                    **json_data
                })
            except IntegrityError:
                session.close()
                raise HTTPError(400, "not valid data")


    def patch(self, id_adv):
        json_data = request.json
        with Session() as session:
            advertisement = session.query(Advertisement). \
                filter(Advertisement.id == id_adv, Advertisement.is_active == True).first()
            advertisement.title = json_data.get('title')
            advertisement.description = json_data.get('description')
            session.add(advertisement)
            session.commit()
            return jsonify({
                'status_code': '204',
                'response': 'No content'
            })

    def delete(self, id_adv):
        with Session() as session:
            advertisement = session.query(Advertisement). \
                filter(Advertisement.id == id_adv, Advertisement.is_active == True).first()
            advertisement.is_active = False
            session.commit()
            return jsonify({
                'status_code': '200'
            })


app.add_url_rule('/advertisement/', view_func=AdvertisementView.as_view('get_advertisement'), methods=['GET'])
app.add_url_rule('/advertisement/', view_func=AdvertisementView.as_view('create_advertisement'), methods=['POST'])
app.add_url_rule('/advertisement/<id_adv>', view_func=AdvertisementView.as_view('select_modify'),
                 methods=['GET', 'PATCH', 'DELETE'])

app.run()
