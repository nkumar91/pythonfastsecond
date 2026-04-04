from app.config.db import Base
from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cat_name = Column(String(255), nullable=False)
    cat_title = Column(String(255), nullable=False)
    cat_des = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Category(id={self.id}, cat_name='{self.cat_name}', cat_title='{self.cat_title}')>"
