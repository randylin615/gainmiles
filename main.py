from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine
from models import Base, Product
from init_db import init_db
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
####################################
####################################
####################################
init_db() 
####################################
####################################
####################################

class ProductCreate(BaseModel):
    name: str
    code: str
    category: str
    size: List[str]
    unit_price: float
    inventory: int
    color: List[str]

class ProductRead(ProductCreate):
    name: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/", response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_name}", response_model=ProductRead)
def read_product(product_name: str, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.name == product_name).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.put("/products/{product_name}", response_model=ProductRead)
def update_product(product_name: str, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.name == product_name).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_name}")
def delete_product(product_name: str, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.name == product_name).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted successfully"}