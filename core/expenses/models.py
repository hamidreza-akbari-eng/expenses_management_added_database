from core.database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship


class ExpenseModel(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    description = Column(String)
    amount = Column(Integer)
    expense_date = Column(DateTime, default=func.now())

    user = relationship("UserModel", back_populates="expenses", uselist=False)
