from flask import Flask, render_template, request, redirect, url_for
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
    return render_template(
        'home.html', brands=brand
    )


@app.route('/new', methods=['GET', 'POST'])
def newModel():
    if request.method == 'POST':
        # brand = session.query(Brand).filter_by(name=request.form['name']).one()
        try:
            print "IN TRY BLOCK"
            brandname = session.query(Brand).filter_by(name=request.form['brand']).one()
            newModel = Model(
                name=request.form['name'],
                description=request.form['description'],
                price=request.form['price'],
                category=request.form['category'],
                brand=brandname
            )
            session.add(newModel)
            session.commit()

            return redirect(url_for("listModels", brand_id=brandname.id))

        except:
            print "IN EXCEPTION BLOCK"
            newBrand = Brand(
                name=request.form['brand']
            )
            session.add(newBrand)
            session.commit()

            print "NEW BRAND!"
            print newBrand.name

            newModel = Model(
                name=request.form['name'],
                description=request.form['description'],
                price=request.form['price'],
                category=request.form['category'],
                brand=session.query(Brand).filter_by(name=newBrand.name).one()
            )
            session.add(newModel)
            session.commit()

            return redirect(url_for("listModels", brand_id=newBrand.id))

    return render_template(
        'newModel.html'
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
    return render_template(
        'modelInfo.html', info=data
    )

@app.route('/models/<int:model_id>/edit', methods=['GET', 'POST'])
def editModel(model_id):
    print "EDITING MODEL!!!!"
    print model_id
    modified = session.query(Model).filter_by(id=model_id).one()
    if request.method == 'POST':
        if request.form['name']:
            modified.name = request.form['name']
            session.add(modified)
            session.commit()
        elif request.form['description']:
            modified.description = request.form['description']
            session.add(modified)
            session.commit()
        elif request.form['price']:
            modified.price = request.form['price']
            session.add(modified)
            session.commit()
        elif request.form['category']:
            modified.category = request.form['category']
        return redirect(url_for('modelInfo', model_id=model_id))
    else:
        return render_template(
            'editModel.html', model_id=model_id, car=modified
        )

@app.route('/models/<int:model_id>/delete', methods=['GET', 'POST'])
def deleteModel(model_id):
    print "MODEL ID"
    print model_id
    toDelete = session.query(Model).filter_by(id=model_id).one()
    if request.method == 'POST':
        session.delete(toDelete)
        session.commit()
        return redirect(url_for('listModels', brand_id=model_id))
    else:
        return render_template(
            "deleteModel.html", model_id=model_id, item=toDelete
        )

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
