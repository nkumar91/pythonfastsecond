from app.config.db import Base
from sqlalchemy import Column, Integer, String, Float, Text
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    product_image_url = Column(String(255), nullable=True)
    stock_quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
