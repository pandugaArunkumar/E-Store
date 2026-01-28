from app import app
from models import db, Product

with app.app_context():
    Product.query.delete()
    db.session.commit()

    products = [
        # WOMEN WINTER
        Product(
            name="Women Winter Jacket",
            price=2499,
            category="Women",
            season="Winter",
            description="Warm women winter jacket",
            image="winter1.webp"
        ),
        Product(
            name="Women Wool Sweater",
            price=1799,
            category="Women",
            season="Winter",
            description="Soft wool sweater",
            image="winter2.jpg"
        ),

        # MEN WINTER
        Product(
            name="Men Winter Hoodie",
            price=1599,
            category="Men",
            season="Winter",
            description="Thick winter hoodie",
            image="winter3.jpg"
        ),
        Product(
            name="Men Winter Coat",
            price=2999,
            category="Men",
            season="Winter",
            description="Premium winter coat",
            image="winter4.jpg"
        ),
    ]

    db.session.add_all(products)
    db.session.commit()
    print("✅ Products added correctly")
