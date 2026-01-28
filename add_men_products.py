from app import app
from models import db, Product

men_products = [
    ("Men Formal Shirt", 1099, "shirt1.jpg"),
    ("Men jacket", 999, "shirt2.jpg"),
    ("Men shirt ", 199, "shirt3.jpg"),
    ("casual shirt", 1009, "shirt4.jpg"),
    ("stylish shirt", 1099, "shirt5.jpg"),
    ("Men Style Shirt", 799, "shirt6.jpg"),
    ("Men Stylish Shirt", 599, "shirt9.jpg"),
]

with app.app_context():
    # make sure tables exist
    db.create_all()

    # OPTIONAL: clear only men's products (safe)
    Product.query.filter_by(category="Men").delete()

    for name, price, image in men_products:
        product = Product(
            name=name,
            price=price,
            image=image,
            category="Men",      # 🔥 THIS IS THE KEY
            season="All",
            description=f"{name} perfect for everyday wear."
        )
        db.session.add(product)

    db.session.commit()
    print("✅ Men's products added successfully")
