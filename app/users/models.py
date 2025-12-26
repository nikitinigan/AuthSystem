from sqlalchemy import Boolean, Column, Integer, String, text
from app.database import Base


class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    middle_name = Column(String(100))
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)


    def __str__(self):
        return f"Пользователь {self.email}"