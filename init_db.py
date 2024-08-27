from models import Base, Product
from database import SessionLocal, engine


def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    products = [
        {"name": "Star", "code": "A-001", "category": "cloth", "size": ["S", "M"], "unit_price": 200, "inventory": 20, "color": ["Red", "Blue"]},
        {"name": "Moon", "code": "A-002", "category": "cloth", "size": ["M", "L"], "unit_price": 300, "inventory": 10, "color": ["Red", "White"]},
        {"name": "Eagle", "code": "B-001", "category": "pants", "size": ["M", "L"], "unit_price": 100, "inventory": 23, "color": ["Green"]},
        {"name": "Bird", "code": "B-002", "category": "pants", "size": ["S", "M", "L"], "unit_price": 50, "inventory": 12, "color": ["Black"]},
    ]
    
    for product_data in products:
        existing_product = db.query(Product).filter_by(name=product_data['name']).first()
        if existing_product is None:
            product = Product(**product_data)
            db.add(product)
        else:
            print(f"Product '{product_data['name']}' already exists. Skipping.")

    db.commit()
    db.close()