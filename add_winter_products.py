from app import app
from models import db, Product
winter_products = [
    ("Winter casual wear", 999, "winter1.png"),   # ✅ FIXED
    ("Winter Sweater", 1799, "winter3.jpg"),
    ("Winter Coat", 2999, "winter5.jpg"),
    ("Puffer Jacket", 2199, "winter7.jpg"),
    ("Long Winter Coat", 3299, "winter8.webp"),
    ("Wool Coat", 2799, "winter9.jpg"),
    ("Oversized Coat", 2599, "winter10.jpg"),
    ("Winter Trench", 3499, "winter11.webp"),
    ("Snow Jacket", 3999, "winter12.jpg"),
    ("Brown Winter Coat", 2899, "winter13.jpg"),
    ("Casual Winter Wear", 1999, "winter15.jpg"),
    ("Stylish Winter Coat", 3199, "winter16.avif"),
    ("Classic Winter Coat", 3599, "wintercoat.webp"),
]


with app.app_context():
    # ✅ CREATE TABLES FIRST (THIS IS THE FIX)
    db.create_all()

    # ✅ SAFE DELETE
    Product.query.delete()

    for name, price, image in winter_products:
        product = Product(
            name=name,
            price=price,
            image=image,
            category="Unisex",
            season="Winter",
            description=f"{name} perfect for cold weather."
        )
        db.session.add(product)

    db.session.commit()
    print("✅ Winter products added successfully")
