from expenses.routes import router as expenses_router
from fastapi import FastAPI
from users.routes import router as users_router

app = FastAPI()

app.include_router(expenses_router)
app.include_router(users_router)
