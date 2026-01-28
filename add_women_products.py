from app import app
from models import db, Product

# 👗 WOMEN PRODUCTS DATA
women_products = [
    ("Women's Kurti", 1299, "kurti.jpg"),
    ("Women's Dress", 1999, "women1.avif"),
    ("Stylish Saree", 2499, "women2.webp"),
    ("Women's Top", 899, "women3.jpg"),
    ("Casual Kurti", 1599, "women4.jpg"),
    ("Party Wear Dress", 2999, "women9.jpg"),
    ("Elegant Saree", 3499, "women5.jpg"),
    ("Cotton Top", 999, "women8.webp"),
]

with app.app_context():
    # ✅ Make sure tables exist
    db.create_all()

    # ⚠️ OPTIONAL: Clear only WOMEN category (safe)
    Product.query.filter(Product.category == "Women").delete()

    # ➕ Insert products
    for name, price, image in women_products:
        product = Product(
            name=name,
            price=price,
            image=image,
            category="Women",
            season="All",
            description=f"{name} perfect for women."
        )
        db.session.add(product)

    db.session.commit()

    print("✅ Women products added successfully!")
