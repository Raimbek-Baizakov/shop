from itertools import product

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://postgres:1106@localhost/shop_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return self.name


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    products = Product.query.order_by(Product.price).all()
    return render_template("index.html", data=products)


@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        in_stock = "in_stock" in request.form
        product = Product(name=name, price=float(price), in_stock=in_stock)

        try:
            db.session.add(product)
            db.session.commit()
            return redirect("/")
        except:
            return "Ошибка при добавлении товара"
    else:
        return render_template("create.html")


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=False)
