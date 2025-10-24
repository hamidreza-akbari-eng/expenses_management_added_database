from core.database import get_db
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from expenses.models import ExpenseModel
from expenses.schemas import (
    ExpenseCreateSchema,
    ExpenseResponseSchema,
    ExpenseUpdateSchema,
)

router = APIRouter(tags=["expense"])


@router.post("/create-expense", response_model=ExpenseResponseSchema)
async def create_expense(
    request: ExpenseCreateSchema,
    db: Session = Depends(get_db),
):
    expense_obj = ExpenseModel(description=request.description, amount=request.amount)

    db.add(expense_obj)
    db.commit()
    return expense_obj


@router.get("/retrive-expenses", response_model=list[ExpenseResponseSchema])
async def retrive_expenses(db: Session = Depends(get_db)):
    expense_objs = db.query(ExpenseModel).all()
    return expense_objs


@router.get("/retrive-expense/{expense_id}", response_model=ExpenseResponseSchema)
async def retrive_specefic_expense(
    expense_id: int = Path(...),
    db: Session = Depends(get_db),
):
    expense_obj = db.query(ExpenseModel).filter_by(id=expense_id).one_or_none()
    return expense_obj


@router.put("/update-expense/{expense_id}", response_model=ExpenseResponseSchema)
async def update_expense(
    request: ExpenseUpdateSchema,
    expense_id: int = Path(...),
    db: Session = Depends(get_db),
):
    expense_obj = db.query(ExpenseModel).filter_by(id=expense_id).first()
    expense_obj.description = request.description
    expense_obj.amount = request.amount
    db.commit()
    db.refresh(expense_obj)
    return expense_obj


@router.delete("/delete-expense/{expense_id}")
async def delete_expense(
    expense_id: int = Path(...),
    db: Session = Depends(get_db),
):
    expense_obj = db.query(ExpenseModel).filter_by(id=expense_id).one_or_none()
    db.delete(expense_obj)
    db.commit()
    return {"message": "expense deleted successfully!"}
