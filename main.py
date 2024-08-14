from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, JSON, ForeignKey
from flask_login import UserMixin, login_user, LoginManager, login_required
import datetime as dt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


class Employee(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    password: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100), unique=True)


class Restaurant(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    menus = relationship('Menu', backref='restaurant')


class Menu(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    items: Mapped[dict] = mapped_column(JSON, nullable=False)
    restaurant_id: Mapped[int] = mapped_column(Integer, ForeignKey('restaurant.id'), nullable=False)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_employee(user_id):
    return db.get_or_404(Employee, user_id)


@app.route('/register', methods=['POST'])
def register():
    hash_salted_password = generate_password_hash(password=request.args.get('password'), method='pbkdf2:sha256', salt_length=8)
    new_user = Employee(
        password=hash_salted_password,
        username=request.args.get('username')
    )

    registered_user = db.session.execute(db.select(Employee).where(Employee.username == new_user.username)).scalar()
    if registered_user:
        return jsonify({'Failed': 'You`ve already sighed up with that email, log in instead!'})

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    return jsonify({"Success": "You have successfully registered."})


@app.route('/login', methods=['POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    employee = db.session.execute(db.select(Employee).where(Employee.username == username)).scalar()

    if not employee:
        return jsonify({"Not Found": "Sorry employee with this username was not found in the database."}), 404
    elif not check_password_hash(pwhash=employee.password, password=password):
        return jsonify({"Password incorrect": "Sorry but you enter the wrong password, please try again."}), 401
    else:
        login_user(employee)
        return jsonify({"Success": "You have successfully logged in."})


@app.route('/add_restaurant', methods=['POST'])
@login_required
def add_restaurant():
    name = request.args.get('name')

    new_restaurant = Restaurant(name=name)
    db.session.add(new_restaurant)
    db.session.commit()

    return jsonify({"message": "Restaurant created successfully"}), 201


@app.route('/restaurants/<int:restaurant_id>/menu', methods=['POST'])
@login_required
def upload_menu(restaurant_id):
    items = request.json.get('items')
    date = dt.date.today()

    menu = Menu(date=date, items=items, restaurant_id=restaurant_id)
    db.session.add(menu)
    db.session.commit()

    return jsonify({"message": "Menu uploaded successfully"}), 201


if __name__ == "__main__":
    app.run(debug=True)
