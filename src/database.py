from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from config import Config
from pathlib import Path

# Ensure database directory exists
db_path = Path("/mount/src/ecommercepython/data")
db_path.mkdir(parents=True, exist_ok=True)

print(f"Using database at: {Config.DATABASE_URL}")  # Debug line

engine = create_engine(Config.DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(100))
    email = Column(String(100))
    is_admin = Column(Boolean, default=False)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    price = Column(Float)
    category = Column(String(50))
    description = Column(Text)
    image = Column(String(200))

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total = Column(Float)
    status = Column(String(20), default='pending')
    items = relationship('OrderItem', back_populates='order')  # Correct relationship name

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    order = relationship('Order', back_populates='items')  # Match relationship name
    product = relationship('Product')

engine = create_engine(Config.DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)