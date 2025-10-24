from pydantic import BaseModel, Field


class ExpenseBaseSchema(BaseModel):
    description: str = Field(..., description="description of the expennse")
    amount: float = Field(..., description="amount of the expense")


class ExpenseCreateSchema(ExpenseBaseSchema):
    pass


class ExpenseResponseSchema(ExpenseBaseSchema):
    id: int = Field(..., gt=0)


class ExpenseUpdateSchema(ExpenseBaseSchema):
    pass
