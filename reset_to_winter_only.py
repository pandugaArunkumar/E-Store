from app import app
from models import db, Product

with app.app_context():

    # ❌ DELETE ALL NON-WINTER PRODUCTS
    Product.query.filter(Product.category != "Winter").delete()
    db.session.commit()

    print("❌ Non-winter products removed")

    # ❄️ ADD REAL WINTER PRODUCTS
    winter_products = [
        Product(
            name="Winter wear",
            price=2499,
            category="Winter",
            description="Warm insulated winter wear",
            image="winter1.png"
        ),
        Product(
            name="Winter jacket",
            price=1599,
            category="Winter",
            description="Soft fleece winter jacket",
            image="winter2.jpg"
        ),
        Product(
            name="Winter wear sweater",
            price=2999,
            category="Winter",
            description="Premium long winter sweater",
            image="winter3.jpg"
        ),
        Product(
            name="Winter Sweater",
            price=1799,
            category="Winter",
            description="Woolen winter sweater",
            image="winter14.png"
        ),
        Product(
            name="Winter Wear",
            price=1999,
            category="Winter",
            description="Stylish winter daily wear",
            image="winter16.avif"
        ),
    ]

    db.session.add_all(winter_products)
    db.session.commit()

    print("✅ ONLY winter outfits exist now")
