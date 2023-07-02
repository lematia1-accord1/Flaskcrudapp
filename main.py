from flask import Flask, flash, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='templates')

# app.secret_key = "Secret Key"

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/crud1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone


# this function created the tables in the database
with app.app_context():
    db.create_all()


@app.route('/')
def Index():
    allData = Data.query.all()

    return render_template('index.html', employees=allData)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        flash("Employee Inserted Successfully!")

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        myData = Data(name, email, phone)
        db.session.add(myData)
        db.session.commit()

        return redirect(url_for('Index'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        myData = Data.query.get(request.form.get('id'))

        myData.name = request.form['name']
        myData.email = request.form['email']
        myData.phone = request.form['phone']

        db.session.commit()
        flash("Employee Update Successfully.")

        return redirect(url_for('Index'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    myData = Data.query.get(id)
    db.session.delete(myData)
    db.session.commit()

    flash("Employee Deleted Successfully.")

    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
