from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "12345"

# Home Page
@app.route("/")
def home():
    return render_template("index.html")

# Product Page
@app.route("/product/<name>/<price>")
def product(name, price):
    return render_template("product.html", name=name, price=price)

# Add to Cart
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    name = request.form.get("name")
    price = int(request.form.get("price"))

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append({"name": name, "price": price})
    session.modified = True

    return redirect(url_for("cart"))

# Cart Page
@app.route("/cart")
def cart():
    items = session.get("cart", [])
    total = sum(item["price"] for item in items)
    return render_template("cart.html", items=items, total=total)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
