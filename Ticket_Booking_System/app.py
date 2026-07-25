from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SECRET_KEY"] = "secret123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///railway.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# -------------------------
# Make 'now' available in every template (e.g. for min date on forms)
# -------------------------

@app.context_processor
def inject_now():
    return {"now": datetime.now()}


# -------------------------
# Currency formatter available in every template, e.g. {{ format_currency(train.price) }}
# -------------------------

@app.template_global()
def format_currency(amount):
    try:
        return "₹{:,.0f}".format(amount)
    except (TypeError, ValueError):
        return "₹0"


# -------------------------
# Models
# -------------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    number = db.Column(db.String(20))
    source = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    departure = db.Column(db.String(20))
    arrival = db.Column(db.String(20))
    price = db.Column(db.Integer)
    image = db.Column(db.String(100), default="train1.jpg")
    rating = db.Column(db.Float, default=4.5)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    passenger_name = db.Column(db.String(100))
    train_name = db.Column(db.String(100))
    journey_date = db.Column(db.String(20))
    amount = db.Column(db.Integer)


# -------------------------
# Home
# -------------------------

@app.route("/")
def index():
    trains = Train.query.all()

    popular_routes = [
        {"from": "Delhi", "to": "Mumbai", "duration": "16h", "price": "₹2500"},
        {"from": "Delhi", "to": "Chandigarh", "duration": "4h", "price": "₹1200"},
        {"from": "Amritsar", "to": "Delhi", "duration": "6h", "price": "₹1800"},
    ]

    return render_template(
        "index.html",
        trains=trains,
        popular_routes=popular_routes
    )


# -------------------------
# Trains (list)
# -------------------------

@app.route("/trains")
def trains():
    trains = Train.query.all()
    return render_template("trains.html", trains=trains)


# -------------------------
# Train Detail
# -------------------------

@app.route("/train/<int:train_id>")
def train_detail(train_id):
    train = Train.query.get_or_404(train_id)
    return render_template("train_detail.html", train=train)


# -------------------------
# About
# -------------------------

@app.route("/about")
def about():
    return render_template("about.html")


# -------------------------
# Contact
# -------------------------

@app.route("/contact")
def contact():
    return render_template("contact.html")


# -------------------------
# Add Train
# -------------------------

@app.route("/add-train", methods=["GET", "POST"])
def add_train():
    if request.method == "POST":
        train = Train(
            name=request.form["name"],
            number=request.form["number"],
            source=request.form["source"],
            destination=request.form["destination"],
            departure=request.form["departure"],
            arrival=request.form["arrival"],
            price=request.form["price"],
            image=request.form.get("image", "train1.jpg"),
            rating=4.5
        )

        db.session.add(train)
        db.session.commit()

        flash("Train Added Successfully")
        return redirect(url_for("trains"))

    return render_template("add_train.html")


# -------------------------
# Book Ticket
# -------------------------

@app.route("/book/<int:id>", methods=["GET", "POST"])
def book(id):

    train = Train.query.get_or_404(id)

    if request.method == "POST":

        booking = Booking(
            passenger_name=request.form["passenger_name"],
            train_name=train.name,
            journey_date=request.form["journey_date"],
            amount=train.price
        )

        db.session.add(booking)
        db.session.commit()

        flash("Ticket Booked Successfully")

        # Send user to payment page for the booking they just created
        return redirect(url_for("payment", id=booking.id))

    return render_template("booking.html", train=train)


# -------------------------
# My Bookings
# -------------------------

@app.route("/bookings")
def bookings():

    data = Booking.query.all()

    return render_template(
        "my_bookings.html",
        bookings=data
    )


# -------------------------
# Payment
# -------------------------

@app.route("/payment/<int:id>", methods=["GET", "POST"])
def payment(id):
    booking = Booking.query.get_or_404(id)

    if request.method == "POST":
        flash("Payment Successful")
        return redirect(url_for("confirmation", id=booking.id))

    return render_template("payment.html", booking=booking)


# -------------------------
# Confirmation
# -------------------------

@app.route("/confirmation/<int:id>")
def confirmation(id):
    booking = Booking.query.get_or_404(id)
    return render_template("confirmation.html", booking=booking)


# -------------------------
# Login
# -------------------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        flash("Login Successful")
        return redirect(url_for("index"))

    return render_template("login.html")


# -------------------------
# Register
# -------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=request.form["password"]
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful")

        return redirect(url_for("login"))

    return render_template("register.html")


# -------------------------
# Profile
# -------------------------

@app.route("/profile")
def profile():
    users = User.query.all()
    return render_template("profile.html", users=users)


# -------------------------
# 404 Error
# -------------------------

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


# -------------------------
# Database Init + Seed
# -------------------------

with app.app_context():
    db.create_all()

    if Train.query.count() == 0:

        trains = [
            Train(
                name="Rajdhani Express",
                number="12951",
                source="Delhi",
                destination="Mumbai",
                departure="16:00",
                arrival="08:00",
                price=2500,
                image="train2.jpg"
            ),
            Train(
                name="Shatabdi Express",
                number="12005",
                source="Delhi",
                destination="Chandigarh",
                departure="07:00",
                arrival="11:00",
                price=1200,
                image="train3.jpg"
            ),
            Train(
                name="Vande Bharat",
                number="22439",
                source="Amritsar",
                destination="Delhi",
                departure="14:30",
                arrival="20:30",
                price=1800,
                image="train4.jpg"
            )
        ]

        db.session.add_all(trains)
        db.session.commit()


# -------------------------
# Run Server
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)