from app.config.db import Base
from sqlalchemy import Column, DateTime, Integer, String, Float, Text
from sqlalchemy.sql import func
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    cat_id = Column(Integer, nullable=True)
    product_image_url = Column(String(255), nullable=True)
    stock_quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate =func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate =func.now())

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
