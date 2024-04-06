from fastapi import FastAPI
from .models import user as user_model
from .repository import database
from .routes import auth, user, category, expense

user_model.Base.metadata.create_all(bind=database.engine)

summary = """
API для управления личным бюджетом. 🚀
"""

description = """
В этой версии реализовано:

* Получение токена доступа.
* Чтение пользователя.
* Создание пользователя.
"""

app = FastAPI(
title="Book keeper",
    summary=summary,
    description=description,
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
    contact={
        "name": "Рахимян Тимерханов",
        # "url": "http://x-force.example.com/contact/",
        "email": "timerkhanov.ri@phystech.edu",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(category.router)
app.include_router(expense.router)


@app.get("/")
def root():
    return {"message": "Welcome to my API"}

