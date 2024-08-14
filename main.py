from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


class Employees(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100), unique=True)


@login_manager.user_loader
def load_employee(user_id):
    return db.get_or_404(Employees, user_id)


with app.app_context():
    db.create_all()


@app.route('/login', methods=['POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    employee = db.session.execute(db.select(Employees).where(Employees.username == username)).scalar()

    if not employee:
        return jsonify({"Not Found": "Sorry employee with this username was not found in the database."}), 404
    elif not check_password_hash(pwhash=employee.password, password=password):
        return jsonify({"Password incorrect": "Sorry but you enter the wrong password, please try again."}), 401
    else:
        login_user(employee)
        return jsonify({"Success": "You have successfully logged in."})


@app.route('/register', methods=['POST'])
def register():
    hash_salted_password = generate_password_hash(password=request.args.get('password'), method='pbkdf2:sha256', salt_length=8)
    new_user = Employees(
        password=hash_salted_password,
        username=request.args.get('username')
    )

    registered_user = db.session.execute(db.select(Employees).where(Employees.username == new_user.username)).scalar()
    if registered_user:
        return jsonify({'Failed': 'You`ve already sighed up with that email, log in instead!'})

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    return jsonify({"Success": "You have successfully registered."})


# @app.route('/employee', methods=['POST'])
# def register():


if __name__ == "__main__":
    app.run(debug=True)
