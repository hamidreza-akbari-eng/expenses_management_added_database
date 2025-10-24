from core.database import Base
from sqlalchemy import Column, DateTime, Integer, String, func


class ExpenseModel(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    description = Column(String)
    amount = Column(Integer)
    expense_date = Column(DateTime, default=func.now())
