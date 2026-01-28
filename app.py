from flask import Flask, render_template, request, redirect, flash, url_for
from flask_login import (
    LoginManager, login_user, logout_user,
    current_user, login_required
)
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, User, Product, Cart, Order, Review,OrderItem
from datetime import datetime


# =====================
# APP CONFIG
# =====================
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret123'

db.init_app(app)


# =====================
# LOGIN MANAGER
# =====================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =====================
# HOME
# =====================
@app.route('/')
def home():
    return render_template('home.html')


# =====================
# REGISTER
# =====================
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form['email']).first():
            flash('Email already registered', 'danger')
            return redirect('/login')

        user = User(
            name=request.form['name'],
            email=request.form['email'],
            password=generate_password_hash(request.form['password'])
        )

        db.session.add(user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect('/login')

    return render_template('register.html')


# =====================
# LOGIN
# =====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()

        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect('/products')

        flash('Invalid credentials', 'danger')

    return render_template('login.html')


# =====================
# LOGOUT
# =====================
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


# =====================
# PRODUCTS  ✅ STEP 1 FIXED
@app.route('/products')
def products():
    page = request.args.get('page', 1, type=int)

    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    season = request.args.get('season', '').strip()
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    sort = request.args.get('sort', '')

    query = Product.query

    # 🔍 Search
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    # 📂 Category
    if category:
        query = query.filter(Product.category == category)

    # ❄️ Season
    if season:
        query = query.filter(Product.season == season)

    # 💰 Price Range
    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    # ↕️ Sorting
    if sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    elif sort == 'newest':
        query = query.order_by(Product.id.desc())
    else:
        query = query.order_by(Product.id.desc())  # default

    products = query.paginate(page=page, per_page=8, error_out=False)

    return render_template(
        'products.html',
        products=products
    )

   

# =====================
# ADD TO CART
# =====================
@app.route('/add-to-cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)

    cart_item = Cart.query.filter_by(
        user_id=current_user.id,
        product_id=product.id
    ).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(
            user_id=current_user.id,
            product_id=product.id,
            quantity=1
        )
        db.session.add(cart_item)

    db.session.commit()
    return redirect(url_for('cart'))


# =====================
# BUY NOW
# =====================
@app.route('/buy-now/<int:product_id>')
@login_required
def buy_now(product_id):
    product = Product.query.get_or_404(product_id)

    cart_item = Cart.query.filter_by(
        user_id=current_user.id,
        product_id=product.id
    ).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart(
            user_id=current_user.id,
            product_id=product.id,
            quantity=1
        )
        db.session.add(cart_item)

    db.session.commit()
    return redirect(url_for('cart'))


# =====================
# CART
# =====================
@app.route('/cart')
@login_required
def cart():
    items = Cart.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in items)

    return render_template('cart.html', cart=items, total=total)

@app.route('/admin/edit-product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    if current_user.role != 'admin':
        return redirect('/products')

    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.category = request.form['category']
        product.description = request.form['description']
        product.image = request.form['image']

        db.session.commit()
        flash("✅ Product updated successfully", "success")
        return redirect('/admin')

    return render_template('admin/edit_product.html', product=product)



# =====================
# PLACE ORDER
@app.route('/place-order', methods=['POST'])
@login_required
def place_order():
    address = request.form.get('address')
    city = request.form.get('city')
    pincode = request.form.get('pincode')
    phone = request.form.get('phone')

    if not address or not city or not pincode or not phone:
        flash("Please fill all delivery details", "danger")
        return redirect(url_for('cart'))

    cart_items = Cart.query.filter_by(user_id=current_user.id).all()

    if not cart_items:
        flash("Your cart is empty", "danger")
        return redirect(url_for('cart'))

    # ✅ CALCULATE TOTAL
    total = sum(item.product.price * item.quantity for item in cart_items)

    # ✅ CREATE ORDER
    order = Order(
        user_id=current_user.id,
        total_amount=total,
        status="Placed"
    )
    db.session.add(order)
    db.session.flush()  # get order.id

    # ✅ SAVE ORDER ITEMS
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.session.add(order_item)

    # ✅ CLEAR CART
    Cart.query.filter_by(user_id=current_user.id).delete()

    db.session.commit()

    flash("Order placed successfully 🎉", "success")
    return redirect(url_for('orders'))





# =====================
# REMOVE FROM CART
# =====================
@app.route('/remove-from-cart/<int:cart_id>')
@login_required
def remove_from_cart(cart_id):
    item = Cart.query.get_or_404(cart_id)

    if item.user_id != current_user.id:
        flash("Unauthorized action", "danger")
        return redirect('/cart')

    db.session.delete(item)
    db.session.commit()

    flash("Item removed", "success")
    return redirect('/cart')


# =====================
# PRODUCT DETAIL
# =====================
@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)

    reviews = Review.query.filter_by(product_id=id).all()

    related_products = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id
    ).limit(8).all()

    return render_template(
        'product_detail.html',
        product=product,
        reviews=reviews,
        related_products=related_products
    )
#-------------for my profile and my order---------------#

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/orders")
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id)\
                        .order_by(Order.created_at.desc())\
                        .all()
    return render_template("orders.html", orders=orders)



# =====================
# ADD REVIEW
# =====================
@app.route('/add-review/<int:product_id>', methods=['POST'])
@login_required
def add_review(product_id):
    review = Review(
        rating=int(request.form['rating']),
        comment=request.form['comment'],
        product_id=product_id,
        user_id=current_user.id
    )

    db.session.add(review)
    db.session.commit()

    return redirect(url_for('product_detail', id=product_id))

#========buy again==========


@app.route("/buy-again/<int:order_id>")
@login_required
def buy_again(order_id):
    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.id:
        flash("Unauthorized access", "danger")
        return redirect(url_for("orders"))

    for item in order.items:
        cart_item = Cart.query.filter_by(
            user_id=current_user.id,
            product_id=item.product_id
        ).first()

        if cart_item:
            cart_item.quantity += item.quantity
        else:
            db.session.add(Cart(
                user_id=current_user.id,
                product_id=item.product_id,
                quantity=item.quantity
            ))

    db.session.commit()
    flash("Items added to cart successfully!", "success")
    return redirect(url_for("cart"))

#---------------order status-----------

@app.route("/update-order-status/<int:order_id>/<status>")
@login_required
def update_order_status(order_id, status):
    order = Order.query.get_or_404(order_id)

    if current_user.role != "admin":
        flash("Unauthorized", "danger")
        return redirect(url_for("orders"))

    order.status = status
    db.session.commit()
    flash("Order status updated", "success")
    return redirect(url_for("orders"))

@app.route("/track/<int:order_id>")
@login_required
def track_order(order_id):
    order = Order.query.get_or_404(order_id)

    if order.user_id != current_user.id:
        flash("Unauthorized access", "danger")
        return redirect(url_for("orders"))

    return render_template("track_order.html", order=order)




# =====================
# ADMIN
# =====================
@app.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect('/products')

    products = Product.query.all()
    return render_template('admin/dashboard.html', products=products)


# =====================
# RUN APP
# =====================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
