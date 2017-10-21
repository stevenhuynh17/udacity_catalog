from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database_setup import Base, Brand, Model

app = Flask(__name__)

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine

DB = sessionmaker(bind=engine)
session = DB()

@app.route('/')
def Hello():
    brand = session.query(Brand).all()
    return render_template(
        'home.html', brands=brand
    )


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
