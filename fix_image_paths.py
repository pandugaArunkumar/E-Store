from app import app
from models import db, Product

with app.app_context():
    products = Product.query.all()

    for p in products:
        if p.image.startswith("images/"):
            p.image = p.image.replace("images/", "")
            print(f"FIXED → ID {p.id}: {p.image}")

    db.session.commit()
    print("✅ All image paths fixed successfully")
