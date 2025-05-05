from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.orm import Session, declarative_base, relationship, sessionmaker

# SQLAlchemy DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./shop.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    Product_ID = Column(Integer, primary_key=True, index=True)
    Product_Name = Column(String(500))
    Storage_Amount = Column(Integer)
    Product_Price = Column(Float)
    items = relationship("OrderItem", back_populates="product")


class Order(Base):
    __tablename__ = "orders"
    Order_ID = Column(Integer, primary_key=True, index=True)
    Customer_Name = Column(String(100))
    Customer_Email = Column(String(100))
    Order_Total = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    OrderItem_ID = Column(Integer, primary_key=True, index=True)
    Order_ID = Column(Integer, ForeignKey("orders.Order_ID"))
    Product_ID = Column(Integer, ForeignKey("products.Product_ID"))
    Product_Amount = Column(Integer)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="items")


Base.metadata.create_all(bind=engine)

# Pydantic DB shemas
class ProductCreate(BaseModel):
    Product_Name: str
    Storage_Amount: int = Field(ge=0)
    Product_Price: float = Field(gt=0)


class ProductOut(ProductCreate):
    Product_ID: int
    class Config:
        orm_mode = True


class OrderItemCreate(BaseModel):
    Product_ID: int
    Product_Amount: int = Field(gt=0)


class OrderCreate(BaseModel):
    Customer_Name: str
    Customer_Email: str
    items: List[OrderItemCreate]


class OrderOut(BaseModel):
    Order_ID: int
    Customer_Name: str
    Customer_Email: str
    Order_Total: float
    items: List[OrderItemCreate]
    class Config:
        orm_mode = True


# FastAPI
app = FastAPI(title="Mini Shop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# produkti
@app.post("/products/", response_model=ProductOut)
def create_product(prod: ProductCreate, db: Session = Depends(get_db)):
    db_prod = Product(**prod.dict())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod


@app.get("/products/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


# pasutijumi
@app.post("/orders/", response_model=OrderOut)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # parbauda un aprekina kopejo cenu
    total = 0.0
    for item in order.items:
        prod = db.get(Product, item.Product_ID)
        if not prod:
            raise HTTPException(404, f"Produkts ar produkta ID {item.Product_ID} neeksistē")
        if prod.Storage_Amount < item.Product_Amount:
            raise HTTPException(400, f"Nepietiekams produkta {prod.Product_Name} (ID {item.Product_ID}) atlikums noliktavā (maks. = {prod.Storage_Amount})")
        total += prod.Product_Price * item.Product_Amount

    # izveido Order + OrderItem ierakstus
    db_order = Order(Customer_Name=order.Customer_Name,
                     Customer_Email=order.Customer_Email,
                     Order_Total=total)
    db.add(db_order)
    db.flush()                        # iegust Order_ID

    for item in order.items:
        db_item = OrderItem(Order_ID=db_order.Order_ID,
                             Product_ID=item.Product_ID,
                             Product_Amount=item.Product_Amount)
        db.add(db_item)
        # samazina noliktavas atlikumu
        prod = db.get(Product, item.Product_ID)
        prod.Storage_Amount -= item.Product_Amount

    db.commit()
    db.refresh(db_order)

    # atbilde
    return OrderOut(
        Order_ID=db_order.Order_ID,
        Customer_Name=db_order.Customer_Name,
        Customer_Email=db_order.Customer_Email,
        Order_Total=db_order.Order_Total,
        items=order.items
    )