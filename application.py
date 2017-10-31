from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Brand, Model

app = Flask(__name__)

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine

DB = sessionmaker(bind=engine)
session = DB()


@app.route('/')
def main():
    brand = session.query(Brand).all()
    print "BRANDSSS"
    print brand
    return render_template(
        'home.html', brands=brand
    )


@app.route('/<int:brand_id>/models')
def listModels(brand_id):
    carMakers = session.query(Brand).all()
    models = session.query(Model).filter_by(model_id=brand_id).all()

    return render_template(
        'models.html', brands=carMakers, models=models
    )


@app.route('/models/<int:model_id>')
def modelInfo(model_id):
    data = session.query(Model).filter_by(id=model_id).one()
    print "INFORMATION!!!!"
    print data
    return render_template(
        'modelInfo.html', info=data
    )


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
