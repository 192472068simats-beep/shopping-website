from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)

# Use an environment variable for secret key if available (recommended for Render)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-please-change")

# Sample product catalog (you can extend this list)
PRODUCTS = [
    {"id": 1, "name": "Trendy Kurti", "price": 399, "desc": "Comfortable cotton kurti, perfect for daily wear."},
    {"id": 2, "name": "Smart Watch", "price": 1499, "desc": "Fitness tracking, notifications and long battery life."},
    {"id": 3, "name": "Bluetooth Earbuds", "price": 799, "desc": "Wireless earbuds with noise reduction."},
    {"id": 4, "name": "Home Decor Lamp", "price": 699, "desc": "Stylish lamp to enhance your home ambience."},
    {"id": 5, "name": "Running Shoes", "price": 1299, "desc": "Lightweight shoes with excellent grip."},
    {"id": 6, "name": "Women Top Wear", "price": 499, "desc": "Casual top with breathable fabric."},
    {"id": 7, "name": "Backpack", "price": 899, "desc": "Durable backpack with multiple compartments."},
    {"id": 8, "name": "Sunglasses", "price": 299, "desc": "Polarized sunglasses with UV protection."},
    {"id": 9, "name": "Bluetooth Speaker", "price": 1099, "desc": "Portable speaker with rich sound."},
    {"id": 10, "name": "Desk Organizer", "price": 249, "desc": "Keep your desk tidy and organized."}
]

# Helper to get product by id
def get_product(pid):
    return next((p for p in PRODUCTS if p["id"] == pid), None)

@app.route("/")
def home():
    return render_template("index.html", products=PRODUCTS)

@app.route("/product/<int:pid>")
def product_detail(pid):
    product = get_product(pid)
    if not product:
        return redirect(url_for("home"))
    return render_template("product.html", product=product)

@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    pid = int(request.form.get("product_id"))
    product = get_product(pid)
    if not product:
        return redirect(url_for("home"))

    cart = session.get("cart", [])
    # store just id and price and name for simplicity
    cart.append({"id": product["id"], "name": product["name"], "price": product["price"]})
    session["cart"] = cart
    session.modified = True
    return redirect(url_for("cart"))

@app.route("/cart")
def cart():
    cart = session.get("cart", [])
    total = sum(item["price"] for item in cart)
    return render_template("cart.html", items=cart, total=total)

@app.route("/remove/<int:index>", methods=["POST"])
def remove_item(index):
    cart = session.get("cart", [])
    if 0 <= index < len(cart):
        cart.pop(index)
        session["cart"] = cart
        session.modified = True
    return redirect(url_for("cart"))

@app.route("/clear_cart", methods=["POST"])
def clear_cart():
    session["cart"] = []
    session.modified = True
    return redirect(url_for("cart"))

if __name__ == "__main__":
    # only for local testing; Render will use gunicorn
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
