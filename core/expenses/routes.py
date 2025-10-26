from auth.jwt_auth import get_authenticated_user
from core.database import get_db
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from users.models import UserModel

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
    user: UserModel = Depends(get_authenticated_user),
):
    data = request.model_dump()
    data.update({"user_id": user.id})
    expense_obj = ExpenseModel(**data)

    db.add(expense_obj)
    db.commit()
    db.refresh(expense_obj)
    return expense_obj


@router.get("/retrive-expenses", response_model=list[ExpenseResponseSchema])
async def retrive_expenses(
    user: UserModel = Depends(get_authenticated_user),
    db: Session = Depends(get_db),
):
    expense_objs = db.query(ExpenseModel).all()
    if expense_objs:
        return expense_objs
    return {"message": "no expense found here!"}


@router.get("/retrive-expense/{expense_id}", response_model=ExpenseResponseSchema)
async def retrive_specefic_expense(
    user: UserModel = Depends(get_authenticated_user),
    expense_id: int = Path(...),
    db: Session = Depends(get_db),
):
    expense_obj = db.query(ExpenseModel).filter_by(id=expense_id).one_or_none()
    if expense_obj:
        return expense_obj
    return {"message": "no expense found here!"}


@router.put("/update-expense/{expense_id}", response_model=ExpenseResponseSchema)
async def update_expense(
    request: ExpenseUpdateSchema,
    user: UserModel = Depends(get_authenticated_user),
    expense_id: int = Path(...),
    db: Session = Depends(get_db),
):
    expense_obj = db.query(ExpenseModel).filter_by(id=expense_id).first()
    if expense_obj:
        expense_obj.description = request.description
        expense_obj.amount = request.amount
        db.commit()
        db.refresh(expense_obj)
        return expense_obj
    return {"message": "no such an expense found here!"}


@router.delete("/delete-expense/{expense_id}")
async def delete_expense(
    user: UserModel = Depends(get_authenticated_user),
    expense_id: int = Path(...),
    db: Session = Depends(get_db),
):
    expense_obj = db.query(ExpenseModel).filter_by(id=expense_id).one_or_none()
    if expense_obj:
        db.delete(expense_obj)
        db.commit()
        return {"message": "expense deleted successfully!"}
    return {"message": "no such an expense found here!"}
